// src/app/admin/manage/customer/[CustomerId]/customer-detail-actions.tsx (VERSI OPTIMAL)

'use client';

import { useState } from 'react';
import { PlusCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { AddBranchForm } from '@/components/forms/add-branch-form';
import { AddLocationForm } from '@/components/forms/add-location-form';

// Aksi di level Customer (Tambah Cabang)
export function CustomerActions({ customerId }: { customerId: string }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" /> Tambah Cabang
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>Tambah Cabang Baru</DialogTitle>
        </DialogHeader>
        {/* 
          OPTIMISASI KUNCI:
          Form hanya di-render ke dalam DOM saat `isOpen` bernilai true.
          Ini memungkinkan code-splitting dan lazy loading.
        */}
        {isOpen && (
          <div className="py-4">
            <AddBranchForm customerId={customerId} onSuccess={() => setIsOpen(false)} />
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

// Aksi di level Branch (Tambah Lokasi)
export function BranchActions({ branchId, customerId }: { branchId: string, customerId: string }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <PlusCircle className="mr-2 h-4 w-4" /> Tambah Lokasi
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>Tambah Lokasi Baru</DialogTitle>
        </DialogHeader>
        {/* 
          OPTIMISASI KUNCI:
          Form hanya di-render ke dalam DOM saat `isOpen` bernilai true.
        */}
        {isOpen && (
          <div className="py-4">
            <AddLocationForm branchId={branchId} customerId={customerId} onSuccess={() => setIsOpen(false)} />
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}