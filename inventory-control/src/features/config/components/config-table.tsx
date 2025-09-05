// inventory-control/src/features/config/components/config-table.tsx
'use client';

import { useMemo } from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  useReactTable,
} from '@tanstack/react-table';

// 1. Import komponen tabel dari shadcn/ui
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { Button } from '@/components/ui/button';
import { DataTableToolbar } from '@/components/ui/table/data-table-toolbar';
import { DataTablePagination } from '@/components/ui/table/data-table-pagination';
import { ConfigFormDialog } from './config-form-dialog';
import { Card, CardContent } from '@/components/ui/card';

// --- Interface tidak berubah ---
interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
}

interface ConfigTableProps {
  data: ConfigItem[];
  onSave: (data: any) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  isLoading?: boolean;
}

// --- Logika komponen tetap sama ---
export function ConfigTable({ data, onSave, onDelete, isLoading = false }: ConfigTableProps) {
  const columns = useMemo<ColumnDef<ConfigItem>[]>(
    () => [
      {
        accessorKey: 'code',
        header: 'Code',
        size:6,
        cell: ({ row }) => (
          <span className="font-mono text-sm">{row.getValue('code')}</span>
        ),
        meta: {
          label: 'Code',
          variant: 'text',
          placeholder: 'Search by code...'
        }
      },
      {
        accessorKey: 'name',  
        header: 'Name',
        size : 10,
        cell: ({ row }) => <div>{row.getValue('name')}</div>,
        meta: {
          label: 'Name',
          variant: 'text', 
          placeholder: 'Search by name...'
        }
      },
      {
        accessorKey: 'description',
        header: 'Description', 
        size : 100,
        cell: ({ row }) => {
          const description = row.getValue('description') as string;
          return (
            <span className="text-muted-foreground">
              {description || 'No description'}
            </span>
          );
        },
        meta: {
          label: 'Description',
          variant: 'text',
          placeholder: 'Search by description...'
        }
      },
      {
        id: 'actions',
        header: 'Actions',
        size : 20,
        cell: ({ row }) => {
          const item = row.original;
          return (
            <div className='flex space-x-2 justify-center'>
              <ConfigFormDialog 
                onSave={onSave} 
                item={item} 
                isLoading={isLoading}
              />
              <Button 
                variant='destructive' 
                size='sm'
                onClick={() => onDelete(item.id)}
                disabled={isLoading}
              >
                Delete
              </Button>
            </div>
          );
        },
        enableSorting: false,
        enableHiding: false
      }
    ],
    [onSave, onDelete, isLoading]
  );

  const table = useReactTable({
    data: data || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(), 
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
  });

  // 2. Ganti bagian return dengan struktur tabel eksplisit
  return (
    <div className="space-y-4 w-full">
      <DataTableToolbar table={table} />
      <Card>
        <CardContent className="p-0">
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => {
                      return (
                        <TableHead key={header.id}>
                          {header.isPlaceholder
                            ? null
                            : flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                              )}
                        </TableHead>
                      );
                    })}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {table.getRowModel().rows?.length ? (
                  table.getRowModel().rows.map((row) => (
                    <TableRow
                      key={row.id}
                      data-state={row.getIsSelected() && "selected"}
                    >
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id}>
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell
                      colSpan={columns.length}
                      className="h-24 text-center"
                    >
                      No results.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
      <DataTablePagination table={table} />
    </div>
  );
}