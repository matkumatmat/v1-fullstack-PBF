from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.document_type import DocumentType, DocumentTypeCreate, DocumentTypeUpdate
from app.services.document_type import (
    create_document_type,
    delete_document_type,
    get_document_type,
    get_document_types,
    update_document_type,
)

router = APIRouter()

@router.post("/", response_model=DocumentType)
def create_new_document_type(
    document_type: DocumentTypeCreate, db: Session = Depends(get_db_session)
):
    return create_document_type(db=db, document_type=document_type)

@router.get("/{document_type_id}", response_model=DocumentType)
def read_document_type(document_type_id: int, db: Session = Depends(get_db_session)):
    db_document_type = get_document_type(db, document_type_id=document_type_id)
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type

@router.get("/", response_model=List[DocumentType])
def read_document_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    document_types = get_document_types(db, skip=skip, limit=limit)
    return document_types

@router.put("/{document_type_id}", response_model=DocumentType)
def update_existing_document_type(
    document_type_id: int,
    document_type: DocumentTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_document_type = update_document_type(
        db, document_type_id=document_type_id, document_type=document_type
    )
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type

@router.delete("/{document_type_id}", response_model=DocumentType)
def delete_existing_document_type(
    document_type_id: int, db: Session = Depends(get_db_session)
):
    db_document_type = delete_document_type(db, document_type_id=document_type_id)
    if db_document_type is None:
        raise HTTPException(status_code=404, detail="DocumentType not found")
    return db_document_type
