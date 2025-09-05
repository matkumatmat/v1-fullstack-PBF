from abc import ABC, abstractmethod
from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseService, transactional, audit_log
from ..schemas.base import PaginationSchema

class CRUDService(BaseService):
    """Service class dengan CRUD operations standard"""

    @property
    @abstractmethod
    def model_class(self):
        """Model class yang digunakan service ini"""
        pass

    @property
    @abstractmethod
    def create_schema(self):
        """Schema untuk create operations"""
        pass

    @property
    @abstractmethod
    def update_schema(self):
        """Schema untuk update operations"""
        pass

    @property
    @abstractmethod
    def response_schema(self):
        """Schema untuk response"""
        pass

    @transactional
    @audit_log('CREATE', 'Entity')
    async def create(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create new entity"""
        validated_data = self.create_schema.model_validate(data).model_dump()

        entity = self.model_class(**validated_data)
        self._set_audit_fields(entity)

        self.db_session.add(entity)
        await self.db_session.flush()

        return self.response_schema.model_validate(entity).model_dump()

    async def get_by_id(self, entity_id: int) -> Dict[str, Any]:
        """Get entity by ID"""
        entity = await self._get_or_404(self.model_class, entity_id)
        return self.response_schema.model_validate(entity).model_dump()

    async def get_by_public_id(self, public_id: str) -> Dict[str, Any]:
        """Get entity by public_id"""
        entity = await self._get_by_public_id_or_404(self.model_class, public_id)
        return self.response_schema.model_validate(entity).model_dump()

    async def list(self, page: int = 1, per_page: int = 20, search: str = None,
             filters: Dict[str, Any] = None, sort_by: str = None,
             sort_order: str = 'asc') -> Dict[str, Any]:
        """List entities with pagination, search, and filters"""
        query = select(self.model_class)

        if filters:
            query = await self._apply_filters(query, self.model_class, filters)

        if search and hasattr(self, 'search_fields'):
            query = await self._apply_search(query, self.model_class, search, self.search_fields)

        query = await self._apply_sorting(query, self.model_class, sort_by, sort_order)

        result = await self._paginate_query(query, page, per_page)

        return {
            'items': [self.response_schema.model_validate(item).model_dump() for item in result['items']],
            'pagination': result['pagination']
        }

    @transactional
    @audit_log('UPDATE', 'Entity')
    async def update(self, entity_id: int, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Update entity"""
        entity = await self._get_or_404(self.model_class, entity_id)

        validated_data = self.update_schema.model_validate(data).model_dump(exclude_unset=True)

        for key, value in validated_data.items():
            setattr(entity, key, value)

        self._set_audit_fields(entity, is_update=True)

        return self.response_schema.model_validate(entity).model_dump()

    @transactional
    @audit_log('DELETE', 'Entity')
    async def delete(self, entity_id: int, **kwargs) -> bool:
        """Delete entity"""
        entity = await self._get_or_404(self.model_class, entity_id)

        if hasattr(entity, 'is_active'):
            entity.is_active = False
            self._set_audit_fields(entity, is_update=True)
        else:
            self.db_session.delete(entity)

        return True

    @transactional
    @audit_log('ACTIVATE', 'Entity')
    async def activate(self, entity_id: int, **kwargs) -> Dict[str, Any]:
        """Activate entity (for soft delete support)"""
        entity = await self._get_or_404(self.model_class, entity_id)

        if hasattr(entity, 'is_active'):
            entity.is_active = True
            self._set_audit_fields(entity, is_update=True)
            return self.response_schema.model_validate(entity).model_dump()
        else:
            raise ValidationError("Entity does not support activation")
