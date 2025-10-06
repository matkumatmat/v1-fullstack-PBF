// components/testing/manifest-table.tsx

"use client";

import * as React from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Tipe props yang diterima komponen ini dari induknya (page.tsx)
interface ManifestTableProps {
  manifests: any[];
  isLoading: boolean;
  error: string | null;
  onViewDetails: (publicId: string) => void;
  selectedManifestDetail: any | null;
  isDetailLoading: boolean;
}

export default function ManifestTable({
  manifests,
  isLoading,
  error,
  onViewDetails,
  selectedManifestDetail,
  isDetailLoading,
}: ManifestTableProps) {

  if (isLoading) return <Card><CardHeader><CardTitle>Daftar Manifest</CardTitle></CardHeader><CardContent>Memuat data manifest...</CardContent></Card>;
  if (error) return <Card><CardHeader><CardTitle>Error</CardTitle></CardHeader><CardContent><p className="text-destructive">{error}</p></CardContent></Card>;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Daftar Manifest Terkirim</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="border rounded-md">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>No. Packing Slip</TableHead>
                <TableHead>Tujuan</TableHead>
                <TableHead>Total Box</TableHead>
                <TableHead className="text-right">Aksi</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {manifests.length === 0 ? (
                <TableRow><TableCell colSpan={4} className="text-center">Belum ada manifest.</TableCell></TableRow>
              ) : (
                manifests.map((manifest) => (
                  <TableRow key={manifest.public_id}>
                    <TableCell><Badge variant="secondary">{manifest.packing_slip || 'N/A'}</Badge></TableCell>
                    <TableCell>{manifest.tujuan_kirim || 'N/A'}</TableCell>
                    <TableCell>{manifest.total_boxes || 'N/A'}</TableCell>
                    <TableCell className="text-right">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button variant="outline" size="sm" onClick={() => onViewDetails(manifest.public_id)}>
                            Lihat Detail
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-3xl">
                          <DialogHeader>
                            <DialogTitle>Detail Manifest: {manifest.packing_slip}</DialogTitle>
                          </DialogHeader>
                          <div className="max-h-[70vh] overflow-y-auto mt-4">
                            {isDetailLoading ? (
                              <p>Memuat detail...</p>
                            ) : (
                              <pre className="p-4 bg-muted rounded-md text-sm">
                                {selectedManifestDetail 
                                  ? JSON.stringify(selectedManifestDetail, null, 2)
                                  : "Gagal memuat atau data tidak ada."}
                              </pre>
                            )}
                          </div>
                        </DialogContent>
                      </Dialog>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}