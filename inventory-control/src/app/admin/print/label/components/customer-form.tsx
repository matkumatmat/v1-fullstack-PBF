// app/main/labeling/components/customer-form.tsx
'use client';

import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { CustomerFormValues, customerFormSchema } from '@/constants/customer';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Trash, PlusCircle } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

// Nanti, data ini harusnya di-fetch dari API menggunakan TanStack Query
const dummyCustomerTypes = [
  { id: 'd1b2e3f4-a5b6-c7d8-e9f0-1a2b3c4d5e6f', name: 'Corporate' },
  { id: 'f6e5d4c3-b2a1-0987-6543-210fedcba987', name: 'Distributor' },
];
const dummySectorTypes = [
  { id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef', name: 'SWASTA' },
  { id: 'fedcba09-8765-4321-fedc-ba9876543210', name: 'PEMERINTAH' },
];

interface CustomerFormProps {
  onFormSubmit: (data: CustomerFormValues) => void;
}

export function CustomerForm({ onFormSubmit }: CustomerFormProps) {
  const form = useForm<CustomerFormValues>({
    resolver: zodResolver(customerFormSchema),
    defaultValues: {
      code: '',
      name: '',
      addresses: [],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'addresses',
  });

  const onSubmit = (data: CustomerFormValues) => {
    console.log('Data Form:', data);
    onFormSubmit(data); 
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 w-full max-w-2xl">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {/* Kode Customer */}
          <FormField
            control={form.control}
            name="code"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Kode Customer</FormLabel>
                <FormControl>
                  <Input placeholder="Contoh: KFTD" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Nama Customer */}
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (    
              <FormItem className='md:col-span-2'>
                <FormLabel>Nama Customer</FormLabel>
                <FormControl>
                  <Input placeholder="Contoh: PT Sejahtera Abadi" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Tipe Customer */}
          <FormField
            control={form.control}
            name="customer_type_public_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tipe Customer</FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Pilih tipe customer" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {dummyCustomerTypes.map((type) => (
                      <SelectItem key={type.id} value={type.id}>
                        {type.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* Tipe Sektor */}
          <FormField
            control={form.control}
            name="sector_type_public_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tipe Sektor</FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Pilih tipe sektor" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {dummySectorTypes.map((type) => (
                      <SelectItem key={type.id} value={type.id}>
                        {type.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <Separator />

        {/* Bagian Alamat Dinamis */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium">Alamat</h3>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() =>
                // VVV INI BAGIAN YANG DIPERBAIKI VVV
                append({
                  // Field yang sudah ada
                  address_name: '',
                  address_line1: '',
                  city: '',
                  is_default: fields.length === 0,

                  // Tambahkan field yang hilang sesuai error TypeScript
                  address_type: 'CUSTOMER', // Nilai default dari enum
                  is_active: true,          // Nilai default boolean
                  country: 'Indonesia',     // Nilai default string

                  // Field opsional lainnya bisa dikosongkan atau tidak disertakan
                  address_line2: '',
                  state_province: '',
                  postal_code: '',
                  contact_person: '',
                  contact_phone: '',
                  contact_email: '',
                })
              }
            >
              <PlusCircle className="mr-2 h-4 w-4" />
              Tambah Alamat
            </Button>
          </div>

          {fields.map((field, index) => (
            <div key={field.id} className="border p-2 rounded-md space-y-4 relative">
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2"
                onClick={() => remove(index)}
              >
                <Trash className="h-4 w-4 text-destructive" />
              </Button>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name={`addresses.${index}.address_name`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nama Alamat</FormLabel>
                      <FormControl>
                        <Input placeholder="Kantor Pusat, Gudang, dll." {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`addresses.${index}.address_line1`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Alamat Baris 1</FormLabel>
                      <FormControl>
                        <Input placeholder="Jl. Jenderal Sudirman No. 1" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`addresses.${index}.city`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Kota</FormLabel>
                      <FormControl>
                        <Input placeholder="Jakarta Selatan" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`addresses.${index}.is_default`}
                  render={({ field }) => (
                    <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4 md:col-span-2">
                      <FormControl>
                        <Checkbox checked={field.value} onCheckedChange={field.onChange} />
                      </FormControl>
                      <div className="space-y-1 leading-none">
                        <FormLabel>Jadikan Alamat Default</FormLabel>
                      </div>
                    </FormItem>
                  )}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-end">
          <Button type="submit">Simpan Customer</Button>
        </div>
      </form>
    </Form>
  );
}