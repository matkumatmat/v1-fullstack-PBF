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
import { CustomerOnboardForm } from './customer-onboard-form'; // Impor form baru kita

export function AddCustomerDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <PlusCircle className="mr-2 h-4 w-4" />
          Tambah Customer
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Onboarding Customer Baru</DialogTitle>
          <DialogDescription>
            Isi detail lengkap customer, termasuk informasi finansial dan cabang. Klik simpan jika sudah selesai.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          {/* Gunakan form baru dan berikan callback untuk menutup dialog */}
          <CustomerOnboardForm onSuccess={() => setOpen(false)} />
        </div>
      </DialogContent>
    </Dialog>
  );
}