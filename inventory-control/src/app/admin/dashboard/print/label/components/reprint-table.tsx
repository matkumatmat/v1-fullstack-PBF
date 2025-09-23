"use client";

import { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { ClientSidePrintLog, PrintPayloadItem } from "../types";
import { ReprintModal } from "./reprint-modal";

type ReprintTableProps = {
    logTrigger: number;
}

type FlattenedLog = PrintPayloadItem & {
    batchId: string;
    pt_tujuan: string;
    timestamp: string;
};

export function ReprintTable({ logTrigger }: ReprintTableProps) {
    const [logs, setLogs] = useState<FlattenedLog[]>([]);
    const [isReprintModalOpen, setIsReprintModalOpen] = useState(false);
    const [itemToReprint, setItemToReprint] = useState<FlattenedLog | null>(null);

    useEffect(() => {
        const storedLogs: ClientSidePrintLog[] = JSON.parse(localStorage.getItem('reprint_cache') || '[]');
        const flattenedLogs = storedLogs.flatMap(batch => 
            batch.items.map(item => ({
                ...item,
                batchId: batch.id,
                pt_tujuan: batch.pt_tujuan,
                timestamp: batch.timestamp,
            }))
        );
        setLogs(flattenedLogs);
    }, [logTrigger]);

    const handleReprintClick = (log: FlattenedLog) => {
        setItemToReprint(log);
        setIsReprintModalOpen(true);
    };

    const handleReprintConfirm = async (item: PrintPayloadItem, printerIp: string, isDebug: boolean) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/print-batch`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    items: [item],
                    printer_ip: printerIp,
                    debug: isDebug,
                }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || "Unknown error from server");
            alert(result.message);
            setIsReprintModalOpen(false);
        } catch (error) {
            if (error instanceof Error) {
                alert(`Error: ${error.message}`);
            } else {
                alert("An unknown error occurred during reprinting.");
            }
        }
    };

    return (
        <div>
            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Tujuan</TableHead>
                            <TableHead>Detail Cetak</TableHead>
                            <TableHead>Waktu Cetak</TableHead>
                            <TableHead className="text-right">Aksi</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {logs.length > 0 ? (
                            logs.map((log, index) => (
                                <TableRow key={`${log.batchId}-${index}`}>
                                    <TableCell>{log.pt_tujuan}</TableCell>
                                    <TableCell>Box {log.box_number}</TableCell>
                                    <TableCell>{new Date(log.timestamp).toLocaleString('id-ID')}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm" onClick={() => handleReprintClick(log)}>Reprint</Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center">Belum ada riwayat cetak dari perangkat ini.</TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            <ReprintModal
                isOpen={isReprintModalOpen}
                onClose={() => setIsReprintModalOpen(false)}
                item={itemToReprint}
                onConfirm={handleReprintConfirm}
            />
        </div>
    )
}
