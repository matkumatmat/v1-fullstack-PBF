"use client";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Destination, PrintQueueItem, PrintGroup, Product } from "../types";
import { useState, useEffect } from "react";
import { useForm, useFieldArray } from "react-hook-form";

type KirimanModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onSave: (item: PrintQueueItem) => void;
  editingItem: PrintQueueItem | null;
  allDestinations: Destination[];
};

type GroupFormData = {
    from: number;
    to: number;
    petugas: string;
    berat: string;
    produk_list: Product[];
}

export function KirimanModal({ isOpen, onClose, onSave, editingItem, allDestinations }: KirimanModalProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<Destination[]>([]);
  const [selectedDestination, setSelectedDestination] = useState<Destination | null>(null);
  const [tempGroups, setTempGroups] = useState<PrintGroup[]>([]);

  const { register, control, handleSubmit, reset, watch } = useForm<GroupFormData>({
    defaultValues: {
      from: 1,
      to: 1,
      petugas: "",
      berat: "",
      produk_list: [{ nama: "", qty: "" }],
    },
  });
  const { fields, append, remove } = useFieldArray({
    control,
    name: "produk_list",
  });

  useEffect(() => {
    if (isOpen) {
        if (editingItem) {
            const dest = allDestinations.find(d => d.id === editingItem.id);
            setSelectedDestination(dest || null);
            setSearchTerm(dest?.pt_tujuan || editingItem.pt_tujuan);
            setTempGroups(editingItem.groups);
        } else {
            setSearchTerm("");
            setSelectedDestination(null);
            setTempGroups([]);
            reset({
                from: 1,
                to: 1,
                petugas: "",
                berat: "",
                produk_list: [{ nama: "", qty: "" }],
            });
        }
    }
  }, [editingItem, isOpen, allDestinations, reset]);

  useEffect(() => {
    if (searchTerm && !selectedDestination) {
      const filtered = allDestinations
        .filter(d =>
            d.pt_tujuan.toLowerCase().includes(searchTerm.toLowerCase()) ||
            d.instansi.toLowerCase().includes(searchTerm.toLowerCase())
        )
        .slice(0, 5);
      setSearchResults(filtered);
    } else {
      setSearchResults([]);
    }
  }, [searchTerm, allDestinations, selectedDestination]);

  const handleSelectDestination = (dest: Destination) => {
    setSelectedDestination(dest);
    setSearchTerm(dest.pt_tujuan);
    setSearchResults([]);
    const nextBoxNumber = (tempGroups.reduce((max, g) => Math.max(max, g.to), 0) || 0) + 1;
    reset({ ...watch(), from: nextBoxNumber, to: nextBoxNumber });
  };

  const handleAddGroup = (data: GroupFormData) => {
    if (data.to < data.from) {
        alert("Nomor box 'sampai' tidak boleh lebih kecil dari 'dari'");
        return;
    }
    const newGroup: PrintGroup = { ...data, produk_list: data.produk_list.filter(p => p.nama) };
    setTempGroups([...tempGroups, newGroup]);
    const nextBoxNumber = data.to + 1;
    reset({
        from: nextBoxNumber,
        to: nextBoxNumber,
        petugas: data.petugas, // carry over petugas
        berat: data.berat, // carry over berat
        produk_list: [{nama: "", qty: ""}]
    });
  };

  const handleDeleteGroup = (index: number) => {
    setTempGroups(tempGroups.filter((_, i) => i !== index));
  }

  const handleSaveToQueue = () => {
    if (!selectedDestination) {
      alert("Pilih alamat tujuan terlebih dahulu!");
      return;
    }
    if (tempGroups.length === 0) {
      alert("Tambahkan minimal satu grup label!");
      return;
    }
    const newItem: PrintQueueItem = {
      id: selectedDestination.id,
      pt_tujuan: selectedDestination.pt_tujuan,
      status: editingItem?.status || 'undone',
      groups: tempGroups,
    };
    onSave(newItem);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-4xl h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>{editingItem ? 'Edit Kiriman' : 'Buat Kiriman Baru'}</DialogTitle>
        </DialogHeader>

        <div className="flex-grow overflow-y-auto pr-6 space-y-6">
            {/* Step 1: Destination */}
            <div>
                <Label>1. Cari & Pilih Alamat Tujuan</Label>
                <div className="pt-4 relative">
                    <Input
                        placeholder="Ketik untuk mencari..."
                        value={searchTerm}
                        onChange={e => {
                            setSearchTerm(e.target.value)
                            if (selectedDestination) {
                                setSelectedDestination(null);
                            }
                        }}
                        disabled={!!editingItem}
                    />
                    {searchResults.length > 0 && (
                        <div className="absolute z-10 w-full bg-slate-800 border border-slate-700 rounded-md mt-1">
                            {searchResults.map(dest => (
                                <div key={dest.id} className="p-2 hover:bg-slate-700 cursor-pointer" onClick={() => handleSelectDestination(dest)}>
                                    {dest.pt_tujuan}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Step 2: Groups */}
            {selectedDestination && (
                <div className="space-y-4">
                    <div className="bg-slate-700/50 p-4 rounded-lg">
                        <p className="font-semibold">{selectedDestination.pt_tujuan}</p>
                        <p className="text-sm text-slate-400">{selectedDestination.alamat}</p>
                    </div>

                    <form onSubmit={handleSubmit(handleAddGroup)} className="border-2 border-dashed border-slate-600 p-4 rounded-lg space-y-4">
                        <h3 className="font-bold text-lg">Tambah Grup Label Baru</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <Input type="number" placeholder="Dari Box No." {...register("from", { valueAsNumber: true, min: 1 })} />
                            <Input type="number" placeholder="Sampai Box No." {...register("to", { valueAsNumber: true, min: 1 })} />
                            <Input placeholder="Petugas" {...register("petugas")} />
                            <Input placeholder="Berat (Kg)" {...register("berat")} />
                        </div>
                        <div>
                            <Label>Produk</Label>
                            {fields.map((field, index) => (
                                <div key={field.id} className="flex items-center gap-2 mt-2">
                                    <Input placeholder="Nama Produk" {...register(`produk_list.${index}.nama`)} />
                                    <Input placeholder="Qty" {...register(`produk_list.${index}.qty`)} />
                                    <Button type="button" variant="destructive" size="sm" onClick={() => remove(index)}>X</Button>
                                </div>
                            ))}
                            <Button type="button" size="sm" variant="outline" className="mt-2" onClick={() => append({nama: "", qty: ""})}>+ Tambah Produk</Button>
                        </div>
                        <div className="text-right">
                            <Button type="submit">Tambah Grup</Button>
                        </div>
                    </form>

                    <div className="space-y-2">
                        <h3 className="font-bold text-lg">Ringkasan Grup</h3>
                        {tempGroups.length === 0 ? (
                            <p className="text-sm text-slate-400">Belum ada grup yang ditambahkan.</p>
                        ) : (
                            tempGroups.map((group, index) => (
                                <div key={index} className="bg-slate-700 p-3 rounded-lg flex justify-between items-center">
                                    <div>
                                        <p className="font-bold">Grup {index + 1}: Box {group.from} - {group.to}</p>
                                        <p className="text-sm text-slate-300">{group.produk_list.map(p=>p.nama).join(', ') || 'Tanpa produk'}</p>
                                    </div>
                                    <Button variant="destructive" size="sm" onClick={() => handleDeleteGroup(index)}>Hapus</Button>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>

        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>Batal</Button>
          <Button onClick={handleSaveToQueue} disabled={!selectedDestination || tempGroups.length === 0}>
            {editingItem ? 'Simpan Perubahan' : 'Simpan ke Antrian'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
