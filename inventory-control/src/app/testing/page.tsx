// app/admin/testing/page.tsx

"use client";

import * as React from "react";
import { useCallback } from "react";
import { toast } from "sonner";
import PageContainer from "@/components/layout/page-container";
import FilteringLocation from "@/components/testing/filtering-location";
import PackingFormDialog from "@/components/testing/packing-form-dialog";
import ManifestTable from "@/components/testing/manifest-table"; // <-- KOMPONEN BARU
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { createManifest, getAllManifests, getManifestById } from "@/services/packingService"; // <-- PAKE SEMUA SERVICE
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";

// Fungsi transformasi data, kita butuh ini di sini
function transformApiData(apiData: any): any {
  if (!apiData || !apiData.location || !apiData.location.public_id) {
    return apiData;
  }
  const { location, ...restOfData } = apiData;
  return { ...restOfData, location_public_id: location.public_id };
}

export default function TestingPage() {
  // State untuk alur form
  const [manipulatedDataFromFilter, setManipulatedDataFromFilter] = React.useState<object | null>(null);
  const [finalJsonOutput, setFinalJsonOutput] = React.useState<object | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  // State BARU untuk tabel manifest
  const [manifests, setManifests] = React.useState<any[]>([]);
  const [isListLoading, setIsListLoading] = React.useState(true);
  const [listError, setListError] = React.useState<string | null>(null);
  
  // State BARU untuk detail di dialog
  const [selectedManifestDetail, setSelectedManifestDetail] = React.useState<any | null>(null);
  const [isDetailLoading, setIsDetailLoading] = React.useState(false);

  // Fungsi buat fetch daftar manifest, pake useCallback biar stabil
  const loadManifests = useCallback(async () => {
    setIsListLoading(true);
    try {
      const rawData = await getAllManifests();
      const transformedData = rawData.map(transformApiData);
      setManifests(transformedData);
    } catch (err: any) {
      setListError(err.message);
    } finally {
      setIsListLoading(false);
    }
  }, []);

  // Panggil loadManifests pas komponen pertama kali muncul
  React.useEffect(() => {
    loadManifests();
  }, [loadManifests]);

  // Fungsi buat kirim POST
  const handleSendManifest = async () => {
    if (!finalJsonOutput) return;
    setIsSubmitting(true);
    try {
      await createManifest(finalJsonOutput);
      toast.success("Manifest berhasil dibuat!");
      setFinalJsonOutput(null); // Kosongin form
      loadManifests(); // <-- INI DIA ANJING, REFRESH DATANYA!
    } catch (error: any) {
      toast.error("Gagal mengirim data", { description: error.message });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Fungsi buat lihat detail
  const handleViewDetails = async (publicId: string) => {
    setIsDetailLoading(true);
    setSelectedManifestDetail(null);
    try {
      const rawDetailData = await getManifestById(publicId);
      const transformedDetailData = transformApiData(rawDetailData);
      setSelectedManifestDetail(transformedDetailData);
    } catch (err: any) {
      toast.error("Gagal memuat detail manifest", { description: err.message });
    } finally {
      setIsDetailLoading(false);
    }
  };

  return (
    <PageContainer>
      <div className="w-full space-y-6">
        <h1 className="text-2xl font-bold">Halaman Testing Proses Pengiriman (All-in-One)</h1>
        
        {/* --- TAHAP 1 & 2 (TETAP SAMA) --- */}
        <FilteringLocation onDataManipulated={setManipulatedDataFromFilter} />
        <PackingFormDialog 
          manipulatedData={manipulatedDataFromFilter} 
          onFormSubmit={setFinalJsonOutput}
        />
        
        {/* Card Debugging Final Payload */}
        <Card>
          <CardHeader><CardTitle>Payload JSON (Debug)</CardTitle></CardHeader>
          <CardContent><pre className="p-4 bg-muted rounded-md overflow-x-auto text-sm">{finalJsonOutput ? JSON.stringify(finalJsonOutput, null, 2) : "Lengkapi form untuk melihat payload."}</pre></CardContent>
        </Card>
        
        {/* Tombol Kirim */}
        <div className="pt-4 border-t">
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button size="lg" className="w-full" disabled={!finalJsonOutput || isSubmitting}>
                {isSubmitting ? "Mengirim..." : "Kirim Manifest ke API"}
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader><AlertDialogTitle>Konfirmasi Pengiriman</AlertDialogTitle><AlertDialogDescription>Anda akan mengirim data manifest ini. Pastikan data sudah benar.</AlertDialogDescription></AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Batal</AlertDialogCancel>
                <AlertDialogAction onClick={handleSendManifest}>Ya, Kirim Sekarang</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>

        <hr className="my-8 border-dashed" />

        {/* --- TAHAP 3: TABEL HASIL (BARU) --- */}
        <ManifestTable
          manifests={manifests}
          isLoading={isListLoading}
          error={listError}
          onViewDetails={handleViewDetails}
          selectedManifestDetail={selectedManifestDetail}
          isDetailLoading={isDetailLoading}
        />
      </div>
    </PageContainer>
  );
}