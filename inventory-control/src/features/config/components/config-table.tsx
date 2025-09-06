'use client';

import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useMemo } from 'react';
import { ConfigFormDialog } from './config-form-dialog';
import { toast } from 'sonner';
import { getMetadataForType } from '../config-metadata';

interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  [key: string]: any;
}

interface ConfigTableProps {
  data: ConfigItem[];
  selectedType: string;
  onSave: (data: any) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  isLoading?: boolean;
}

export function ConfigTable({
  data,
  selectedType,
  onSave,
  onDelete,
  isLoading = false,
}: ConfigTableProps) {
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await onDelete(id);
        toast.success('Item deleted successfully!');
      } catch (error) {
        toast.error('Failed to delete item.');
        console.error('Delete error:', error);
      }
    }
  };

  const columns = useMemo<ColumnDef<ConfigItem>[]>(() => {
    // Kolom dasar yang selalu ada
    const baseColumns: ColumnDef<ConfigItem>[] = [
      {
        accessorKey: 'code',
        header: 'Code',
        cell: info => <span className="font-mono">{info.getValue<string>()}</span>,
        // DIUBAH: Menambahkan metadata untuk styling lebar kolom
        meta: {
          className: 'px-2 w-[30px]',
        },
      },
      {
        accessorKey: 'name',
        header: 'Name',
      },
      {
        accessorKey: 'description',
        header: 'Description',
        cell: info => <span className="text-sm text-muted-foreground">{info.getValue<string>() || '-'}</span>,
      },
    ];

    // Dapatkan field tambahan dari metadata
    const additionalFields = getMetadataForType(selectedType);

    const dynamicColumns: ColumnDef<ConfigItem>[] = additionalFields.map(field => ({
      accessorKey: field.key,
      header: field.label,
      cell: ({ row }) => {
        const value = row.getValue(field.key);
        if (field.type === 'boolean') {
          return value ? 'Yes' : 'No';
        }
        // Tampilkan '-' jika nilai null atau undefined
        return <span>{value !== null && value !== undefined ? String(value) : '-'}</span>;
      },
    }));

    // Kolom aksi
    const actionColumn: ColumnDef<ConfigItem> = {
      id: 'actions',
      header: 'Actions',
      cell: ({ row }) => {
        const item = row.original;
        return (
          <div className="flex space-x-1 justify-center">
            <ConfigFormDialog
              onSave={onSave}
              item={item}
              isLoading={isLoading}
              selectedType={selectedType}
            />
            <Button
              variant="destructive"
              size="sm"
              onClick={() => handleDelete(item.id)}
              disabled={isLoading}
            >
              Delete
            </Button>
          </div>
        );
      },
      // DIUBAH: Menambahkan metadata untuk styling lebar dan perataan kolom
      meta: {
        className: 'flex-wrap w-[80px] text-center',
      },
    };

    return [...baseColumns, ...dynamicColumns, actionColumn];
  }, [onSave, onDelete, isLoading, selectedType, data]);


  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map(headerGroup => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                // DIUBAH: Menerapkan className dari metadata ke header
                <TableHead key={header.id} className={header.column.columnDef.meta?.className}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map(row => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && 'selected'}
              >
                {row.getVisibleCells().map(cell => (
                  // DIUBAH: Menerapkan className dari metadata ke sel
                  <TableCell key={cell.id} className={cell.column.columnDef.meta?.className}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                {isLoading ? 'Loading data...' : 'No results.'}
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}