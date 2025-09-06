// inventory-control/src/features/config/types.ts

/**
 * Tipe data utama yang merepresentasikan satu item konfigurasi dari backend.
 * '[key: string]: any;' memungkinkan objek ini memiliki properti tambahan apa pun,
 * yang membuatnya fleksibel untuk berbagai skema data.
 */
export interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  [key: string]: any;
}