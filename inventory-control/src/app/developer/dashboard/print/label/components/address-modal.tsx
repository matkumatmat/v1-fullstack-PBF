"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Destination } from "../types";
import { useForm } from "react-hook-form";
import { useEffect } from "react";

type AddressModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Destination) => void;
  address: Destination | null;
};

export function AddressModal({ isOpen, onClose, onSave, address }: AddressModalProps) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<Destination>();

  useEffect(() => {
    if (address) {
      reset(address);
    } else {
      reset({
        pt: '',
        instansi: '',
        tujuan: '',
        alamat: '',
        provinsi: '',
        kontak: '',
      } as unknown as Destination);
    }
  }, [address, reset]);

  const onSubmit = (data: Destination) => {
    onSave(data);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[625px]">
        <DialogHeader>
          <DialogTitle>{address ? "Edit Alamat" : "Tambah Alamat Baru"}</DialogTitle>
          <DialogDescription>
            {address ? "Ubah detail alamat di bawah ini." : "Isi detail untuk alamat baru."}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
            <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="pt" className="text-right">Nama PT</Label>
                    <Input id="pt" {...register("pt", { required: true })} className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="instansi" className="text-right">Instansi</Label>
                    <Input id="instansi" {...register("instansi", { required: true })} className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="tujuan" className="text-right">Tujuan</Label>
                    <Input id="tujuan" {...register("tujuan", { required: true })} className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="alamat" className="text-right">Alamat</Label>
                    <Textarea id="alamat" {...register("alamat", { required: true })} className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="provinsi" className="text-right">Provinsi</Label>
                    <Input id="provinsi" {...register("provinsi", { required: true })} className="col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="kontak" className="text-right">Kontak</Label>
                    <Input id="kontak" {...register("kontak")} className="col-span-3" />
                </div>
            </div>
            <DialogFooter>
                <Button type="button" variant="ghost" onClick={onClose}>Batal</Button>
                <Button type="submit">Simpan</Button>
            </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
