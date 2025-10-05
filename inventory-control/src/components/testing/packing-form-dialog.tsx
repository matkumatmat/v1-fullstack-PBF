// src/components/testing/packing-form-dialog.tsx

"use client";

import * as React from "react";
import { useForm, useFieldArray, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { PlusCircle, Trash2 } from "lucide-react";

// Skema validasi menggunakan Zod sesuai struktur yang Anda inginkan
const formSchema = z.object({
  total_box: z.coerce.number().min(1, "Minimal 1 box"),
  packing_slip: z.string().min(1, "Packing slip harus diisi"),
  box_number: z.array(z.object({
      id: z.coerce.number(),
      sscc: z.string(),
      gtin: z.string(),
      petugas: z.string().min(1, "Petugas harus diisi"),
      berat: z.string().min(1, "Berat harus diisi"),
      items: z.array(z.object({
          product: z.string().min(1, "Produk harus diisi"),
          batch: z.string().min(1, "Batch harus diisi"),
          expire_date: z.string().min(1, "ED harus diisi"),
          quantity: z.string().min(1, "Qty harus diisi"),
          unit: z.string().min(1, "Unit harus diisi"),
      })).min(1, "Minimal 1 item per box").max(6, "Maksimal 6 item per box"),
  })).min(1, "Harus ada minimal 1 box detail"),
});

type FormValues = z.infer<typeof formSchema>;

interface PackingFormDialogProps {
  manipulatedData: object | null;
  onFormSubmit: (finalJson: object) => void;
}

export default function PackingFormDialog({ manipulatedData, onFormSubmit }: PackingFormDialogProps) {
  const [isOpen, setIsOpen] = React.useState(false);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      packing_slip: "",
      box_number: [],
    },
  });

  const { fields: boxFields, append: appendBox, remove: removeBox } = useFieldArray({
    control: form.control,
    name: "box_number",
  });

  function onSubmit(data: FormValues) {
    const finalJson = {
      locations: manipulatedData,
      content: data,
    };
    onFormSubmit(finalJson);
    setIsOpen(false); // Tutup dialog setelah submit
    form.reset(); // Reset form
  }

  // Fungsi untuk menambah box baru dengan data statis
  const handleAddBox = () => {
    appendBox({
      id: boxFields.length + 1, // ID dinamis berdasarkan jumlah box
      sscc: "{1}{8994957}{000011111}{9}", // Statis sesuai permintaan
      gtin: "{1}{8994957}{88888888}", // Statis sesuai permintaan
      petugas: "",
      berat: "",
      items: [], // Mulai dengan item kosong
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Langkah 2: Buat Konten Pengiriman</CardTitle>
      </CardHeader>
      <CardContent>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button disabled={!manipulatedData}>
              {manipulatedData ? "Isi Detail Pengiriman" : "Pilih Lokasi Terlebih Dahulu"}
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Form Detail Pengiriman</DialogTitle>
              <DialogDescription>
                Isi detail untuk setiap box yang akan dikirim.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              {/* Form Fields Utama */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="total_box">Total Box</Label>
                  <Input id="total_box" type="number" {...form.register("total_box")} />
                  {form.formState.errors.total_box && <p className="text-red-500 text-sm">{form.formState.errors.total_box.message}</p>}
                </div>
                <div>
                  <Label htmlFor="packing_slip">No. Packing Slip</Label>
                  <Input id="packing_slip" {...form.register("packing_slip")} />
                  {form.formState.errors.packing_slip && <p className="text-red-500 text-sm">{form.formState.errors.packing_slip.message}</p>}
                </div>
              </div>

              <hr />

              {/* Form Fields Dinamis untuk Box */}
              <div className="space-y-4">
                {boxFields.map((box, boxIndex) => (
                  <BoxFormFields key={box.id} form={form} boxIndex={boxIndex} removeBox={removeBox} />
                ))}
              </div>

              <Button type="button" variant="outline" onClick={handleAddBox} className="w-full">
                <PlusCircle className="mr-2 h-4 w-4" /> Tambah Box
              </Button>

              <DialogFooter>
                <Button type="submit">Simpan dan Generate JSON</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  );
}


// Komponen terpisah untuk field di dalam box agar lebih rapi
function BoxFormFields({ form, boxIndex, removeBox }: { form: any; boxIndex: number; removeBox: (index: number) => void }) {
  const { fields: itemFields, append: appendItem, remove: removeItem } = useFieldArray({
    control: form.control,
    name: `box_number.${boxIndex}.items`,
  });

  return (
    <Card className="bg-muted/50">
      <CardHeader className="flex flex-row items-center justify-between py-3">
        <CardTitle className="text-lg">Detail Box #{boxIndex + 1}</CardTitle>
        <Button type="button" variant="ghost" size="icon" onClick={() => removeBox(boxIndex)}>
          <Trash2 className="h-4 w-4 text-red-500" />
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label>Petugas</Label>
            <Input {...form.register(`box_number.${boxIndex}.petugas`)} />
          </div>
          <div>
            <Label>Berat (kg)</Label>
            <Input {...form.register(`box_number.${boxIndex}.berat`)} />
          </div>
        </div>
        
        <Label>Item di dalam Box</Label>
        <div className="space-y-2">
            {itemFields.map((item, itemIndex) => (
                <div key={item.id} className="grid grid-cols-12 gap-2 items-center">
                    <Input placeholder="Produk" {...form.register(`box_number.${boxIndex}.items.${itemIndex}.product`)} className="col-span-3"/>
                    <Input placeholder="Batch" {...form.register(`box_number.${boxIndex}.items.${itemIndex}.batch`)} className="col-span-3"/>
                    <Input placeholder="ED (YYYY-MM-DD)" {...form.register(`box_number.${boxIndex}.items.${itemIndex}.expire_date`)} className="col-span-2"/>
                    <Input placeholder="Qty" {...form.register(`box_number.${boxIndex}.items.${itemIndex}.quantity`)} className="col-span-1"/>
                    <Input placeholder="Unit" {...form.register(`box_number.${boxIndex}.items.${itemIndex}.unit`)} className="col-span-2"/>
                    <Button type="button" variant="ghost" size="icon" onClick={() => removeItem(itemIndex)} className="col-span-1">
                        <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                </div>
            ))}
        </div>

        <Button type="button" variant="secondary" size="sm" onClick={() => appendItem({ product: '', batch: '', expire_date: '', quantity: '', unit: '' })} disabled={itemFields.length >= 6}>
          <PlusCircle className="mr-2 h-4 w-4" /> Tambah Item
        </Button>
        {form.formState.errors?.box_number?.[boxIndex]?.items && <p className="text-red-500 text-sm">Error: {form.formState.errors.box_number[boxIndex].items.message}</p>}
      </CardContent>
    </Card>
  );
}