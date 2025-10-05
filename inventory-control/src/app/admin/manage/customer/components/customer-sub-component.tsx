'use client';

import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';
import { AlertCircle, Building, MapPin, PlusCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

// Skema Zod untuk memvalidasi respons detail dari API
const locationResponseSchema = z.object({
  public_id: z.string().uuid(),
  name: z.string().nullable(),
  city: z.string().nullable(),
  state_province: z.string().nullable(),
  addr_line_1: z.string().nullable(),
  addr_line_2: z.string().nullable(),
  addr_line_3: z.string().nullable(),
  is_default: z.boolean(),
});

const branchResponseSchema = z.object({
  public_id: z.string().uuid(),
  name: z.string(),
  locations: z.array(locationResponseSchema),
});

const customerDetailResponseSchema = z.object({
  public_id: z.string().uuid(),
  name: z.string(),
  branches: z.array(branchResponseSchema),
});

type CustomerDetail = z.infer<typeof customerDetailResponseSchema>;

// Fungsi untuk mengambil detail customer
async function fetchCustomerDetails(customerId: string): Promise<CustomerDetail> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const response = await fetch(`${apiUrl}/api/v1/customer/customers/${customerId}`);
  if (!response.ok) {
    throw new Error('Gagal mengambil detail customer.');
  }
  const jsonData = await response.json();
  return customerDetailResponseSchema.parse(jsonData);
}

interface CustomerSubComponentProps {
  customerId: string;
}

export function CustomerSubComponent({ customerId }: CustomerSubComponentProps) {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['customer-detail', customerId],
    queryFn: () => fetchCustomerDetails(customerId),
    staleTime: 5 * 60 * 1000, // Cache data detail selama 5 menit
  });

  if (isLoading) {
    return (
      <div className="p-4 space-y-4"><Skeleton className="h-8 w-1/3" /><Skeleton className="h-24 w-full" /></div>
    );
  }

  if (isError) {
    return (
      <div className="p-4 text-destructive flex items-center gap-2"><AlertCircle className="h-5 w-5" /><span>Error: {error.message}</span></div>
    );
  }

  if (!data) {
    return (
      <div className="p-4 text-muted-foreground flex items-center gap-2"><AlertCircle className="h-5 w-5" /><span>Data tidak tersedia.</span></div>
    );
  }

  return (
    <div className="p-4 bg-background/30">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg">Detail Cabang & Lokasi</CardTitle>
          <Button variant="outline" size="sm"><PlusCircle className="mr-2 h-4 w-4" />Tambah Cabang Baru</Button>
        </CardHeader>
        <CardContent className="space-y-4">
          {data.branches.length === 0 ? (
            <p className="text-muted-foreground text-sm">Customer ini belum memiliki cabang.</p>
          ) : (
            data.branches.map((branch) => (
              <div key={branch.public_id} className="p-3 border rounded-md">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold flex items-center gap-2"><Building className="h-4 w-4 text-primary" />{branch.name}</h4>
                  <Button variant="ghost" size="sm"><PlusCircle className="mr-2 h-4 w-4" />Tambah Lokasi</Button>
                </div>
                <div className="pl-6 space-y-2">
                  {branch.locations.map((location) => (
                    <div key={location.public_id} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <MapPin className="h-3 w-3 mt-1 flex-shrink-0" />
                      <div className="flex flex-col">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-foreground">{location.name}</span>
                          {location.is_default && <Badge variant="secondary">Default</Badge>}
                        </div>
                        <span>{location.addr_line_1}</span>
                        {location.addr_line_2 && <span>{location.addr_line_2}</span>}
                        <span>{location.city}, {location.state_province}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
}