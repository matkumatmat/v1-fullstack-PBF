"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { useState } from "react";

type PrintConfirmModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (printerIp: string, isDebug: boolean) => void;
  summary: string;
};

export function PrintConfirmModal({ isOpen, onClose, onConfirm, summary }: PrintConfirmModalProps) {
  const [printerIp, setPrinterIp] = useState("");
  const [isDebug, setIsDebug] = useState(true);

  const handleConfirm = () => {
    if (!printerIp) {
      alert("Masukkan IP Printer Zebra terlebih dahulu.");
      return;
    }
    onConfirm(printerIp, isDebug);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Konfirmasi Cetak</DialogTitle>
          <DialogDescription dangerouslySetInnerHTML={{ __html: summary }} />
        </DialogHeader>
        <div className="space-y-4 py-4">
            <Input 
                id="printer_ip"
                placeholder="Masukkan IP Printer Zebra"
                value={printerIp}
                onChange={e => setPrinterIp(e.target.value)}
                required
            />
            <div className="flex items-center space-x-2">
                <Checkbox 
                    id="debug-mode"
                    checked={isDebug}
                    onCheckedChange={(checked) => setIsDebug(!!checked)}
                />
                <Label htmlFor="debug-mode">Mode Debug (Simpan ke file .txt)</Label>
            </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="ghost" onClick={onClose}>Batal</Button>
          <Button type="button" onClick={handleConfirm}>Cetak Sekarang</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
