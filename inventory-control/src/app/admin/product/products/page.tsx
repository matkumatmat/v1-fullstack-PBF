"use client";

import React, { useState } from 'react';
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { format } from "date-fns";
import { id } from "date-fns/locale";
import { CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";

import PageContainer from '@/components/layout/page-container';
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Textarea } from "@/components/ui/textarea";

const formSchema = z.object({
  customer: z.string().min(1, "Nama customer harus diisi."),
  kota: z.string().min(1, "Kota harus diisi."),
  provinsi: z.string().min(1, "Provinsi harus diisi."),
  nomorSo: z.string().optional(),
  nomorPo: z.string().min(1, "Nomor PO harus diisi."),
  tglPo: z.date({ required_error: "Tanggal PO harus diisi." }),
  realisasiQty: z.coerce.number().min(1, "Kuantitas minimal 1."),
  tglKirim: z.date({ required_error: "Tanggal kirim harus diisi." }),
  realisasiValue: z.coerce.number().min(1, "Value harus diisi."),
  keterangan: z.string().optional(),
});

type Product = {
  id: number;
  type: string;
  sku: string;
  name: string;
  packaging: string;
  price: string;
  priceUnit: string;
  stock: string;
  stockUnit: string;
};

const productsData: Product[] = [
  {
    id: 1,
    type: 'TENDER SWT',
    sku: 'AHPVA408AC',
    name: 'BOPV 20 dsA BHDABINAOSDNABDJASNDKAJD',
    packaging: '10 Amp/box',
    price: '129.969',
    priceUnit: 'ampul',
    stock: '120.911',
    stockUnit: 'ampul'
  },
  {
    id: 4,
    type: 'TENDER SWT',
    sku: 'AHPVA408AC',
    name: 'BOPV 20 dsA BHDABINAOSDNABDJASNDKAJD',
    packaging: '10 Amp/box',
    price: '129.969',
    priceUnit: 'ampul',
    stock: '120.911',
    stockUnit: 'ampul'
  },
  {
    id: 3,
    type: 'TENDER SWT',
    sku: 'AHPVA408AC',
    name: 'BOPV 20 dsA BHDABINAOSDNABDJASNDKAJD',
    packaging: '10 Amp/box',
    price: '129.969',
    priceUnit: 'ampul',
    stock: '120.911',
    stockUnit: 'ampul'
  },
  {
    id: 2,
    type: 'REGULER',
    sku: 'BHASD821OP',
    name: 'PRODUK REGULER NAMA PENDEK',
    packaging: '20 Strip/box',
    price: '250.000',
    priceUnit: 'box',
    stock: '5.000',
    stockUnit: 'box'
  },
];

type ProductCardProps = {
  product: Product;
  onClick: () => void;
};

const ProductCard = ({ product, onClick }: ProductCardProps) => {
  return (
    <div
      onClick={onClick}
      className='w-[160px] h-[220px] rounded-md border bg-white shadow-sm flex flex-col cursor-pointer'
    >
      <div className='relative bg-slate-300 w-full h-1/2 rounded-t-md'>
        <span className='bg-green-500 text-white text-[5px] font-bold px-1.5 py-0.5 rounded flex-shrink-0 absolute m-1'>
          {product.type}
        </span>
      </div>
      <div className='p-2 flex flex-col flex-grow'>
        <div className='flex items-center gap-1 mb-1'>
          <span className='bg-amber-500 text-white text-[5px] font-bold px-1.5 py-0.5 rounded flex-shrink-0'>
            {product.sku}
          </span>
        </div>
        <div className='flex items-start gap-2'>
          <p className=' font-semibold text-[8px] text-gray-800 leading-tight line-clamp-2' title={product.name}>
            {product.name}
          </p>
          <p className='py-1 mx-2 items-center text-[8px] text-gray-500 flex-shrink-0'>
            {product.packaging}
          </p>
        </div>
        <div className='flex items-start gap-1 mt-6'>
          <p className='font-semibold text-[8px] text-gray-800 leading-tight'>
            Harga Het :
          </p>
          <p className='font-semibold text-[8px] text-gray-500'>
            Rp.{product.price} / {product.priceUnit}
          </p>
        </div>
        <div className='flex items-start gap-1'>
          <p className='font-semibold text-[8px] text-gray-800 leading-tight'>
            Tersedia :
          </p>
          <p className='font-semibold text-[8px] text-gray-500'>
            {product.stock} {product.stockUnit}
          </p>
        </div>
      </div>
    </div>
  );
};

