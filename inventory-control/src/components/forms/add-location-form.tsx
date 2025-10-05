// src/components/forms/add-location-form.tsx (INI YANG BENAR)

'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';

import { locationCreateSchema, LocationCreatePayload } from '@/lib/schemas/customer-schemas';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { LocationFormFields } from './shared/location-form-fields';

async function addLocationToBranch({ branchId, payload }: { branchId: string; payload: LocationCreatePayload }) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const response = await fetch(`${apiUrl}/api/v1/customer/customers/branches/${branchId}/locations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error('Gagal menambahkan lokasi baru.');
  return response.json();
}

type AddLocationFormProps = { branchId: string; customerId: string; onSuccess: () => void; };

export function AddLocationForm({ branchId, customerId, onSuccess }: AddLocationFormProps) {
  const queryClient = useQueryClient();
  const form = useForm<LocationCreatePayload>({
    resolver: zodResolver(locationCreateSchema),
    defaultValues: {
      name: '',
      state_province: '',
      city: '',
      addr_line_1: '',
      addr_line_2: '',
      addr_line_3: '',
      location_pic: '',
      location_pic_contact: '',
      delivery_instructions: '',
      is_default: false,
      is_active: true,
      country: 'Indonesia',
      minimal_order_value: 0,
      location_type: '',
      postal_code: '',
    },
  });

  const mutation = useMutation({
    mutationFn: addLocationToBranch,
    onSuccess: () => {
      toast.success('Lokasi baru berhasil ditambahkan!');
      queryClient.invalidateQueries({ queryKey: ['customerDetails', customerId] });
      onSuccess();
    },
    onError: (error: Error) => toast.error(error.message),
  });

  function onSubmit(values: LocationCreatePayload) {
    mutation.mutate({ branchId, payload: values });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 max-h-[70vh] overflow-y-auto p-1">
        <LocationFormFields control={form.control} basePath="" />
        
        <Button type="submit" disabled={mutation.isPending} className="w-full !mt-6">
          {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Simpan Lokasi
        </Button>
      </form>
    </Form>
  );
}