// Fixed Form Dialog with Validation
// inventory-control/src/features/config/components/config-form-dialog.tsx
'use client';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const formSchema = z.object({
  code: z.string().min(1, 'Code is required').max(50, 'Code must be less than 50 characters'),
  name: z.string().min(1, 'Name is required').max(100, 'Name must be less than 100 characters'),
  description: z.string().max(255, 'Description must be less than 255 characters').optional()
});

interface ConfigFormDialogProps {
  onSave: (data: any) => Promise<void>;
  item?: any;
  isLoading?: boolean;
}

export function ConfigFormDialog({ onSave, item, isLoading = false }: ConfigFormDialogProps) {
  const [open, setOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      code: item?.code || '',
      name: item?.name || '',
      description: item?.description || ''
    }
  });

  useEffect(() => {
    if (item) {
      form.reset({
        code: item.code || '',
        name: item.name || '',
        description: item.description || ''
      });
    } else {
      form.reset({
        code: '',
        name: '',
        description: ''
      });
    }
  }, [item, form]);

  const handleSubmit = async (data: any) => {
    try {
      setIsSubmitting(true);
      await onSave({ ...item, ...data });
      setOpen(false);
      form.reset();
    } catch (error) {
      console.error('Error saving item:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant={item ? 'outline' : 'default'} disabled={isLoading}>
          {item ? 'Edit' : 'Add New'}
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{item ? 'Edit Item' : 'Add New Item'}</DialogTitle>
          <DialogDescription>
            Fill out the form to {item ? 'edit the' : 'add a new'} configuration
            item.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className='space-y-4'
          >
            <FormField
              control={form.control}
              name='code'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Code *</FormLabel>
                  <FormControl>
                    <Input placeholder='Enter code' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='name'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name *</FormLabel>
                  <FormControl>
                    <Input placeholder='Enter name' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='description'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Input placeholder='Enter description' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button 
                type='button' 
                variant='outline' 
                onClick={() => setOpen(false)}
              >
                Cancel
              </Button>
              <Button 
                type='submit' 
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Saving...' : 'Save'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
