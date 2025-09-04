import uuid
from sqlalchemy import(
    Column, Integer, String, ForeignKey, 
    Text, DateTime, Date, Numeric, Boolean,
    Float, Func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .base import BaseModel

##disini saya sepertinya memerlukan model untuk tracing movement dari produk secara end -to end hngga ke produk di terima oleh kurir