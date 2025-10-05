// app/admin/testing/page.tsx

"use client";

import * as React from "react";
import PageContainer from "@/components/layout/page-container";
import FilteringLocation from "@/components/testing/filtering-location";
import PackingFormDialog from "@/components/testing/packing-form-dialog";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function TestingPage() {
  // State untuk "menjembatani" data antar komponen
  const [manipulatedDataFromFilter, setManipulatedDataFromFilter] = React.useState<object | null>(null);
  
  // State untuk menyimpan hasil akhir dari form
  const [finalJsonOutput, setFinalJsonOutput] = React.useState<object | null>(null);

  return (
    <PageContainer>
      <div className="w-full space-y-6">
        <h1 className="text-2xl font-bold">Halaman Testing Proses Pengiriman</h1>
        
        {/* Tahap 1: Filter Lokasi. Komponen ini akan mengirim data ke state di atas */}
        <FilteringLocation onDataManipulated={setManipulatedDataFromFilter} />
        
        {/* Tahap 2: Isi Form. Komponen ini menerima data dari state di atas */}
        <PackingFormDialog 
          manipulatedData={manipulatedDataFromFilter} 
          onFormSubmit={setFinalJsonOutput}
        />

        {/* Card untuk Debugging Hasil Manipulasi (dari Tahap 1) */}
        <Card>
            <CardHeader>
                <CardTitle>Hasil Manipulasi dari Filter</CardTitle>
                <CardDescription>Ini adalah data yang diterima dari komponen filter.</CardDescription>
            </CardHeader>
            <CardContent>
                <pre className="p-4 bg-muted rounded-md overflow-x-auto text-sm">
                    {manipulatedDataFromFilter 
                        ? JSON.stringify(manipulatedDataFromFilter, null, 2) 
                        : "Pilih lokasi di Tahap 1 untuk melihat datanya di sini."}
                </pre>
            </CardContent>
        </Card>

        {/* Tahap 3: Hasil Akhir */}
        <Card className="bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700">
          <CardHeader>
            <CardTitle>Hasil Akhir (Final JSON)</CardTitle>
            <CardDescription>
              Gabungan dari data tujuan dan data form. Siap kirim ke API.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="p-4 bg-background rounded-md overflow-x-auto text-sm">
              {finalJsonOutput 
                ? JSON.stringify(finalJsonOutput, null, 2) 
                : "Lengkapi form di Tahap 2 untuk melihat hasilnya di sini."}
            </pre>
          </CardContent>
        </Card>
      </div>
    </PageContainer>
  );
}