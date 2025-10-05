// src/components/forms/shared/location-form-fields.tsx (VERSI FINAL YANG SUDAH DIPERBAIKI)

import { Control } from 'react-hook-form';
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';

type LocationFormFieldsProps = {
  control: Control<any>;
  basePath: string;
};

export function LocationFormFields({ control, basePath }: LocationFormFieldsProps) {
  const fieldName = (name: string) => `${basePath}${name}`;

  return (
    <div className="space-y-3">
      <FormField control={control} name={fieldName('name')} render={({ field }) => (
        <FormItem>
          <FormLabel>Nama Lokasi</FormLabel>
          <FormControl><Input placeholder="Gudang Pusat" {...field} /></FormControl>
          <FormMessage />
        </FormItem>
      )}/>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <FormField control={control} name={fieldName('addr_line_1')} render={({ field }) => (
          <FormItem>
            <FormLabel>Alamat Baris 1</FormLabel>
            <FormControl><Input placeholder="Jl. Jenderal Sudirman No. 1" {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('addr_line_2')} render={({ field }) => (
          <FormItem>
            <FormLabel>Alamat Baris 2</FormLabel>
            <FormControl><Input placeholder="Kecamatan, Kelurahan" {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('city')} render={({ field }) => (
          <FormItem>
            <FormLabel>Kota</FormLabel>
            <FormControl><Input placeholder="Jakarta" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('state_province')} render={({ field }) => (
          <FormItem>
            <FormLabel>Provinsi</FormLabel>
            <FormControl><Input placeholder="DKI Jakarta" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('location_pic')} render={({ field }) => (
          <FormItem>
            <FormLabel>Nama PIC</FormLabel>
            <FormControl><Input placeholder="Budi" {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('location_pic_contact')} render={({ field }) => (
          <FormItem>
            <FormLabel>Kontak PIC</FormLabel>
            <FormControl><Input placeholder="08123456789" {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
      </div>
      
      <FormField control={control} name={fieldName('delivery_instructions')} render={({ field }) => (
        <FormItem>
          <FormLabel>Instruksi Pengiriman</FormLabel>
          <FormControl><Textarea placeholder="Contoh: Barang diturunkan di Pintu B" {...field} value={field.value ?? ''} /></FormControl>
          <FormMessage />
        </FormItem>
      )}/>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <FormField control={control} name={fieldName('postal_code')} render={({ field }) => (
          <FormItem>
            <FormLabel>Kode Pos (Opsional)</FormLabel>
            <FormControl><Input {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('location_type')} render={({ field }) => (
          <FormItem>
            <FormLabel>Tipe Lokasi (Opsional)</FormLabel>
            <FormControl><Input placeholder="Gudang" {...field} value={field.value ?? ''} /></FormControl>
            <FormMessage />
          </FormItem>
        )}/>
      </div>

      <div className="flex items-center space-x-4 pt-2">
        <FormField control={control} name={fieldName('is_default')} render={({ field }) => (
          <FormItem className="flex items-center space-x-2">
            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} /></FormControl>
            <FormLabel>Lokasi Default</FormLabel>
          </FormItem>
        )}/>
        <FormField control={control} name={fieldName('is_active')} render={({ field }) => (
          <FormItem className="flex items-center space-x-2">
            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} /></FormControl>
            <FormLabel>Aktif</FormLabel>
          </FormItem>
        )}/>
      </div>
    </div>
  );
}