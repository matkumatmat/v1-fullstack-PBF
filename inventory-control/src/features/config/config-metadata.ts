// inventory-control/src/features/config/config-metadata.ts
import { z } from 'zod';

// Mendefinisikan struktur untuk setiap field kustom
export interface FieldConfig {
  key: string;
  label: string;
  type: 'text' | 'number' | 'textarea'; // Bisa diperluas nanti
  validation: z.ZodTypeAny;
}

// Objek utama yang menjadi "kamus" untuk semua tipe konfigurasi
export const configMetadata: Record<string, FieldConfig[]> = {
  status_type: [
    { key: 'color', label: 'Color', type: 'text', validation: z.string().min(1, 'Color is required') },
  ],
  priority_level: [
    { key: 'level', label: 'Level', type: 'number', validation: z.coerce.number().min(1, 'Level must be at least 1') },
  ],
  packaging_material: [
    { key: 'stock', label: 'Stock', type: 'number', validation: z.coerce.number().default(0) },
    { key: 'unit', label: 'Unit', type: 'text', validation: z.string().min(1, 'Unit is required') },
  ],
  temperature_type: [
    { key: 'min_temp', label: 'Min Temperature', type: 'number', validation: z.coerce.number() },
    { key: 'max_temp', label: 'Max Temperature', type: 'number', validation: z.coerce.number() },
  ],
  // Tipe yang tidak punya field tambahan, biarkan array kosong
  document_type: [],
  allocation_type: [],
  customer_type: [],
  delivery_type: [],
  location_type: [],
  movement_type: [],
  notification_type: [],
  package_type: [],
  packaging_box_type: [],
  product_price: [],
  product_type: [],
  sector_type: [],
  // Fallback jika tipe tidak ditemukan
  default: [],
};