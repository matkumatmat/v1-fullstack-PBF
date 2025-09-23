import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Pencil, Printer } from "lucide-react";

import { PrintQueueItem } from "../types";

type PrintQueueSectionProps = {
  items: PrintQueueItem[];
  isLoading: boolean;
};

export default function PrintQueueSection({ items, isLoading }: PrintQueueSectionProps) {
  
  const renderQueueTableBody = () => {
    if (isLoading) {
      // Tampilan skeleton saat loading
      return Array.from({ length: 3 }).map((_, index) => (
        <TableRow key={`skeleton-${index}`}>
          <TableCell><Skeleton className="h-5 w-48" /></TableCell>
          <TableCell><Skeleton className="h-5 w-20" /></TableCell>
          <TableCell><Skeleton className="h-8 w-24 rounded-full" /></TableCell>
          <TableCell>
            <div className="flex justify-center items-center gap-2">
              <Skeleton className="h-9 w-9" />
              <Skeleton className="h-9 w-9" />
            </div>
          </TableCell>
        </TableRow>
      ));
    }

    if (items.length === 0) {
      // Tampilan jika data kosong
      return (
        <TableRow>
          <TableCell colSpan={4} className="text-center h-24">
            Tidak ada data antrian.
          </TableCell>
        </TableRow>
      );
    }
    
    // Tampilan jika data ada
    return items.map((item) => {
      const totalBoxes = item.groups.reduce((acc, group) => acc + (group.to - group.from + 1), 0);
      return (
        <TableRow key={item.id}>
          <TableCell className="font-medium">{item.pt_tujuan}</TableCell>
          <TableCell>{totalBoxes} box</TableCell>
          <TableCell>
            <Badge variant="outline" className={item.status === 'done' ? 'text-green-300' : 'text-red-400'}>
                {item.status === 'done' ? 'Selesai' : 'Belum Selesai'}
            </Badge>
          </TableCell>
          <TableCell>
            <div className="flex justify-center items-center gap-2">
              <Button variant="outline" size="icon" className="text-slate-200 border-slate-600 hover:bg-green-900/50 hover:text-green-400 hover:border-green-600">
                <Printer className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" className="text-slate-200 border-slate-600 hover:bg-blue-900/50 hover:text-blue-400 hover:border-blue-600">
                <Pencil className="h-4 w-4" />
              </Button>
            </div>
          </TableCell>
          <TableCell>
            <div className="flex justify-center items-center gap-2">
              <Button variant="outline" size="icon" className="text-slate-200 border-slate-600 hover:bg-green-900/50 hover:text-green-400 hover:border-green-600">
                <Printer className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" className="text-slate-200 border-slate-600 hover:bg-blue-900/50 hover:text-blue-400 hover:border-blue-600">
                <Pencil className="h-4 w-4" />
              </Button>
            </div>
          </TableCell>
        </TableRow>
      );
    });
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Antrian Cetak</h1>
          <p className="text-slate-400 mt-1">Siapkan dan kelola daftar kiriman yang akan dicetak.</p>
        </div>
      </div>
      <Card className="mt-4">
        <CardContent className="">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[20%] text-lg -font-bold">Tujuan Pengiriman</TableHead>
                <TableHead className="w-[15%] text-lg font-bold">Total Box</TableHead>
                <TableHead className="w-[15%] text-lg font-bold">Status</TableHead>
                <TableHead className="w-[15%] text-lg font-bold">Keterangan</TableHead>
                <TableHead className="text-center text-lg w-[30%] font-bold">Aksi</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {renderQueueTableBody()}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}