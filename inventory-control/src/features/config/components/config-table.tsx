// Fixed Config Table - Now compatible with your DataTable component
// inventory-control/src/features/config/components/config-table.tsx
'use client';

import { Button } from '@/components/ui/button';
import { DataTable } from '@/components/ui/table/data-table';
import { DataTableToolbar } from '@/components/ui/table/data-table-toolbar';
import { ColumnDef } from '@tanstack/react-table';
import { 
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues
} from '@tanstack/react-table';
import { useMemo } from 'react';
import { ConfigFormDialog } from './config-form-dialog';

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

export function ConfigTable({ data, onSave, onDelete, isLoading = false }: ConfigTableProps) {
  const columns = useMemo<ColumnDef<ConfigItem>[]>(
    () => [
      {
        accessorKey: 'code',
        header: 'Code',
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
        meta: {
          label: 'Name',
          variant: 'text',
          placeholder: 'Search by name...'
        }
      },
      {
        accessorKey: 'description',
        header: 'Description',
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
        cell: ({ row }) => {
          const item = row.original;
          return (
            <div className='flex space-x-2'>
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
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  });

  return (
    <DataTable table={table}>
      <DataTableToolbar table={table} />
    </DataTable>
  );
}