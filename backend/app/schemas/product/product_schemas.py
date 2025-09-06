from pydantic import BaseModel
from typing import Optional

class ProductTypeBase(BaseModel):
    public_id :str
    product_code :str
    name : str
    manufacturer : str
    product_type_id : int
    package_type_id : int
    temperature_type_id :int
    batches : Optional[int]=None
    