# file: app/api/routers/type/product_type.py (REFAKTORED)

# Impor pabrik fungsional yang baru, bukan kelas yang lama.
from app.api.utils.crud_router_factory import create_crud_router

# Impor service object dan schemas yang akan kita gunakan.
from app.services import type_service
from app import schemas

### DEVIL'S ADVOCATE NOTE ###
# Ini adalah implementasi dari pola Pabrik Router Generik (Generic Router Factory).
# Alih-alih menulis 5 endpoint (create, get, get_all, update, delete) secara manual,
# kita memanggil satu fungsi pabrik yang membuat semuanya untuk kita.
# Ini secara drastis mengurangi duplikasi kode dan memastikan konsistensi di seluruh API.

router = create_crud_router(
    # service: Objek service generik yang berisi logika CRUD.
    # Pabrik ini akan memanggil metode .create(), .get(), dll. dari service ini.
    service=type_service.product_type,

    # response_schema: Skema Pydantic yang digunakan untuk serialisasi data
    # yang dikembalikan ke klien. Ini memastikan API kita memiliki kontrak output yang jelas.
    response_schema=schemas.ProductType,

    ### DEVIL'S ADVOCATE NOTE:
    # `create_schema` dan `update_schema` tidak lagi diperlukan sebagai argumen di sini.
    # Pabrik router yang baru cukup pintar untuk menyimpulkan (infer) tipe skema ini
    # langsung dari anotasi tipe generik pada `type_service.product_type`.
    # Ini adalah perbaikan yang menyelesaikan error Pylance "Variable not allowed in type expression".

    # prefix & tags: Konfigurasi untuk endpoint.
    # Dengan menempatkannya di sini, file ini menjadi sepenuhnya mandiri (self-contained).
    # File `api.py` utama hanya perlu meng-include router ini tanpa konfigurasi tambahan.
    prefix="/product-types",
    tags=["Master Data - Types"]
)