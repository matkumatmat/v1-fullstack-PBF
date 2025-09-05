'use client';

import { Button } from '@/components/ui/button';
import { DataTable } from '@/components/ui/table/data-table';
import { ColumnDef } from '@tanstack/react-table';
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
  onSave: (data: any) => void;
  onDelete: (id: number) => void;
}

export function ConfigTable({ data, onSave, onDelete }: ConfigTableProps) {
  const columns = useMemo<ColumnDef<ConfigItem>[]>(
    () => [
      {
        accessorKey: 'code',
        header: 'Code'
      },
      {
        accessorKey: 'name',
        header: 'Name'
      },
      {
        accessorKey: 'description',
        header: 'Description'
      },
      {
        id: 'actions',
        cell: ({ row }) => {
          const item = row.original;
          return (
            <div className='space-x-2'>
              <ConfigFormDialog onSave={onSave} item={item} />
              <Button variant='destructive' onClick={() => onDelete(item.id)}>
                Delete
              </Button>
            </div>
          );
        }
      }
    ],
    [onSave, onDelete]
  );

  return <DataTable<ConfigItem> columns={columns} data={data} />;
}
