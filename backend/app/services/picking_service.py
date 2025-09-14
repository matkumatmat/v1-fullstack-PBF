# file: app/services/outbound_service.py (CONTOH)

from app.models import RackItem, Allocation, RackStatusEnum

async def pick_from_rack(db: AsyncSession, rack_item_id: int, quantity_to_pick: int) -> RackItem:
    """
    Mengambil sejumlah kuantitas dari RackItem.
    Mengupdate kuantitas di Allocation dan status Rack jika item habis.
    """
    async with db.begin_nested():
        # 1. Ambil RackItem dan relasinya dengan lock untuk update
        item_query = select(RackItem).where(RackItem.id == rack_item_id).options(
            selectinload(RackItem.rack),
            selectinload(RackItem.allocation)
        ).with_for_update()
        
        item = (await db.execute(item_query)).scalar_one_or_none()
        
        if not item:
            raise NotFoundException(f"RackItem with id {rack_item_id} not found.")
        if quantity_to_pick > item.quantity:
            raise BadRequestException(f"Cannot pick {quantity_to_pick}. Only {item.quantity} available in rack.")

        # 2. ✅ LOGIKA "ONUPDATE": Update kuantitas
        item.quantity -= quantity_to_pick
        
        # Update kuantitas di Allocation
        item.allocation.shipped_quantity += quantity_to_pick
        item.allocation.reserved_quantity -= quantity_to_pick # Asumsi sudah direservasi
        item.allocation.allocated_quantity -= quantity_to_pick
        
        # 3. ✅ LOGIKA "ONUPDATE": Cek jika item habis
        if item.quantity == 0:
            # Item habis, ubah status rak kembali ke ACTIVE (kosong)
            item.rack.status = RackStatusEnum.ACTIVE
            # Hapus record RackItem karena sudah tidak ada isinya
            await db.delete(item)
        else:
            db.add(item)
            
        db.add(item.allocation)
        db.add(item.rack)
        
        await db.flush()
        
        # Jika item tidak dihapus, refresh state-nya
        if item.quantity > 0:
            await db.refresh(item)
            
        return item