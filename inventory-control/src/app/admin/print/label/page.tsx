// TIDAK ADA 'use client' di sini. Ini adalah Server Component.
// TIDAK ADA import useState atau useEffect.

import PageContainer from "@/components/layout/page-container";
import { PrintQueueItem } from "./types";
import { dummyPrintQueue } from "./dummy-data";
import PrintQueueSection from "./components/printqueuesection";
import QueuesectionModal from "./components/queuesection-modal";
import { CustomersDataTable } from "./components/customers-data-table";

// Fungsi untuk mengambil data. Ini berjalan di server.
async function getPrintQueueItems(): Promise<PrintQueueItem[]> {
  // Di dunia nyata, ini akan memanggil API Anda:
  // const response = await fetch('...');
  // const data = await response.json();
  // return data;

  // Untuk sekarang, kita simulasikan network delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  return dummyPrintQueue;
}

// Komponen halaman sekarang menjadi 'async'
export default async function LabelingPage() {
  // Data di-fetch di server SEBELUM halaman dikirim ke browser.
  const initialQueueItems = await getPrintQueueItems();

  return (
    <PageContainer>
      <div className="w-full p-4 space-y-8">
        
        {/* === BAGIAN 1: ANTRIAN CETAK === */}
        {/* Komponen ini menerima data awal sebagai props. */}
        {/* isLoading=false karena data sudah tersedia saat render. */}
        <PrintQueueSection items={initialQueueItems} isLoading={false} />
        
        <hr className="my-6 border-slate-700" />
        
        {/* === BAGIAN 2: MANAJEMEN ALAMAT === */}
        {/* Komponen ini adalah Client Component ('use client') yang mengelola state-nya sendiri */}
        <CustomersDataTable />

        <hr className="my-6 border-slate-700" />
        
        {/* Modal adalah Client Component */}
        <div className="fixed bottom-18 right-8 md:bottom-8 md:right-10 z-50">
          <QueuesectionModal />
        </div>

      </div>
    </PageContainer>
  );
}