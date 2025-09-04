export type Destination = {
  id: number;
  pt: string;
  pt_tujuan: string;
  instansi: string;
  tujuan: string;
  alamat: string;
  provinsi: string;
  kontak: string | null;
};

export type Log = {
  id: number;
  pt_tujuan: string;
  box_number: string;
  produk: string;
  status: string;
  tanggal_print: string;
};

export type PrintQueueItem = {
  id: number; // This is the destination id
  pt_tujuan: string;
  status: 'undone' | 'done';
  groups: PrintGroup[];
};

export type PrintGroup = {
  from: number;
  to: number;
  petugas: string;
  berat: string;
  produk_list: Product[];
};

export type Product = {
  nama: string;
  qty: string;
};

export type PrintPayloadItem = {
  id: number;
  box_number: string;
  petugas: string;
  berat: string;
  produk_list: Product[];
};
