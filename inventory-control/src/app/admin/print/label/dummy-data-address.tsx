import type { Customer, Address, AdressesPayload } from './types'; 

const address1: Address = {
  uuid: 'addr-uuid-001',
  addresses_type: 'Kantor Pusat',
  addresses_line1: 'Jl. Jenderal Sudirman Kav. 52-53',
  addresses_line2: 'Gedung Artha Graha, Lantai 25',
  city: 'Jakarta Selatan',
  state_province: 'DKI Jakarta',
  postal_code: '12190',
  country: 'Indonesia',
  contact_person: 'Budi Santoso',
  contact_phone: '081234567890',
  contact_email: 'budi.s@sejahtera-abadi.com',
  delivery_instructions: 'Serahkan ke resepsionis, sebutkan untuk Divisi Logistik.',
  special_requirements: 'Perlu akses lift barang.',
  latitude: -6.2249,
  longitude: 106.8094,
  is_active: true,
  is_default: true,
};

const address2: Address = {
  uuid: 'addr-uuid-002',
  addresses_type: 'Gudang',
  addresses_line1: 'Kawasan Industri MM2100',
  addresses_line2: 'Blok C-17, Jl. Kalimantan',
  city: 'Cikarang Barat',
  state_province: 'Jawa Barat',
  postal_code: '17530',
  country: 'Indonesia',
  contact_person: 'Agus Wijaya',
  contact_phone: '087712345678',
  contact_email: 'gudang.cikarang@sejahtera-abadi.com',
  delivery_instructions: 'Masuk dari Pintu 3, lapor ke pos satpam.',
  special_requirements: 'Hanya menerima barang pukul 08:00 - 15:00.',
  latitude: -6.3475,
  longitude: 107.0396,
  is_active: true,
  is_default: false,
};

const address3: Address = {
  uuid: 'addr-uuid-003',
  addresses_type: 'Pabrik',
  addresses_line1: 'Jl. Rungkut Industri Raya No. 10',
  addresses_line2: '',
  city: 'Surabaya',
  state_province: 'Jawa Timur',
  postal_code: '60293',
  country: 'Indonesia',
  contact_person: 'Siti Aminah',
  contact_phone: '085698765432',
  contact_email: 'purchasing@nusantara-karya.co.id',
  delivery_instructions: 'Timbang dulu di jembatan timbang sebelum bongkar muat.',
  special_requirements: '-',
  latitude: -7.3297,
  longitude:112.7686,
  is_active: true,
  is_default: true,
};

const customer1: Customer = {
  uuid: 'cust-uuid-111',
  customer: 'KFTD - BANDUNG',
  customer_type: 'Corporate',
  customer_sector_type: 'SWASTA',
  customer_addresses: [address1, address2], 
};

const customer2: Customer = {
  uuid: 'cust-uuid-222',
  customer: 'PPI - BANDUNG',
  customer_type: 'Corporate',
  customer_sector_type: 'SWASTA',
  customer_addresses: [address3], 
};

export const dummyCustomers: Customer[] = [
  customer1,
  customer2,
  customer1,
  customer2,
];


// --- LANGKAH 3: Buat contoh data untuk AdressesPayload ---
// Ini adalah format data jika kamu mau mengirimkan daftar alamat BARU
// untuk customer yang sudah ada (misalnya customer1).
export const dummyAddressesPayload: AdressesPayload = {
  uuid: 'cust-uuid-111', // UUID dari Customer yang mau di-update
  addresses: [], // Sesuai tipe, ini adalah array kosong.
};

// **PENTING:** Jika tipe `AdressesPayload` seharusnya berisi data alamat,
// maka tipenya harus diubah dari `addresses: []` menjadi `addresses: Address[]`.
// Contohnya akan seperti ini:
/*
export const dummyAddressesPayloadWithData: { uuid: string, addresses: Address[] } = {
  uuid: 'cust-uuid-111',
  addresses: [
    {
      uuid: 'addr-uuid-new-004',
      // ... (isi detail alamat baru di sini)
    }
  ]
};
*/