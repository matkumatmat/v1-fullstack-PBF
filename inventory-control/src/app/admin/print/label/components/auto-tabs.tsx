// src/components/labeling/OtomatisTabContent.tsx

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { OutlinedInput } from '@/components/ui/outlined-input'

export default function OtomatisTabContent() {
  return (
    // Bungkus konten dengan Card juga
    <>
      <CardHeader>
        <CardTitle>Otomatis</CardTitle>
        <CardDescription>
          Pilih dari daftar pengiriman yang sudah ada untuk membuat antrian.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <OutlinedInput
          id="search_shipment"
          label="Cari Nomor Pengiriman..."
          type="search"
        />
        {/* Di sini nanti bisa ditambahkan daftar hasil pencarian */}
      </CardContent>
    </>
  )
}