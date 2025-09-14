from sqlalchemy import Table, Column, Integer, ForeignKey
from ..configuration import BaseModel

allocation_batches_association = Table(
    'allocation_batches',
    BaseModel.metadata,
    Column('allocation_id', Integer, ForeignKey('allocations.id'), primary_key=True),
    Column('batch_id', Integer, ForeignKey('batches.id'), primary_key=True)
)