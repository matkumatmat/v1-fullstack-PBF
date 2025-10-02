// app/main/labeling/components/add-customer-dialog.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { PlusCircle } from 'lucide-react';
import { CustomerForm } from './customer-form';
import {CustomerFormValues} from '@/constants/customer'

export function AddCustomerDialog() {
  const [open, setOpen] = useState(false);

  const handleFormSubmit = (data: CustomerFormValues) => {
    // Logika untuk mengirim data ke backend akan ada di sini
    // menggunakan useMutation dari TanStack Query.
    
    // Untuk sekarang, kita tutup dialog setelah submit.
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" />
          Tambah Customer
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[800px]">
        <DialogHeader>
          <DialogTitle>Tambah Customer Baru</DialogTitle>
          <DialogDescription>
            Isi detail customer dan alamat pengiriman. Klik simpan jika sudah selesai.
          </DialogDescription>
        </DialogHeader>
            <div className="w-full flex justify-center">
                <CustomerForm onFormSubmit={handleFormSubmit} />
            </div>
      </DialogContent>
    </Dialog>
  );
}