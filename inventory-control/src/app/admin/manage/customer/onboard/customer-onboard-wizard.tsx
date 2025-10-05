// src/app/admin/manage/customer/onboard/customer-onboard-wizard.tsx

'use client';

import { useState } from 'react';
import { useForm, useFieldArray, FieldErrors, Control } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Loader2, PlusCircle, Trash2, ArrowLeft, ArrowRight } from 'lucide-react';

import { customerOnboardSchema, CustomerOnboardPayload, customerTypeEnumSchema } from '@/lib/schemas/customer-schemas';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { LocationFormFields } from '@/components/forms/shared/location-form-fields';

async function onboardCustomer(payload: CustomerOnboardPayload) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const response = await fetch(`${apiUrl}/api/v1/customer/customers/onboard`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Gagal melakukan onboarding customer.');
  }
  return response.json();
}

const steps = [
  { id: 1, name: 'Informasi Dasar', fields: ['name', 'customer_type'] as const },
  { id: 2, name: 'Detail & Spesifikasi', fields: ['details', 'specification'] as const },
  { id: 3, name: 'Struktur Cabang', fields: ['branches'] as const },
  { id: 4, name: 'Review & Submit' },
];

// Default location sekarang hanya berisi string kosong untuk nullable fields
// karena skema Zod sudah menghandle transformasi ke null.
const defaultLocation = {
  name: '', state_province: '', city: '', 
  addr_line_1: '', addr_line_2: '', addr_line_3: '',
  location_pic: '', location_pic_contact: '', delivery_instructions: '',
  postal_code: '', location_type: '', is_default: false, is_active: true,
};

