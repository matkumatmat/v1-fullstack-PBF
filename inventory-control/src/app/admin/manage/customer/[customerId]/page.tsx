// src/app/admin/manage/customer/[customerId]/page.tsx
// ^^ Lihat, path-nya sudah pakai huruf kecil

import { notFound } from 'next/navigation';
import { z } from 'zod';
import { Building, MapPin } from 'lucide-react';
import PageContainer from '@/components/layout/page-container';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CustomerActions, BranchActions } from './customer-detail-actions';

// Skema dan fungsi fetch ini sudah benar untuk halaman detail
const locationResponseSchema = z.object({
  public_id: z.string().uuid(), 
  name: z.string().nullable(), 
  city: z.string().nullable(),
  state_province: z.string().nullable(), 
  addr_line_1: z.string().nullable(),
  addr_line_2: z.string().nullable(), 
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
  customer_type: z.string(),
  branches: z.array(branchResponseSchema),
});

async function getCustomerDetails(customerId: string) {
  const apiUrl = process.env.API_URL;
  if (!apiUrl) throw new Error("Server configuration error: API_URL is not set.");
  
  const response = await fetch(`${apiUrl}/api/v1/customer/customers/${customerId}`, { cache: 'no-store' });
  
  if (!response.ok) {
    if (response.status === 404) {
      notFound();
    }
    throw new Error(`Failed to fetch customer details. Server responded with ${response.status}.`);
  }
  
  const jsonData = await response.json();
  return customerDetailResponseSchema.parse(jsonData);
}

// PERUBAHAN DI SINI 1: Ubah tipe props dari CustomerId menjadi customerId
type CustomerDetailPageProps = { params: { customerId: string } };

export default async function CustomerDetailPage({ params }: CustomerDetailPageProps) {
  // PERUBAHAN DI SINI 2: Gunakan params.customerId (c kecil)
  const customer = await getCustomerDetails(params.customerId);

  return (
    <PageContainer>
      <div className="w-full space-y-6">
        <Card>
          <CardHeader>
            <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
              <div>
                <CardTitle className="text-2xl">{customer.name}</CardTitle>
                <CardDescription>Detail lengkap untuk customer tipe: {customer.customer_type}</CardDescription>
              </div>
              <CustomerActions customerId={customer.public_id} />
            </div>
          </CardHeader>
        </Card>

        <h2 className="text-xl font-semibold">Cabang & Lokasi</h2>
        {customer.branches.length === 0 ? (
          <Card><CardContent className="pt-6 text-center text-muted-foreground">Customer ini belum memiliki cabang.</CardContent></Card>
        ) : (
          <div className="space-y-4">
            {customer.branches.map((branch) => (
              <Card key={branch.public_id}>
                <CardHeader>
                  <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
                    <CardTitle className="text-lg flex items-center gap-2"><Building className="h-5 w-5 text-primary" />{branch.name}</CardTitle>
                    <BranchActions branchId={branch.public_id} customerId={customer.public_id} />
                  </div>
                </CardHeader>
                <CardContent className="pl-6 sm:pl-12 space-y-2">
                  {branch.locations.length === 0 ? (
                    <p className="text-sm text-muted-foreground">Cabang ini belum memiliki lokasi.</p>
                  ) : (
                    branch.locations.map((location) => (
                      <div key={location.public_id} className="flex items-start gap-3 text-sm text-muted-foreground border-l-2 pl-4">
                        <MapPin className="h-4 w-4 mt-1 flex-shrink-0" />
                        <div className="flex flex-col">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-foreground">{location.name ?? 'Lokasi Tanpa Nama'}</span>
                            {location.is_default && <Badge variant="secondary">Default</Badge>}
                          </div>
                          <span>{location.addr_line_1}</span>
                          {location.addr_line_2 && <span>{location.addr_line_2}</span>}
                          <span>{location.city}, {location.state_province}</span>
                        </div>
                      </div>
                    ))
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </PageContainer>
  );
}