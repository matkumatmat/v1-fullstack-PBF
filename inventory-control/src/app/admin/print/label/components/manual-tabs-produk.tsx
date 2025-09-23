import { OutlinedInput } from "@/components/ui/outlined-input"
import { UnitCombobox } from "./unit-combo-box"

function ManualTabsProduk() {
  return (
    <>
      <div className="space-y-2 px-2 pb-6">
        <div className="grid grid-cols-2 gap-2">
          <OutlinedInput
            id="nama_produk"
            label="Produk"
            type="text"
            autoComplete="off"
          />
          <OutlinedInput
            id="batch"
            label="Batch"
            type="text"
            autoComplete="off"
          />
        </div>
        <div className="grid grid-cols-3 items-center gap-2">
          <OutlinedInput
            id="exp_date"
            label="Exp date"     
            type="text"
            autoComplete="off"
          />
          <OutlinedInput
            id="jumlah" 
            label="Quantity"
            type="text"
            autoComplete="off"
          />
          <div>
            <UnitCombobox />
          </div>
        </div>
      </div>
    </>
  )
}

export default ManualTabsProduk