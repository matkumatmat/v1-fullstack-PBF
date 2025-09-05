from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import DocumentType
from app.schemas.document_type import DocumentTypeCreate, DocumentTypeUpdate

async def get_document_type(db: AsyncSession, document_type_id: int):
    result = await db.execute(select(DocumentType).filter(DocumentType.id == document_type_id))
    return result.scalar_one_or_none()

async def get_document_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DocumentType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_document_type(db: AsyncSession, document_type: DocumentTypeCreate):
    db_document_type = DocumentType(**document_type.dict())
    db.add(db_document_type)
    await db.commit()
    await db.refresh(db_document_type)
    return db_document_type

async def update_document_type(db: AsyncSession, document_type_id: int, document_type: DocumentTypeUpdate):
    db_document_type = await get_document_type(db, document_type_id)
    if db_document_type:
        update_data = document_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_document_type, key, value)
        await db.commit()
        await db.refresh(db_document_type)
    return db_document_type

async def delete_document_type(db: AsyncSession, document_type_id: int):
    db_document_type = await get_document_type(db, document_type_id)
    if db_document_type:
        await db.delete(db_document_type)
        await db.commit()
    return db_document_type