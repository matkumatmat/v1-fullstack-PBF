// src/app/admin/manage/customer/page.tsx

import Link from 'next/link';
import { z } from 'zod';
import { Building, PlusCircle } from 'lucide-react';

import PageContainer from '@/components/layout/page-container';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

// 1. Skema untuk satu item dalam daftar (lebih ringan dari skema detail)
const customerListItemSchema = z.object({
  public_id: z.string().uuid(),
  name: z.string(),
  customer_type: z.string(),
});

// Skema untuk respons API daftar customer
const customerListResponseSchema = z.array(customerListItemSchema);

// 2. Fungsi untuk mengambil SEMUA customer
async function getCustomers() {
  const apiUrl = process.env.API_URL;
  if (!apiUrl) {
    throw new Error("Server configuration error: API_URL is not set.");
  }
  
  // Asumsi endpoint untuk mengambil daftar customer
  const response = await fetch(`${apiUrl}/api/v1/customer/customers`, {
    cache: 'no-store', // Data customer bisa sering berubah
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch customers. Server responded with ${response.status}.`);
  }
  
  const jsonData = await response.json();
  return customerListResponseSchema.parse(jsonData);
}

export default async function CustomerListPage() {
  const customers = await getCustomers();

  return (
    <PageContainer>
      <div className="w-full space-y-6">
        {/* Header Halaman */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Manajemen Customer</h1>
            <p className="text-muted-foreground">
              Pilih customer untuk melihat detail cabang dan lokasi.
            </p>
          </div>
          <Button>
            <PlusCircle className="mr-2 h-4 w-4" />
            Tambah Customer
          </Button>
        </div>

        {/* Grid Responsif untuk Kartu Customer */}
        {customers.length === 0 ? (
          <Card>
            <CardContent className="pt-6 text-center text-muted-foreground">
              Belum ada data customer.
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {customers.map((customer) => (
              <Link 
                key={customer.public_id} 
                href={`/admin/manage/customer/${customer.public_id}`}
                className="block"
              >
                <Card className="h-full hover:shadow-lg hover:-translate-y-1 transition-all duration-200 ease-in-out">
                  {/* Placeholder untuk Gambar */}
                  <div className="aspect-video w-full bg-muted flex items-center justify-center">
                    <Building className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <CardHeader>
                    <h3 className="font-semibold text-lg truncate" title={customer.name}>
                      {customer.name}
                    </h3>
                    <Badge variant="secondary">{customer.customer_type}</Badge>
                  </CardHeader>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </PageContainer>
  );
}