const ProductShowcase = () => {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      customer: "",
      kota: "",
      provinsi: "",
      nomorSo: "",
      nomorPo: "",
      realisasiQty: 0,
      realisasiValue: 0,
      keterangan: "",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log("Form Submitted:", {
      product: selectedProduct,
      formData: values,
    });
    setIsModalOpen(false);
    form.reset();
  }

  const handleCardClick = (product: Product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
    form.reset();
  };

  return (
    <PageContainer>
      <div className='w-full h-full p-4'>
        <div className='flex flex-row flex-wrap gap-4'>
          {productsData.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onClick={() => handleCardClick(product)}
            />
          ))}
        </div>
      </div>

      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Form Realisasi Penjualan</DialogTitle>
            <DialogDescription>
              Isi semua field yang dibutuhkan di bawah ini.
            </DialogDescription>
          </DialogHeader>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="customer"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Customer</FormLabel>
                      <FormControl>
                        <Input placeholder="Nama Customer" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="nomorPo"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nomor PO</FormLabel>
                      <FormControl>
                        <Input placeholder="Nomor PO" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="kota"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Kota</FormLabel>
                      <FormControl>
                        <Input placeholder="Kota" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="provinsi"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Provinsi</FormLabel>
                      <FormControl>
                        <Input placeholder="Provinsi" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                 <FormField
                  control={form.control}
                  name="tglPo"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>Tanggal PO</FormLabel>
                      <Popover>
                        <PopoverTrigger asChild>
                          <FormControl>
                            <Button
                              variant={"outline"}
                              className={cn(
                                "pl-3 text-left font-normal",
                                !field.value && "text-muted-foreground"
                              )}
                            >
                              {field.value ? (
                                format(field.value, "PPP", { locale: id })
                              ) : (
                                <span>Pilih tanggal</span>
                              )}
                              <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                            </Button>
                          </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            mode="single"
                            selected={field.value}
                            onSelect={field.onChange}
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="nomorSo"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nomor SO (Opsional)</FormLabel>
                      <FormControl>
                        <Input placeholder="Nomor SO" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormItem>
                <FormLabel>Produk</FormLabel>
                <FormControl>
                  <Input value={selectedProduct?.name || ''} disabled />
                </FormControl>
              </FormItem>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="realisasiQty"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Realisasi Qty</FormLabel>
                      <FormControl>
                        <Input type="number" placeholder="0" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="tglKirim"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>Tanggal Kirim</FormLabel>
                      <Popover>
                        <PopoverTrigger asChild>
                          <FormControl>
                            <Button
                              variant={"outline"}
                              className={cn(
                                "pl-3 text-left font-normal",
                                !field.value && "text-muted-foreground"
                              )}
                            >
                              {field.value ? (
                                format(field.value, "PPP", { locale: id })
                              ) : (
                                <span>Pilih tanggal</span>
                              )}
                              <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                            </Button>
                          </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            mode="single"
                            selected={field.value}
                            onSelect={field.onChange}
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="realisasiValue"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Realisasi Value</FormLabel>
                      <FormControl>
                        <Input type="number" placeholder="0" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormItem>
                  <FormLabel>Type</FormLabel>
                  <FormControl>
                    <Input value={selectedProduct?.type || ''} disabled />
                  </FormControl>
                </FormItem>
              </div>

              <FormField
                control={form.control}
                name="keterangan"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Keterangan (Opsional)</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Tambahkan keterangan jika ada..."
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit">Submit</Button>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </PageContainer>
  );
};

export default ProductShowcase;