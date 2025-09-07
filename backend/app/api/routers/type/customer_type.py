# file: app/api/routers/type/customer_type.py (SUDAH DIPERBAIKI/DIREFAKTOR)

# Impor pabrik fungsional kita.
from app.api.utils.crud_router_factory import create_crud_router

# Impor service object dan schemas yang relevan.
from app.services import type_service
from app import schemas

# Buat router menggunakan pabrik, sama seperti router tipe lainnya.
router = create_crud_router(
    # Tunjuk ke service yang benar untuk customer_type
    service=type_service.customer_type,

    # Tentukan skema respons yang benar
    response_schema=schemas.CustomerType,

    # Konfigurasi endpoint
    prefix="/customer-types",
    tags=["Master Data - Types"]
)