from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.document_type import DocumentType, DocumentTypeCreate, DocumentTypeUpdate
import app.services.document_type as document_type_service

router = APIRouter()

@router.post("/", response_model=DocumentType)
async def create_document_type(
    document_type: DocumentTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await document_type_service.create_document_type(db=db, document_type=document_type)

@router.get("/", response_model=List[DocumentType])
async def read_document_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    document_types = await document_type_service.get_document_types(db, skip=skip, limit=limit)
    return document_types

@router.get("/{document_type_id}", response_model=DocumentType)
async def read_document_type(document_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_document_type = await document_type_service.get_document_type(db, document_type_id=document_type_id)
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type

@router.put("/{document_type_id}", response_model=DocumentType)
async def update_document_type(
    document_type_id: int,
    document_type: DocumentTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_document_type = await document_type_service.update_document_type(
        db, document_type_id=document_type_id, document_type=document_type
    )
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type

@router.delete("/{document_type_id}", response_model=DocumentType)
async def delete_document_type(
    document_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_document_type = await document_type_service.delete_document_type(db, document_type_id=document_type_id)
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type