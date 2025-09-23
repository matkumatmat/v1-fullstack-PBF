'use client' // Butuh ini untuk useState

import { useState } from 'react'
import { OutlinedInput } from '@/components/ui/outlined-input'
import ManualTabsProduk from './manual-tabs-produk'
import { Button } from '@/components/ui/button'
import { PlusCircle, Trash } from 'lucide-react'
import { ScrollArea } from '@/components/ui/scroll-area'

type ProductForm = {
  id: number;
};

export default function ManualTabContent() {
  // State untuk menyimpan daftar form produk
  const [products, setProducts] = useState<ProductForm[]>([{ id: 1 }]);
  
  const handleAddProduct = () => {
    setProducts(currentProducts => [
      ...currentProducts,
      { id: Date.now() } // ID unik
    ]);
  };

  const handleDeleteProduct = (idToDelete: number) => {
  // Filter keluar produk yang memiliki id yang sama dengan idToDelete
  setProducts(currentProducts => currentProducts.filter(product => product.id !== idToDelete));
  };

  return (
    <>
      {/* Bagian Form Atas (TETAP SAMA) */}
      <div className="space-y-6 px-6 pb-6">
        <OutlinedInput
          id="pt_tujuan"
          label="Daerah Tujuan"
          type="text"
          autoComplete="off"
        />
        <div className="grid grid-cols-4 gap-2">
          <OutlinedInput id="box_from" label="From" type="number" autoComplete="off" />
          <OutlinedInput id="box_to" label="To" type="number" autoComplete="off" />
          <OutlinedInput id="kode" label="Kode" type="text" autoComplete="off" />
          <OutlinedInput id="berat" label="Berat" type="text" autoComplete="off" />
        </div>
      </div>

<div className="px-6">
  <hr className="border-primary"/>
</div>

<ScrollArea className="h-48 w-full rounded-md px-4 pt-2">
  <div className="space-y-4">
    {products.map((product, index) => (
      <div key={product.id}>
        <div   key={product.id} className="flex justify-between items-center px-4">
          <h3 className="text-sm font-semibold text-muted-foreground">
            Produk #{index + 1}
          </h3>
          <div className='flex justify-end items-center mb-2 pt-2'>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleDeleteProduct(product.id)}
              className="
                group
                transition-all duration-150 
                hover:bg-red-600 
                active:bg-red-800/60 
              "
>
              <Trash 
                className="
                  h-4 w-4 text-slate-400
                  group-hover:text-red-400 
                "
              />
            </Button>
          </div>
        </div>
        <ManualTabsProduk />
      </div>
    ))}
  </div>
</ScrollArea>

<div className="flex justify-end px-6 pt-4">
  <Button variant="outline" onClick={handleAddProduct}>
    <PlusCircle className="mr-2 h-4 w-4" />
    Tambah
  </Button>
</div>
    </>
  )
}
