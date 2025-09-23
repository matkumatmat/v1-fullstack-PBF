import { PrintQueueItem, PrintGroup, PrintPayloadItem, Product } from "./types";

const produkList1: Product[] = [
  { nama: 'Kertas HVS A4 70gr', qty: '5 rim' },
  { nama: 'Spidol Boardmarker Hitam', qty: '12 pcs' },
];

const produkList2: Product[] = [
  { nama: 'Tinta Printer Epson L3110 Black', qty: '2 botol' },
];

const produkList3: Product[] = [
  { nama: 'Buku Tulis Sinar Dunia 38lbr', qty: '10 pack' },
  { nama: 'Pulpen Standard AE7', qty: '2 box' },
  { nama: 'Lakban Bening', qty: '3 pcs' },
];

export const dummyPrintQueue: PrintQueueItem[] = [
  {
    id: 101, // ID PT. Tujuan
    pt_tujuan: 'PT. Sejahtera Abadi',
    status: 'undone',
    groups: [
      {
        from: 1,
        to: 50,
        petugas: 'Budi Hartono',
        berat: '25 kg',
        produk_list: produkList1,
      },
      {
        from: 51,
        to: 60,
        petugas: 'Budi Hartono',
        berat: '10 kg',
        produk_list: produkList2,
      },
    ],
  },
  {
    id: 102,
    pt_tujuan: 'CV. Cipta Karya Nusantara',
    status: 'done',
    groups: [
      {
        from: 1,
        to: 20,
        petugas: 'Siti Aminah',
        berat: '15.5 kg',
        produk_list: produkList3,
      },
    ],
  },
  {
    id: 103,
    pt_tujuan: 'Gudang Logistik Bersama',
    status: 'undone',
    groups: [
      {
        from: 100,
        to: 250,
        petugas: 'Agus Setiawan',
        berat: '150 kg',
        produk_list: [{ nama: 'Kardus Packing Ukuran Medium', qty: '150 pcs' }],
      },
    ],
  },
];