// src/components/forms/add-branch-form.tsx

'use client';

import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, useFieldArray } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Loader2, PlusCircle, Trash2 } from 'lucide-react';

import { branchCreateForExistingCustomerSchema, BranchCreateForExistingCustomerPayload } from '@/lib/schemas/customer-schemas';
import { LocationFormFields } from './shared/location-form-fields'; // <-- IMPORT KOMPONEN BARU
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';

async function addBranchToCustomer({ customerId, payload }: { customerId: string; payload: BranchCreateForExistingCustomerPayload }) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const response = await fetch(`${apiUrl}/api/v1/customer/customers/${customerId}/branches`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error('Gagal menambahkan cabang baru.');
  return response.json();
}

const defaultLocation = {
  name: '', state_province: '', city: '', addr_line_1: '', addr_line_2: '',
  location_pic: '', location_pic_contact: '', delivery_instructions: '',
};

type AddBranchFormProps = { customerId: string; onSuccess: () => void; };

export function AddBranchForm({ customerId, onSuccess }: AddBranchFormProps) {
  const queryClient = useQueryClient();
  const form = useForm<z.infer<typeof branchCreateForExistingCustomerSchema>>({
    resolver: zodResolver(branchCreateForExistingCustomerSchema),
    defaultValues: {
      branch_data: { name: '', locations: [defaultLocation] }, // Gunakan default object
    },
  });

  const { fields, append, remove } = useFieldArray({ control: form.control, name: 'branch_data.locations' });

  const mutation = useMutation({
    mutationFn: addBranchToCustomer,
    onSuccess: () => {
      toast.success('Cabang baru berhasil ditambahkan!');
      queryClient.invalidateQueries({ queryKey: ['customerDetails', customerId] });
      onSuccess();
    },
    onError: (error: Error) => toast.error(error.message),
  });

  function onSubmit(values: BranchCreateForExistingCustomerPayload) {
    mutation.mutate({ customerId, payload: values });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField control={form.control} name="branch_data.name" render={({ field }) => (
          <FormItem><FormLabel className="text-lg font-semibold">Nama Cabang</FormLabel><FormControl><Input placeholder="e.g., Cabang Utama Jakarta" {...field} /></FormControl><FormMessage /></FormItem>
        )}/>
        <Separator />
        <div>
          <h3 className="text-md font-semibold mb-2">Lokasi Awal</h3>
          <div className="space-y-4">
            {fields.map((field, index) => (
              <div key={field.id} className="p-4 border rounded-md relative">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-sm">Lokasi #{index + 1}</h4>
                  {fields.length > 1 && <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2" onClick={() => remove(index)}><Trash2 className="h-4 w-4 text-destructive" /></Button>}
                </div>
                {/* REFACTOR: Ganti semua FormField lokasi dengan satu komponen ini */}
                <LocationFormFields control={form.control} basePath={`branch_data.locations.${index}.`} />
              </div>
            ))}
          </div>
          <Button type="button" variant="outline" size="sm" className="mt-4" onClick={() => append(defaultLocation)}>
            <PlusCircle className="mr-2 h-4 w-4" /> Tambah Lokasi Lain
          </Button>
        </div>
        <Button type="submit" disabled={mutation.isPending} className="w-full">{mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />} Simpan Cabang Baru</Button>
      </form>
    </Form>
  );
}