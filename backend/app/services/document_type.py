from sqlalchemy.orm import Session
from app.models.type import DocumentType
from app.schemas.document_type import DocumentTypeCreate, DocumentTypeUpdate

def get_document_type(db: Session, document_type_id: int):
    return db.query(DocumentType).filter(DocumentType.id == document_type_id).first()

def get_document_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DocumentType).offset(skip).limit(limit).all()

def create_document_type(db: Session, document_type: DocumentTypeCreate):
    db_document_type = DocumentType(**document_type.dict())
    db.add(db_document_type)
    db.commit()
    db.refresh(db_document_type)
    return db_document_type

def update_document_type(db: Session, document_type_id: int, document_type: DocumentTypeUpdate):
    db_document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
    if db_document_type:
        update_data = document_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_document_type, key, value)
        db.commit()
        db.refresh(db_document_type)
    return db_document_type

def delete_document_type(db: Session, document_type_id: int):
    db_document_type = db.query(DocumentType).filter(DocumentType.id == document_type_id).first()
    if db_document_type:
        db.delete(db_document_type)
        db.commit()
    return db_document_type
