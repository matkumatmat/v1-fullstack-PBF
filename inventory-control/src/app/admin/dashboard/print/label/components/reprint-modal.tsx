"use client";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PrintPayloadItem } from "../types";
import { useState, useEffect } from "react";

type ReprintModalProps = {
  isOpen: boolean;
  onClose: () => void;
  item: PrintPayloadItem | null;
  onConfirm: (item: PrintPayloadItem, printerIp: string, isDebug: boolean) => void;
};

export function ReprintModal({ isOpen, onClose, item, onConfirm }: ReprintModalProps) {
  const [printerIp, setPrinterIp] = useState("192.168.1.100"); // Default printer IP
  const [isDebug, setIsDebug] = useState(false);

  const handleConfirm = () => {
    if (!item) return;
    onConfirm(item, printerIp, isDebug);
  };

  if (!item) return null;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Konfirmasi Reprint Label</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
            <div>
                <p>Anda akan mencetak ulang label berikut:</p>
                <p><strong>Detail:</strong> Box {item.box_number}</p>
                <p><strong>Petugas:</strong> {item.petugas}</p>
                <p><strong>Berat:</strong> {item.berat} Kg</p>
                <p><strong>Produk:</strong> {item.produk_list.map(p => `${p.nama} (${p.qty})`).join(', ')}</p>
            </div>
            <div className="space-y-2">
                <Label htmlFor="printerIp">Alamat IP Printer</Label>
                <Input
                    id="printerIp"
                    value={printerIp}
                    onChange={(e) => setPrinterIp(e.target.value)}
                />
            </div>
             <div className="flex items-center space-x-2">
                <input
                    type="checkbox"
                    id="isDebug"
                    checked={isDebug}
                    onChange={(e) => setIsDebug(e.target.checked)}
                />
                <Label htmlFor="isDebug">Cetak sebagai gambar (Debug)</Label>
            </div>
        </div>
        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>Batal</Button>
          <Button onClick={handleConfirm}>Konfirmasi & Cetak</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
