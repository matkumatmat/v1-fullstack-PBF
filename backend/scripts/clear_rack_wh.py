# file: scripts/clear_racks_in_warehouse.py

import asyncio
import typer
from sqlalchemy.future import select
from sqlalchemy import delete

# --- [PERBAIKAN DIMULAI DI SINI] ---
import sys
import os

# Menambahkan path proyek agar impor `app` berfungsi
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# DEVIL'S ADVOCATE NOTE:
# Ini adalah perbaikan khusus untuk Windows.
# Kode ini memeriksa apakah sistem operasinya adalah Windows, dan jika ya,
# ia menetapkan kebijakan event loop ke `SelectorEventLoop` yang kompatibel
# dengan `psycopg`/`asyncpg`. Ini harus dilakukan sebelum `asyncio.run()` dipanggil.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# --- [AKHIR PERBAIKAN] ---


# Mengganti nama SessionLocal menjadi AsyncSessionLocal sesuai perubahan Anda
from app.database import AsyncSessionLocal as SessionLocal
from app.models import Warehouse, Rack, StockPlacement

cli = typer.Typer()

async def clear_racks(warehouse_id: int):
    """Menghapus semua rak dan penempatan stok terkait di dalam satu gudang."""
    
    print(f"Mencari rak di Warehouse ID: {warehouse_id}...")
    
    async with SessionLocal() as db:
        # ... (sisa logika fungsi ini tetap sama persis) ...
        warehouse = await db.get(Warehouse, warehouse_id)
        if not warehouse:
            typer.secho(f"ERROR: Warehouse dengan ID {warehouse_id} tidak ditemukan.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        rack_ids_query = select(Rack.id).where(Rack.warehouse_id == warehouse_id)
        rack_ids_result = await db.execute(rack_ids_query)
        rack_ids = [r_id for (r_id,) in rack_ids_result]

        if not rack_ids:
            typer.secho(f"Tidak ada rak yang ditemukan di Warehouse '{warehouse.name}'. Tidak ada yang perlu dihapus.", fg=typer.colors.YELLOW)
            return

        typer.echo(f"Ditemukan {len(rack_ids)} rak yang akan dihapus.")

        if not typer.confirm("Apakah Anda yakin ingin menghapus semua rak ini secara permanen?"):
            print("Operasi dibatalkan.")
            raise typer.Exit()

        delete_placements_stmt = delete(StockPlacement).where(StockPlacement.rack_id.in_(rack_ids))
        await db.execute(delete_placements_stmt)
        print("-> Penempatan stok (StockPlacement) terkait telah dihapus.")

        delete_racks_stmt = delete(Rack).where(Rack.id.in_(rack_ids))
        await db.execute(delete_racks_stmt)
        print("-> Rak telah dihapus.")

        await db.commit()
        typer.secho(f"✅ Berhasil menghapus {len(rack_ids)} rak dari Warehouse '{warehouse.name}'.", fg=typer.colors.GREEN)

@cli.command()
def run(
    warehouse_id: int = typer.Argument(..., help="ID numerik dari Warehouse yang raknya akan dihapus.")
):
    """
    Menghapus SEMUA rak di dalam satu warehouse spesifik.
    """
    asyncio.run(clear_racks(warehouse_id))

if __name__ == "__main__":
    cli()