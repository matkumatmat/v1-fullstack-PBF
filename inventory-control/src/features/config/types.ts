// inventory-control/src/features/config/types.ts

// Ini adalah tipe data utama yang merepresentasikan satu item konfigurasi
// dari backend, lengkap dengan kemungkinan field tambahan.
export interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  // Ini memungkinkan objek memiliki properti lain dengan tipe apa pun.
  [key: string]: any;
}