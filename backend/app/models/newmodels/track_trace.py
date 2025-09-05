import uuid
from sqlalchemy import(
    Column, Integer, String, ForeignKey, 
    Text, DateTime, Date, Numeric, Boolean,
    Float, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .base import BaseModel

##saya butuh model untuk track and trace produk, dengan reference ke uuid dari packing_box
##ini akan berfungsi sebagai track trace produk, tabel disini akan mengisi detail scan.
#pada prosesnya pihak kurir dan penerima akan melakukan scan barcode yang ada di box, lalu akan mengupdate lokasi box tersebut
#jadi saya memerlukan field seperti long, lat, devices, foto, waktu, tanggal