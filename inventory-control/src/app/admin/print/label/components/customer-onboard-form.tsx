'use client';

import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Loader2, PlusCircle, Trash } from 'lucide-react';

import { customerOnboardSchema, CustomerOnboardPayload } from '@/lib/schemas/customer-onboard';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';

// Fungsi untuk mengirim data ke API
// Ganti URL dengan endpoint API Anda yang sebenarnya
async function onboardCustomer(payload: CustomerOnboardPayload) {
  const response = await fetch('/api/v1/customer/customers/onboard', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    // Coba parse error dari body jika ada
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Gagal menambahkan customer baru.');
  }

  return response.json();
}

interface CustomerOnboardFormProps {
  onSuccess?: () => void; // Callback untuk menutup dialog/sheet setelah berhasil
}

export function CustomerOnboardForm({ onSuccess }: CustomerOnboardFormProps) {
  const queryClient = useQueryClient();

  const form = useForm<CustomerOnboardPayload>({
    resolver: zodResolver(customerOnboardSchema),
    defaultValues: {
      name: '',
      customer_type: 'DISTRIBUTOR',
      details: { npwp: '', bank: '', rekening: '' },
      specification: { default_credit_limit: 0, default_payment_terms_days: 30 },
      branches: [],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'branches',
  });

  const mutation = useMutation({
    mutationFn: onboardCustomer,
    onSuccess: () => {
      toast.success('Customer baru berhasil ditambahkan!');
      // Invalidate query 'customers' agar data table di-refresh otomatis
      queryClient.invalidateQueries({ queryKey: ['customers'] });
      onSuccess?.(); // Panggil callback jika ada
      form.reset(); // Reset form setelah berhasil
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const onSubmit = (data: CustomerOnboardPayload) => {
    console.log('Submitting data:', data);
    mutation.mutate(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Bagian Detail Customer */}
        <div className="p-4 border rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Informasi Customer</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField control={form.control} name="name" render={({ field }) => (
              <FormItem>
                <FormLabel>Nama Customer</FormLabel>
                <FormControl><Input placeholder="PT. Sukses Selalu" {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
            <FormField control={form.control} name="customer_type" render={({ field }) => (
              <FormItem>
                <FormLabel>Tipe Customer</FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl><SelectTrigger><SelectValue placeholder="Pilih tipe" /></SelectTrigger></FormControl>
                  <SelectContent>
                    <SelectItem value="PEMERINTAH">Pemerintah</SelectItem>
                    <SelectItem value="DISTRIBUTOR">Distributor</SelectItem>
                    <SelectItem value="RETAIL">Retail</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )} />
          </div>
        </div>

        {/* Bagian Detail Finansial & Spesifikasi */}
        <div className="p-4 border rounded-lg">
          <h3 className="text-lg font-semibold mb-4">Detail Finansial & Spesifikasi</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <FormField control={form.control} name="details.npwp" render={({ field }) => (
              <FormItem>
                <FormLabel>NPWP</FormLabel>
                <FormControl><Input placeholder="Nomor NPWP" {...field} value={field.value ?? ''} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
            <FormField control={form.control} name="details.bank" render={({ field }) => (
              <FormItem>
                <FormLabel>Bank</FormLabel>
                <FormControl><Input placeholder="Nama Bank" {...field} value={field.value ?? ''} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
            <FormField control={form.control} name="details.rekening" render={({ field }) => (
              <FormItem>
                <FormLabel>No. Rekening</FormLabel>
                <FormControl><Input placeholder="Nomor Rekening" {...field} value={field.value ?? ''} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
             <FormField control={form.control} name="specification.default_payment_terms_days" render={({ field }) => (
              <FormItem>
                <FormLabel>Termin Pembayaran (Hari)</FormLabel>
                <FormControl><Input type="number" {...field} onChange={e => field.onChange(parseInt(e.target.value, 10))} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
          </div>
        </div>

        <Separator />

        {/* Bagian Cabang Dinamis */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium">Cabang (Branches)</h3>
            <Button type="button" variant="outline" size="sm" onClick={() => append({ name: '', locations: [{ name: '', state_province: '', city: '', addr_line_1: '' }] })}>
              <PlusCircle className="mr-2 h-4 w-4" /> Tambah Cabang
            </Button>
          </div>

          {fields.map((field, index) => (
            <div key={field.id} className="border p-4 rounded-md space-y-4 relative bg-muted/20">
              <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2" onClick={() => remove(index)}>
                <Trash className="h-4 w-4 text-destructive" />
              </Button>
              <FormField control={form.control} name={`branches.${index}.name`} render={({ field }) => (
                <FormItem>
                  <FormLabel>Nama Cabang #{index + 1}</FormLabel>
                  <FormControl><Input placeholder="Contoh: Cabang Jakarta" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              {/* Di sini kita bisa menambahkan field array lagi untuk 'locations' jika diperlukan */}
              <p className="text-sm text-muted-foreground">Detail lokasi untuk cabang ini bisa ditambahkan di sini.</p>
            </div>
          ))}
        </div>

        <div className="flex justify-end">
          <Button type="submit" disabled={mutation.isPending}>
            {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Simpan Customer
          </Button>
        </div>
      </form>
    </Form>
  );
}