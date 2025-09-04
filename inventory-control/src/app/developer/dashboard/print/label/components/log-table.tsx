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
import { Log } from "../types";

type ApiResponse = {
  items: Log[];
  total_pages: number;
  current_page: number;
};

export function LogTable() {
    const [logs, setLogs] = useState<Log[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [loading, setLoading] = useState(true);

    const fetchLogs = async (page: number) => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:5000/api/logs?page=${page}`);
            if (!response.ok) {
                throw new Error('Failed to fetch logs');
            }
            const data: ApiResponse = await response.json();
            setLogs(data.items);
            setCurrentPage(data.current_page);
            setTotalPages(data.total_pages);
        } catch (error) {
            console.error("Error fetching logs:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs(currentPage);
    }, [currentPage]);

    const handlePageChange = (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            setCurrentPage(newPage);
        }
    }

    return (
        <div>
            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>
                                 Log</TableHead>
                            <TableHead>Tujuan</TableHead>
                            <TableHead>Detail Cetak</TableHead>
                            <TableHead>Waktu Cetak</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center">Memuat log...</TableCell>
                            </TableRow>
                        ) : logs.length > 0 ? (
                            logs.map((log) => (
                                <TableRow key={log.id}>
                                    <TableCell>{log.id}</TableCell>
                                    <TableCell>{log.pt_tujuan}</TableCell>
                                    <TableCell>Box {log.box_number} - {log.produk || 'N/A'}</TableCell>
                                    <TableCell>{new Date(log.tanggal_print).toLocaleString('id-ID')}</TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center">Belum ada riwayat cetak.</TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            <div className="flex items-center justify-between space-x-2 py-4">
                 <div className="text-sm text-muted-foreground">
                    Page {currentPage} of {totalPages}
                </div>
                <div className="space-x-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handlePageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </Button>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handlePageChange(currentPage + 1)}
                        disabled={currentPage >= totalPages}
                    >
                        Next
                    </Button>
                </div>
            </div>
        </div>
    )
}
