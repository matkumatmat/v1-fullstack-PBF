"""
Base Service Classes
====================

Base classes dan utilities untuk semua services
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from functools import wraps
import logging
import uuid
import json

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .exceptions import WMSException, ValidationError, NotFoundError, ConflictError
from ..schemas import PaginationSchema

logger = logging.getLogger(__name__)

def transactional(func):
    """Decorator untuk automatic transaction management"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            if hasattr(self, 'db_session') and self.db_session:
                await self.db_session.commit()
            return result
        except Exception as e:
            if hasattr(self, 'db_session') and self.db_session:
                await self.db_session.rollback()
            logger.error(f"Transaction failed in {func.__name__}: {str(e)}")
            raise
    return wrapper

def audit_log(action: str, entity_type: str):
    """Decorator for intelligent audit logging."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            request_id = str(uuid.uuid4())
            
            # Extract context from kwargs
            ip_address = kwargs.get('ip_address')
            user_agent = kwargs.get('user_agent')
            username = kwargs.get('username')
            user_id = kwargs.get('user_id')

            old_values = None
            entity_id = None

            # For UPDATE actions, capture old state before execution
            if action == 'UPDATE' and args:
                entity_id = args[0]
                if hasattr(self, 'model_class') and hasattr(self, 'response_schema'):
                    try:
                        old_entity = await self._get_or_404(self.model_class, entity_id)
                        old_values = json.loads(self.response_schema.model_validate(old_entity).model_dump_json())
                    except NotFoundError:
                        # If entity not found, it will be caught in the main try-except block
                        pass

            try:
                result = await func(self, *args, **kwargs)
                
                if hasattr(self, 'audit_service') and self.audit_service:
                    final_entity_id = entity_id
                    new_values = None

                    if result:
                        if hasattr(result, 'id'):
                            final_entity_id = result.id
                        elif isinstance(result, dict) and 'id' in result:
                            final_entity_id = result['id']

                        if action == 'UPDATE':
                            # result is a dict with datetime objects, need to serialize it for comparison and logging
                            new_values = json.loads(self.response_schema.model_validate(result).model_dump_json())
                            
                            # Filter to show only changed values
                            if old_values:
                                changed_old = {k: v for k, v in old_values.items() if k in new_values and v != new_values[k]}
                                changed_new = {k: v for k, v in new_values.items() if k in old_values and v != old_values[k]}
                                old_values = changed_old
                                new_values = changed_new

                    await self.audit_service.log_action(
                        entity_type=entity_type,
                        entity_id=final_entity_id,
                        action=action,
                        user_id=user_id,
                        username=username,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        old_values=old_values,
                        new_values=new_values,
                        request_id=request_id,
                        severity="INFO"
                    )
                
                return result
                
            except Exception as e:
                if hasattr(self, 'audit_service') and self.audit_service:
                    # Try to get entity_id from args if not already set
                    if not entity_id and args and isinstance(args[0], int):
                        entity_id = args[0]

                    await self.audit_service.log_action(
                        entity_type=entity_type,
                        entity_id=entity_id,
                        action=f"{action}_FAILED",
                        user_id=user_id,
                        username=username,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        notes=str(e),
                        request_id=request_id,
                        severity="ERROR"
                    )
                raise
        return wrapper
    return decorator

class BaseService(ABC):
    """Base service class dengan common functionality"""
    
    def __init__(self, db_session: AsyncSession, current_user: str = None, 
                 audit_service=None, notification_service=None):
        self.db_session = db_session
        self.current_user = current_user
        self.audit_service = audit_service
        self.notification_service = notification_service
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def _get_or_404(self, model_class, entity_id: int, error_message: str = None):
        """Get entity by ID or raise 404 error"""
        result = await self.db_session.execute(select(model_class).filter(model_class.id == entity_id))
        entity = result.scalars().first()
        if not entity:
            resource_type = model_class.__name__
            raise NotFoundError(resource_type, entity_id)
        return entity
    
    async def _get_by_public_id_or_404(self, model_class, public_id: str):
        """Get entity by public_id or raise 404 error"""
        result = await self.db_session.execute(select(model_class).filter(model_class.public_id == public_id))
        entity = result.scalars().first()
        if not entity:
            resource_type = model_class.__name__
            raise NotFoundError(resource_type, public_id)
        return entity
    
    async def _validate_unique_field(self, model_class, field_name: str, field_value: Any, 
                              exclude_id: int = None, error_message: str = None):
        """Validate that field value is unique"""
        query = select(model_class).filter(getattr(model_class, field_name) == field_value)
        if exclude_id:
            query = query.filter(model_class.id != exclude_id)
        
        result = await self.db_session.execute(query)
        existing = result.scalars().first()
        if existing:
            message = error_message or f"{field_name} '{field_value}' already exists"
            raise ConflictError(message, model_class.__name__)
    
    async def _paginate_query(self, query, page: int = 1, per_page: int = 20, 
                       max_per_page: int = 100):
        """Paginate query results"""
        per_page = min(per_page, max_per_page)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db_session.execute(count_query)
        total = total_result.scalar()
        
        # Calculate pagination info
        pages = (total + per_page - 1) // per_page if total > 0 else 1
        has_prev = page > 1
        has_next = page < pages
        
        # Get paginated results
        offset = (page - 1) * per_page
        paginated_query = query.offset(offset).limit(per_page)
        items_result = await self.db_session.execute(paginated_query)
        items = items_result.scalars().all()
        
        return {
            'items': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages,
                'has_prev': has_prev,
                'has_next': has_next
            }
        }
    
    async def _apply_filters(self, query, model_class, filters: Dict[str, Any]):
        """Apply filters to query"""
        for field, value in filters.items():
            if value is not None:
                if hasattr(model_class, field):
                    query = query.filter(getattr(model_class, field) == value)
        return query
    
    async def _apply_search(self, query, model_class, search_term: str, search_fields: List[str]):
        """Apply text search to query"""
        if not search_term or not search_fields:
            return query
        
        search_conditions = []
        for field in search_fields:
            if hasattr(model_class, field):
                field_attr = getattr(model_class, field)
                search_conditions.append(field_attr.ilike(f'%{search_term}%'))
        
        if search_conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*search_conditions))
        
        return query
    
    async def _apply_sorting(self, query, model_class, sort_by: str = None, 
                      sort_order: str = 'asc', default_sort: str = 'id'):
        """Apply sorting to query"""
        sort_field = sort_by or default_sort
        
        if hasattr(model_class, sort_field):
            field_attr = getattr(model_class, sort_field)
            if sort_order.lower() == 'desc':
                query = query.order_by(field_attr.desc())
            else:
                query = query.order_by(field_attr.asc())
        
        return query
    
    def _set_audit_fields(self, entity, is_update: bool = False):
        """Set audit fields pada entity"""
        if is_update:
            entity.last_modified_by = self.current_user
            entity.last_modified_date = datetime.utcnow()
        else:
            entity.created_by = self.current_user
            entity.created_date = datetime.utcnow()
    
    async def _send_notification(self, notification_type: str, recipients: List[str], 
                          context: Dict[str, Any]):
        """Send notification through notification service"""
        if self.notification_service:
            try:
                await self.notification_service.send_notification(
                    notification_type=notification_type,
                    recipients=recipients,
                    context=context
                )
            except Exception as e:
                self.logger.warning(f"Failed to send notification: {str(e)}")

        
        