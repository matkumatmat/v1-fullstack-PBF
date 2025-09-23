'use client'

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ChevronDown, Pencil, PlusCircle, Trash } from 'lucide-react';
import { AddressComboBox } from './address-combo-box';
import type { Customer, Address } from '../types';
import { dummyCustomers } from '../dummy-data-address';

export default function AddressManagementSection() {
  const [customers, setCustomers] = useState<Customer[]>(dummyCustomers);
  const [openCollapsible, setOpenCollapsible] = useState<string | null>(null);

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Manajemen Alamat</h1>
          <p className="text-slate-400 mt-1">Kelola semua data tujuan di database.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button>
            <PlusCircle className="mr-2 h-4 w-4" />
            Tambah Customer
          </Button>
        </div>
      </div>
      <Card className="mt-4">
        <CardContent>
          <AddressComboBox/>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[37%] text-lg font-bold">Nama Customer</TableHead>
                <TableHead className='w-[20%] font-bold text-lg'>Sektor</TableHead>
                <TableHead className='w-[20%] font-bold text-lg'>Provinsi</TableHead>
                <TableHead className='w-[20%] font-bold text-lg'>Kota</TableHead>
                <TableHead className='w-[30%] font-bold text-lg'>Jumlah Alamat</TableHead>
                <TableHead className=""></TableHead> {/* Kolom untuk tombol expand */}
              </TableRow>
            </TableHeader>
            <TableBody>
              {customers.map((customer) => (
                <Collapsible asChild key={customer.uuid} open={openCollapsible === customer.uuid} onOpenChange={() => setOpenCollapsible(prev => prev === customer.uuid ? null : customer.uuid)}>
                  <>
                    {/* Baris utama Customer yang bisa di-klik */}
                    <TableRow className="cursor-pointer">
                      <TableCell className="font-medium">{customer.customer}</TableCell>
                      <TableCell>{customer.customer_sector_type}</TableCell>
                      <TableCell>{customer.customer_addresses.find(address => address.is_default)?.state_province}</TableCell>
                      <TableCell>{customer.customer_addresses.find(address => address.is_default)?.city}</TableCell>
                      <TableCell>{customer.customer_addresses.length} alamat</TableCell>
                      <TableCell>
                        <CollapsibleTrigger asChild>
                          <Button variant="ghost" size="icon">
                            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${openCollapsible === customer.uuid ? 'rotate-180' : ''}`} />
                          </Button>
                        </CollapsibleTrigger>
                      </TableCell>                      
                    </TableRow>

                    {/* Konten yang muncul saat di-expand */}
                    <CollapsibleContent asChild>
                      <TableRow>
                        <TableCell colSpan={5} className="p-0">
                          <div className="bg-slate-900/50 p-4">
                            <h4 className="font-semibold mb-3 ml-2">Detail Alamat:</h4>
                            <div className="space-y-4">
                              {customer.customer_addresses.map(address => (
                                <AddressCard key={address.uuid} address={address} />
                              ))}
                            </div>
                          </div>
                        </TableCell>
                      </TableRow>
                    </CollapsibleContent>
                  </>
                </Collapsible>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

// Komponen kecil untuk menampilkan detail satu alamat
function AddressCard({ address }: { address: Address }) {
  return (
    <div className="border border-slate-700 rounded-lg p-4 flex justify-between items-start">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <p className="font-semibold">{address.addresses_type}</p>
          {address.is_default && <Badge>Default</Badge>}
        </div>
        <p className="text-sm text-muted-foreground">
          {address.addresses_line1}, {address.addresses_line2 ? `${address.addresses_line2}, ` : ''}
          {address.city}, {address.state_province} {address.postal_code}
        </p>
        <p className="text-sm text-muted-foreground mt-1">
          Kontak: {address.contact_person} ({address.contact_phone})
        </p>
      </div>
      <div className="flex gap-2">
        <Button variant="outline" size="icon" className="group">
          <Pencil className="h-4 w-4 text-slate-400 group-hover:text-primary" />
        </Button>
        <Button variant="outline" size="icon" className="group">
          <Trash className="h-4 w-4 text-slate-400 group-hover:text-destructive" />
        </Button>
      </div>
    </div>
  )
}