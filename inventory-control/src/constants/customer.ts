// app/main/labeling/components/schemas.ts

import { z } from 'zod';

// Skema ini mencerminkan Pydantic `_CustomerAddressCore`
export const addressSchema = z.object({
  address_name: z.string().min(1, 'Nama alamat tidak boleh kosong.'),
  address_type: z.enum(['CUSTOMER', 'WAREHOUSE', 'OTHER']).default('CUSTOMER'), // Sesuaikan dengan AddressTypeEnum Anda
  address_line1: z.string().min(1, 'Baris alamat 1 tidak boleh kosong.'),
  address_line2: z.string().optional(),
  city: z.string().min(1, 'Kota tidak boleh kosong.'),
  state_province: z.string().optional(),
  postal_code: z.string().optional(),
  country: z.string().default('Indonesia'),
  contact_person: z.string().optional(),
  contact_phone: z.string().optional(),
  contact_email: z.string().email('Email tidak valid.').optional().or(z.literal('')),
  is_active: z.boolean().default(true),
  is_default: z.boolean().default(false),
});

// Skema ini mencerminkan Pydantic `CustomerFePl`
export const customerFormSchema = z.object({
  code: z.string().min(1, 'Kode customer tidak boleh kosong.'),
  name: z.string().min(1, 'Nama customer tidak boleh kosong.'),
  // Kita gunakan string untuk ID, karena di form biasanya berupa value dari <select>
  customer_type_public_id: z.string().uuid('ID Tipe Customer tidak valid.'),
  sector_type_public_id: z.string().uuid('ID Tipe Sektor tidak valid.'),
  addresses: z.array(addressSchema).optional(),
});

export type CustomerFormValues = z.infer<typeof customerFormSchema>;