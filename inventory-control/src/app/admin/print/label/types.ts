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

export type PrintPayloadItem = {
  id: number;
  box_number: string;
  petugas: string;
  berat: string;
  produk_list: Product[];
};

export type Product = {
  nama: string;
  qty: string;
};

export type Customer ={
  uuid:string;
  customer:string;
  customer_type:string;
  customer_sector_type:string;
  customer_addresses:Address[];
};

export type Address = {
  uuid: string;
  addresses_type:string;
  addresses_line1:string;
  addresses_line2:string;
  city:string;
  state_province:string;
  postal_code:string;
  country:string;
  contact_person:string;
  contact_phone:string;
  contact_email:string;
  delivery_instructions:string;
  special_requirements:string;
  latitude:number;
  longitude:number;
  is_active:boolean;
  is_default:boolean;
};

export type AdressesPayload ={
  uuid:string
  addresses:[];
}