// file: tanstack-table.d.ts

import '@tanstack/react-table';

declare module '@tanstack/react-table' {
  // Tambahkan properti apa pun yang Anda inginkan ke meta
  interface ColumnMeta<TData extends RowData, TValue> {
    className?: string;
  }
}