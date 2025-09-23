'use client'

import { useState, useEffect } from "react";
import PageContainer from "@/components/layout/page-container";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

import { PrintQueueItem } from "./types";
import { dummyPrintQueue } from "./dummy-data";

import PrintQueueSection from "./components/printqueuesection";
import QueuesectionModal from "./components/queuesection-modal";

import AddressManagementSection from "./components/addressmanagement";

export default function LabelingPages() {
  const [queueItems, setQueueItems] = useState<PrintQueueItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    const timer = setTimeout(() => {
      setQueueItems(dummyPrintQueue);
      setIsLoading(false);
    }, 1500); 

    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer>
      <div className="w-full p-4 space-y-8">
        
        {/* === BAGIAN 1: ANTRIAN CETAK (SEKARANG MENGGUNAKAN KOMPONEN) === */}
        <PrintQueueSection items={queueItems} isLoading={isLoading} />
        
        <hr className="my-6 border-slate-700" />
        
        {/* === BAGIAN 2: MANAJEMEN ALAMAT === */}
        <AddressManagementSection/>

        <hr className="my-6 border-slate-700" />
        
        <>
          <div className="fixed bottom-18 right-8 md:bottom-8 md:right-10 z-50">
            <QueuesectionModal />
          </div>
        </>

      </div>
    </PageContainer>
  )
}