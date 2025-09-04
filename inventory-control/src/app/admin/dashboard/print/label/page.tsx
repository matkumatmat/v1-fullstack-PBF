"use client";

import { Card, CardContent } from "@/components/ui/card";
import { AddressManagement } from "./components/address-management";
import { LogTable } from "./components/log-table";
import { QueueTable } from "./components/queue-table";
import { useState, useEffect } from "react";
import { Destination, PrintQueueItem, PrintPayloadItem } from "./types";
import { Button } from "@/components/ui/button";
import { KirimanModal } from "./components/kiriman-modal";
import { PrintConfirmModal } from "./components/print-confirm-modal";
import PageContainer from "@/components/layout/page-container";

export default function LabelingPage() {
  const [printQueue, setPrintQueue] = useState<PrintQueueItem[]>([]);
  const [allDestinations, setAllDestinations] = useState<Destination[]>([]);
  const [isKirimanModalOpen, setIsKirimanModalOpen] = useState(false);
  const [isPrintModalOpen, setIsPrintModalOpen] = useState(false);
  const [editingQueueIndex, setEditingQueueIndex] = useState<number | null>(null);
  const [isDataReady, setIsDataReady] = useState(false);

  useEffect(() => {
    const fetchAllDestinations = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/destinations?all=true`);
        const data = await response.json();
        setAllDestinations(data.items);
      } catch (error) {
        console.error("Failed to fetch all destinations:", error);
      } finally {
        setIsDataReady(true);
      }
    };
    fetchAllDestinations();
  }, []);

  const handleOpenKirimanModal = (index: number | null) => {
    setEditingQueueIndex(index);
    setIsKirimanModalOpen(true);
  };

  const handleSaveKiriman = (item: PrintQueueItem) => {
    if (editingQueueIndex !== null) {
      setPrintQueue(currentQueue =>
        currentQueue.map((q, i) => (i === editingQueueIndex ? item : q))
      );
    } else {
      setPrintQueue(currentQueue => [...currentQueue, item]);
    }
    setIsKirimanModalOpen(false);
    setEditingQueueIndex(null);
  };

  const handleDeleteQueueItem = (index: number) => {
    if (window.confirm("Yakin ingin menghapus item ini dari antrian?")) {
      setPrintQueue(currentQueue => currentQueue.filter((_, i) => i !== index));
    }
  };

  const handlePrintBatch = async (printerIp: string, isDebug: boolean) => {
    const itemsToPrintPayload: PrintPayloadItem[] = [];
    const itemsToUpdateStatus = printQueue.filter(item => item.status === "undone");

    itemsToUpdateStatus.forEach(item => {
      const totalLabelsInKiriman = item.groups.reduce(
        (acc, group) => acc + (group.to - group.from + 1),
        0
      );
      item.groups.forEach(group => {
        for (let i = group.from; i <= group.to; i++) {
          const payload = {
            id: item.id,
            box_number: `${i}/${totalLabelsInKiriman}`,
            petugas: group.petugas,
            berat: group.berat,
            produk_list: group.produk_list,
          };
          itemsToPrintPayload.push(payload);
        }
      });
    });

    if (itemsToPrintPayload.length === 0) {
      alert("Tidak ada item baru untuk dicetak.");
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/print-batch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items: itemsToPrintPayload,
          printer_ip: printerIp,
          debug: isDebug,
        }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Unknown error from server");

      alert(result.message);
      setPrintQueue(currentQueue =>
        currentQueue.map(item =>
          item.status === "undone" ? { ...item, status: "done" } : item
        )
      );
      setIsPrintModalOpen(false);
      // Consider refreshing log table here
    } catch (error) {
      if (error instanceof Error) {
        alert(`Error: ${error.message}`);
      } else {
        alert("An unknown error occurred during printing.");
      }
    }
  };
  
  const getPrintSummary = () => {
    const toPrint = printQueue.filter(item => item.status === 'undone');
    if (toPrint.length === 0) return "Tidak ada item baru untuk dicetak.";
    let totalLabels = toPrint.reduce((acc, item) => {
        return acc + item.groups.reduce((gAcc, group) => gAcc + (group.to - group.from + 1), 0);
    }, 0);
    return `Anda akan mencetak total <strong>${totalLabels}</strong> label dari <strong>${toPrint.length}</strong> kiriman.`;
  }

  return (
    <PageContainer>
      <div className="w-full p-4 space-y-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">Antrian Cetak</h1>
            <p className="text-slate-400 mt-1">
              Siapkan dan kelola daftar kiriman yang akan dicetak.
            </p>
          </div>
          <div className="flex items-center space-x-4 mt-4 sm:mt-0">
            <Button onClick={() => handleOpenKirimanModal(null)} disabled={!isDataReady}>
              {!isDataReady ? "Memuat data..." : "+ Buat Kiriman"}
            </Button>
            <Button variant="outline" onClick={() => setIsPrintModalOpen(true)}>Cetak Antrian</Button>
          </div>
        </div>

        <Card>
          <CardContent className="pt-6">
            <QueueTable
              queue={printQueue}
              onEdit={handleOpenKirimanModal}
              onDelete={handleDeleteQueueItem}
            />
          </CardContent>
        </Card>
        
        <KirimanModal
          isOpen={isKirimanModalOpen}
          onClose={() => {
              setIsKirimanModalOpen(false);
              setEditingQueueIndex(null);
          }}
          onSave={handleSaveKiriman}
          editingItem={editingQueueIndex !== null ? printQueue[editingQueueIndex] : null}
          allDestinations={allDestinations}
        />
        <PrintConfirmModal
          isOpen={isPrintModalOpen}
          onClose={() => setIsPrintModalOpen(false)}
          onConfirm={handlePrintBatch}
          summary={getPrintSummary()}
        />

        <hr className="my-6 border-slate-700" />

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Log Cetak</h1>
            <p className="text-slate-400 mt-1">
              Riwayat semua label yang telah diproses.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <LogTable />
          </CardContent>
        </Card>

        <hr className="my-6 border-slate-700" />

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">Manajemen Alamat</h1>
            <p className="text-slate-400 mt-1">
              Kelola semua data tujuan di database.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <AddressManagement />
          </CardContent>
        </Card>
      </div>
    </PageContainer>
  );
}
