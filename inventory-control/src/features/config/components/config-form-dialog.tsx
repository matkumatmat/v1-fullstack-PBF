'use client';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { useEffect, useState, useMemo } from 'react';
import { useForm, FieldValues } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { getMetadataForType, FieldConfig } from '../config-metadata';

interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  [key: string]: any;
}

interface ConfigFormDialogProps {
  onSave: (data: any) => Promise<void>;
  item?: ConfigItem;
  isLoading?: boolean;
  selectedType: string;
}

export function ConfigFormDialog({ onSave, item, isLoading = false, selectedType }: ConfigFormDialogProps) {
  const [open, setOpen] = useState(false);

  const additionalFields = useMemo(() => getMetadataForType(selectedType), [selectedType]);

  const formSchema = useMemo(() => {
    const baseSchema = {
      code: z.string().min(1, 'Code is required').max(50),
      name: z.string().min(1, 'Name is required').max(100),
      description: z.string().max(255).optional().nullable(),
    };
    const dynamicSchema = additionalFields.reduce((acc, field) => {
      acc[field.key] = field.validation;
      return acc;
    }, {} as Record<string, z.ZodTypeAny>);
    return z.object({ ...baseSchema, ...dynamicSchema });
  }, [additionalFields]);

  type FormData = z.infer<typeof formSchema>;

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {},
  });
  
  useEffect(() => {
    if (open) {
      const defaultValues: FieldValues = {};
      if (item) {
        defaultValues.code = item.code || '';
        defaultValues.name = item.name || '';
        defaultValues.description = item.description || null;
        additionalFields.forEach(field => {
          const value = item[field.key];
          if (field.type === 'boolean') {
            defaultValues[field.key] = !!value;
          } else {
            defaultValues[field.key] = value ?? '';
          }
        });
      } else {
        defaultValues.code = '';
        defaultValues.name = '';
        defaultValues.description = '';
        additionalFields.forEach(field => {
          const defValue = (form.formState.defaultValues as any)?.[field.key];
          defaultValues[field.key] = defValue ?? (field.type === 'boolean' ? false : '');
        });
      }
      form.reset(defaultValues as FormData);
    }
  }, [open, item, additionalFields, form]);

  const handleSubmit = async (data: FormData) => {
    try {
      await onSave({ ...item, ...data });
      setOpen(false);
    } catch (error) {
      console.error("Submission failed, dialog remains open.");
    }
  };
  
  // DIUBAH: Helper renderField disederhanakan untuk hanya mengembalikan elemen input
  const renderField = (fieldConfig: FieldConfig, formField: any) => {
    switch (fieldConfig.type) {
      case 'boolean':
        return (
          <Checkbox
            checked={formField.value}
            onCheckedChange={formField.onChange}
            id={fieldConfig.key}
          />
        );
      case 'textarea':
        return <Textarea placeholder={fieldConfig.placeholder || `Enter ${fieldConfig.label}`} {...formField} value={formField.value ?? ''}/>;
      case 'number':
      case 'decimal':
        return <Input type="number" step={fieldConfig.type === 'decimal' ? '0.01' : '1'} placeholder={fieldConfig.placeholder || `Enter ${fieldConfig.label}`} {...formField} value={formField.value ?? ''} />;
      default:
        return <Input placeholder={fieldConfig.placeholder || `Enter ${fieldConfig.label}`} {...formField} value={formField.value ?? ''} />;
    }
  };

  // BARU: Logika untuk mengelompokkan field menjadi baris-baris
  const groupedFields = useMemo(() => {
    const groups: Record<string, FieldConfig[]> = {};
    const result: FieldConfig[][] = [];
    
    additionalFields.forEach(field => {
      if (field.group) {
        if (!groups[field.group]) {
          groups[field.group] = [];
          result.push(groups[field.group]);
        }
        groups[field.group].push(field);
      } else {
        result.push([field]);
      }
    });
    
    return result;
  }, [additionalFields]);

  // BARU: Cek apakah ada grup untuk melebarkan dialog
  const hasGroups = useMemo(() => additionalFields.some(field => !!field.group), [additionalFields]);
  
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {item ? <Button variant='ghost' size='sm'>Edit</Button> : <Button>Add New</Button>}
      </DialogTrigger>
      {/* DIUBAH: Lebar dialog sekarang dinamis */}
      <DialogContent className={hasGroups ? "sm:max-w-2xl" : "sm:max-w-md"}>
        <DialogHeader>
          <DialogTitle>{item ? 'Edit Item' : 'Add New Item'}</DialogTitle>
          <DialogDescription>
            {item ? `Editing "${item.name}"` : `Add a new item to ${selectedType}`}
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            {/* Field Dasar */}
            <FormField control={form.control} name="code" render={({ field }) => (
                <FormItem>
                  <FormLabel>Code</FormLabel>
                  <FormControl><Input placeholder="Enter code" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
            )}/>
            <FormField control={form.control} name="name" render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl><Input placeholder="Enter name" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
            )}/>
            <FormField control={form.control} name="description" render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl><Textarea placeholder="Enter description (optional)" {...field} value={field.value ?? ''} /></FormControl>
                  <FormMessage />
                </FormItem>
            )}/>

            {/* DIUBAH: Logika render dinamis yang benar */}
            {groupedFields.map((fieldGroup, index) => (
              // Setiap 'fieldGroup' adalah satu baris
              <div key={index} className="flex flex-col sm:flex-row sm:items-start sm:gap-4">
                {fieldGroup.map((fieldConfig) => (
                  // Setiap 'fieldConfig' adalah satu kolom di dalam baris
                  <div key={fieldConfig.key} className="flex-1 w-full">
                    <FormField
                      control={form.control}
                      name={fieldConfig.key as keyof FormData}
                      render={({ field }) => (
                        <FormItem 
                          className={
                            fieldConfig.type === 'boolean'
                              ? "flex flex-row items-center space-x-3 space-y-0 h-10"
                              : "space-y-2"
                          }
                        >
                          {fieldConfig.type !== 'boolean' && <FormLabel>{fieldConfig.label}</FormLabel>}
                          
                          <FormControl>
                            {renderField(fieldConfig, field)}
                          </FormControl>

                          {fieldConfig.type === 'boolean' && (
                            <FormLabel htmlFor={fieldConfig.key} className="font-normal cursor-pointer">
                              {fieldConfig.label}
                            </FormLabel>
                          )}

                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                ))}
              </div>
            ))}
            
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={form.formState.isSubmitting}>
                Cancel
              </Button>
              <Button type="submit" disabled={form.formState.isSubmitting || isLoading}>
                {form.formState.isSubmitting ? 'Saving...' : 'Save'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}