export function CustomerOnboardWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const router = useRouter();
  const form = useForm<CustomerOnboardPayload>({
    resolver: zodResolver(customerOnboardSchema),
    defaultValues: {
      name: '',
      customer_type: undefined,
      details: { npwp: '', bank: '', rekening: '' },
      specification: { default_credit_limit: 0, default_payment_terms_days: 30 },
      branches: [],
    },
    mode: 'onTouched',
  });

  const { fields: branchFields, append: appendBranch, remove: removeBranch } = useFieldArray({
    control: form.control, name: 'branches',
  });

  const mutation = useMutation({
    mutationFn: onboardCustomer,
    onSuccess: () => {
      toast.success('Customer baru berhasil di-onboard!');
      router.push('/admin/manage/customer');
    },
    onError: (error: Error) => toast.error(error.message),
  });

  const next = async () => {
    const fields = steps[currentStep].fields;
    if (fields) {
      const output = await form.trigger(fields, { shouldFocus: true });
      if (!output) return;
    }
    if (currentStep < steps.length - 1) setCurrentStep(step => step + 1);
  };

  const prev = () => { if (currentStep > 0) setCurrentStep(step => step - 1); };
  
  // ===============================================
  // FUNGSI SUBMIT DENGAN LOGGING
  // ===============================================
  function onValidSubmit(values: CustomerOnboardPayload) {
    console.log("✅ VALIDASI BERHASIL. DATA YANG DIKIRIM:", values);
    mutation.mutate(values);
  }

  function onInvalidSubmit(errors: FieldErrors<CustomerOnboardPayload>) {
    console.error("❌ VALIDASI GAGAL. DETAIL ERROR:", errors);
    toast.error("Form tidak valid. Silakan periksa kembali field yang ditandai merah.");
  }

  return (
    <div className="space-y-8">
      <Progress value={((currentStep + 1) / steps.length) * 100} />
      <Form {...form}>
        {/* Tambahkan handler onInvalidSubmit di sini */}
        <form onSubmit={form.handleSubmit(onValidSubmit, onInvalidSubmit)} className="space-y-6">
          
          {/* Step 1: Informasi Dasar */}
          <div className={currentStep === 0 ? 'block' : 'hidden'}>
            <div className="space-y-4">
              <FormField control={form.control} name="name" render={({ field }) => (
                <FormItem><FormLabel>Nama Customer</FormLabel><FormControl><Input placeholder="PT. Maju Mundur" {...field} /></FormControl><FormMessage /></FormItem>
              )}/>
              <FormField control={form.control} name="customer_type" render={({ field }) => (
                <FormItem><FormLabel>Tipe Customer</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl><SelectTrigger><SelectValue placeholder="Pilih tipe customer" /></SelectTrigger></FormControl>
                    <SelectContent>{customerTypeEnumSchema.options.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}</SelectContent>
                  </Select><FormMessage />
                </FormItem>
              )}/>
            </div>
          </div>

          {/* Step 2: Detail & Spesifikasi */}
          <div className={currentStep === 1 ? 'block' : 'hidden'}>
            <div className="space-y-4">
              <FormField control={form.control} name="details.npwp" render={({ field }) => (
                <FormItem><FormLabel>NPWP (Opsional)</FormLabel><FormControl><Input {...field} value={field.value ?? ''} /></FormControl><FormMessage /></FormItem>
              )}/>
              <FormField control={form.control} name="details.bank" render={({ field }) => (
                <FormItem><FormLabel>Bank (Opsional)</FormLabel><FormControl><Input {...field} value={field.value ?? ''} /></FormControl><FormMessage /></FormItem>
              )}/>
              <FormField control={form.control} name="details.rekening" render={({ field }) => (
                <FormItem><FormLabel>No. Rekening (Opsional)</FormLabel><FormControl><Input {...field} value={field.value ?? ''} /></FormControl><FormMessage /></FormItem>
              )}/>
              <Separator />
              <FormField control={form.control} name="specification.default_credit_limit" render={({ field }) => (
                <FormItem><FormLabel>Limit Kredit Default</FormLabel>
                  <FormControl><Input type="number" {...field} onChange={e => field.onChange(e.target.value === '' ? 0 : parseFloat(e.target.value))} /></FormControl>
                  <FormMessage />
                </FormItem>
              )}/>
              <FormField control={form.control} name="specification.default_payment_terms_days" render={({ field }) => (
                <FormItem><FormLabel>Termin Pembayaran (Hari)</FormLabel>
                  <FormControl><Input type="number" {...field} onChange={e => field.onChange(e.target.value === '' ? 0 : parseInt(e.target.value, 10))} /></FormControl>
                  <FormMessage />
                </FormItem>
              )}/>
            </div>
          </div>

          {/* Step 3: Struktur Cabang */}
          <div className={currentStep === 2 ? 'block' : 'hidden'}>
            <div className="space-y-4">
              {branchFields.map((branch, branchIndex) => (
                <div key={branch.id} className="p-4 border rounded-lg space-y-4">
                  <div className="flex justify-between items-center">
                    <h4 className="font-semibold">Cabang #{branchIndex + 1}</h4>
                    <Button type="button" variant="ghost" size="icon" onClick={() => removeBranch(branchIndex)}><Trash2 className="h-4 w-4 text-destructive" /></Button>
                  </div>
                  <FormField control={form.control} name={`branches.${branchIndex}.name`} render={({ field }) => (
                    <FormItem><FormLabel>Nama Cabang</FormLabel><FormControl><Input {...field} /></FormControl><FormMessage /></FormItem>
                  )}/>
                  <LocationArrayInput branchIndex={branchIndex} control={form.control} />
                </div>
              ))}
              <Button type="button" variant="outline" onClick={() => appendBranch({ name: '', locations: [defaultLocation] })}>
                <PlusCircle className="mr-2 h-4 w-4" /> Tambah Cabang
              </Button>
            </div>
          </div>

          {/* Step 4: Review */}
          <div className={currentStep === 3 ? 'block' : 'hidden'}>
            <div className="space-y-2 p-4 border rounded-md bg-muted/50 text-sm">
              <h3 className="font-semibold text-base mb-2">Review Data</h3>
              <p><strong>Nama:</strong> {form.watch('name') || '-'}</p>
              <p><strong>Tipe:</strong> {form.watch('customer_type') || '-'}</p>
              <p><strong>Jumlah Cabang:</strong> {form.watch('branches')?.length || 0}</p>
              {form.watch('branches')?.map((branch, index) => (
                 <div key={index} className="pl-4 mt-1">
                    <p><strong>Cabang {index + 1}:</strong> {branch.name || '(Tanpa Nama)'} - {branch.locations.length} lokasi</p>
                 </div>
              ))}
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="mt-8 pt-5">
            <div className="flex justify-between">
              <Button type="button" onClick={prev} disabled={currentStep === 0}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Kembali
              </Button>
              {currentStep < steps.length - 1 && (
                <Button type="button" onClick={next}>
                  Lanjutkan <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              )}
              {currentStep === steps.length - 1 && (
                <Button type="submit" disabled={mutation.isPending}>
                  {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Submit Onboarding
                </Button>
              )}
            </div>
          </div>
        </form>
      </Form>
    </div>
  );
}

// Tidak ada perubahan pada komponen ini
function LocationArrayInput({ branchIndex, control }: { branchIndex: number, control: Control<any> }) {
  const { fields, append, remove } = useFieldArray({
    control, name: `branches.${branchIndex}.locations`,
  });

  return (
    <div className="pl-4 border-l-2 ml-2 space-y-3">
      <h5 className="font-medium text-sm">Lokasi</h5>
      {fields.map((location, locationIndex) => (
        <div key={location.id} className="p-3 border rounded-md bg-background">
          <div className="flex justify-between items-center mb-2">
            <h6 className="text-xs font-semibold">Lokasi #{locationIndex + 1}</h6>
            {fields.length > 1 && <Button type="button" variant="ghost" size="icon" className="h-6 w-6" onClick={() => remove(locationIndex)}><Trash2 className="h-3 w-3 text-destructive" /></Button>}
          </div>
          <LocationFormFields control={control} basePath={`branches.${branchIndex}.locations.${locationIndex}.`} />
        </div>
      ))}
      <Button type="button" variant="secondary" size="sm" onClick={() => append(defaultLocation)}>
        <PlusCircle className="mr-2 h-3 w-3" /> Tambah Lokasi
      </Button>
    </div>
  );
}