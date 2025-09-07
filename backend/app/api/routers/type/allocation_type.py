# file: app/api/routers/type/allocation_type.py (REFAKTORED)

# Impor pabrik fungsional kita.
from app.api.utils.crud_router_factory import create_crud_router

# Impor service object dan schemas yang relevan.
# Perhatikan kita sekarang mengimpor `type_service` yang berisi SEMUA instance CRUD generik.
from app.services import type_service
from app import schemas

### DEVIL'S ADVOCATE NOTE ###
# Kode asli berisi ~50 baris kode boilerplate untuk operasi CRUD.
# Dengan menggunakan pabrik, kita menggantinya dengan 6 baris deklaratif.
# Ini secara drastis meningkatkan keterbacaan dan kemudahan pemeliharaan.
# Jika kita perlu mengubah cara kerja otorisasi atau logging untuk SEMUA endpoint tipe,
# kita hanya perlu mengubahnya di satu tempat: `crud_router_factory.py`.

router = create_crud_router(
    # service: Kita menunjuk ke instance `allocation_type` dari `type_service`.
    # Pabrik akan tahu cara memanggil metode .create(), .get(), dll. dari objek ini.
    service=type_service.allocation_type,

    # response_schema: Skema yang digunakan untuk serialisasi output.
    response_schema=schemas.AllocationType,

    # Konfigurasi endpoint yang mandiri.
    prefix="/allocation-types",
    tags=["Master Data - Types"]
)