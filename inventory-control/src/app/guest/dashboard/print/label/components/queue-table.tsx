"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { PrintQueueItem } from "../types";

type QueueTableProps = {
    queue: PrintQueueItem[];
    onEdit: (index: number) => void;
    onDelete: (index:number) => void;
}

export function QueueTable({ queue, onEdit, onDelete }: QueueTableProps) {
    const getTotalLabels = (item: PrintQueueItem) => {
        return item.groups.reduce((acc, group) => acc + (group.to - group.from + 1), 0);
    }

    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Tujuan</TableHead>
                        <TableHead>Total Label</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Aksi</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {queue.length > 0 ? (
                        queue.map((item, index) => (
                            <TableRow key={index}>
                                <TableCell>{item.pt_tujuan}</TableCell>
                                <TableCell>{getTotalLabels(item)} Label ({item.groups.length} Grup)</TableCell>
                                <TableCell>
                                    <span className={item.status === 'done' ? 'text-green-400' : 'text-yellow-400'}>
                                        {item.status === 'done' ? 'Sudah Cetak' : 'Belum Cetak'}
                                    </span>
                                </TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="sm" onClick={() => onEdit(index)} className="mr-2">Edit</Button>
                                    <Button variant="ghost" size="sm" onClick={() => onDelete(index)} className="text-red-500 hover:text-red-400">Hapus</Button>
                                </TableCell>
                            </TableRow>
                        ))
                    ) : (
                        <TableRow>
                            <TableCell colSpan={4} className="text-center">Antrian cetak masih kosong.</TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
