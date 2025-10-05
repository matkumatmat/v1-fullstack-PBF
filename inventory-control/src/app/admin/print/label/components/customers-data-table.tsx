'use client';

import * as React from 'react';
import { z } from 'zod';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getExpandedRowModel,
  getPaginationRowModel, // <-- PERBAIKAN 1: Ditambahkan kembali
  useReactTable,
} from '@tanstack/react-table';
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { ChevronDown, MoreHorizontal, Pencil, Trash } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AddCustomerDialog } from './add-customer-dialog';
import { Skeleton } from '@/components/ui/skeleton';
import { CustomerSubComponent } from './customer-sub-component';

// Skema Zod untuk API list
const customerResponseSchema = z.object({
  public_id: z.string().uuid(),
  name: z.string(),
  customer_type: z.enum(['PEMERINTAH', 'DISTRIBUTOR', 'RETAIL']),
  
});
const customersApiResponseSchema = z.array(customerResponseSchema);
type Customer = z.infer<typeof customerResponseSchema>;

// Fungsi fetch
const fetchCustomers = async (skip: number, limit: number): Promise<Customer[]> => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) throw new Error("FATAL: NEXT_PUBLIC_API_URL is not defined");
  const response = await fetch(`${apiUrl}/api/v1/customer/customers?skip=${skip}&limit=${limit}`);
  if (!response.ok) throw new Error('Gagal mengambil data customer.');
  const jsonData = await response.json();
  return customersApiResponseSchema.parse(jsonData);
};

// Definisi kolom di luar komponen untuk stabilitas referensi
const columns: ColumnDef<Customer>[] = [
  {
    id: 'expander',
    header: () => null,
    cell: ({ row }) => (
      <Button
        variant="ghost"
        size="icon"
        onClick={row.getToggleExpandedHandler()}
        disabled={!row.getCanExpand()}
        className="w-8 h-8"
      >
        <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${row.getIsExpanded() ? 'rotate-180' : ''}`} />
      </Button>
    ),
  },
  { accessorKey: 'name', header: 'Nama Customer' },
  { accessorKey: 'customer_type', header: 'Tipe' },
  {
    id: 'actions',
    cell: ({ row }) => (
      <div className="text-right">
        <DropdownMenu>
          <DropdownMenuTrigger asChild><Button variant="ghost" className="h-8 w-8 p-0"><MoreHorizontal className="h-4 w-4" /></Button></DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Aksi</DropdownMenuLabel>
            <DropdownMenuItem onClick={() => navigator.clipboard.writeText(row.original.public_id)}>Salin ID</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem><Pencil className="mr-2 h-4 w-4" /> Edit</DropdownMenuItem>
            <DropdownMenuItem className="text-destructive focus:text-destructive focus:bg-destructive/10"><Trash className="mr-2 h-4 w-4" /> Hapus</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    ),
  },
];

export function CustomersDataTable() {
  const [pagination, setPagination] = React.useState({ pageIndex: 0, pageSize: 10 });
  const [expanded, setExpanded] = React.useState({});

  const { data: queryData, isLoading } = useQuery({
    queryKey: ['customers', pagination.pageIndex, pagination.pageSize],
    queryFn: () => fetchCustomers(pagination.pageIndex * pagination.pageSize, pagination.pageSize),
    placeholderData: keepPreviousData,
  });

  // PERBAIKAN 2: Pola yang lebih aman untuk menangani data 'undefined'
  const tableData = queryData ?? [];
  const hasMoreData = tableData.length === pagination.pageSize;

  const table = useReactTable({
    data: tableData,
    columns,
    state: { pagination, expanded },
    onPaginationChange: setPagination,
    onExpandedChange: setExpanded,
    getRowCanExpand: () => true,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(), // <-- Sekarang berfungsi
    getExpandedRowModel: getExpandedRowModel(),
    manualPagination: true,
  });

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
          <div>
            <CardTitle>Manajemen Customer</CardTitle>
            <CardDescription>Kelola semua data customer, cabang, dan lokasi di database.</CardDescription>
          </div>
          <div className="mt-4 sm:mt-0"><AddCustomerDialog /></div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <TableHead key={header.id} style={{ width: header.getSize() !== 150 ? header.getSize() : undefined }}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
                    </TableHead>
                  ))}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={`skeleton-${i}`}><TableCell colSpan={columns.length}><Skeleton className="h-10 w-full" /></TableCell></TableRow>
                ))
              ) : table.getRowModel().rows?.length ? (
                table.getRowModel().rows.map((row) => (
                  <React.Fragment key={row.id}>
                    <TableRow data-state={row.getIsExpanded() && "selected"}>
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                      ))}
                    </TableRow>
                    {row.getIsExpanded() && (
                      <TableRow>
                        <TableCell colSpan={columns.length}>
                          <CustomerSubComponent customerId={row.original.public_id} />
                        </TableCell>
                      </TableRow>
                    )}
                  </React.Fragment>
                ))
              ) : (
                <TableRow><TableCell colSpan={columns.length} className="h-24 text-center">Tidak ada data ditemukan.</TableCell></TableRow>
              )}
            </TableBody>
          </Table>
        </div>
        <div className="flex items-center justify-end space-x-2 py-4">
          <div className="flex-1 text-sm text-muted-foreground">Halaman {table.getState().pagination.pageIndex + 1}</div>
          <Button variant="outline" size="sm" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>Sebelumnya</Button>
          <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!hasMoreData}>Selanjutnya</Button>
        </div>
      </CardContent>
    </Card>
  );
}