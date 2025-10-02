'use client';

import * as React from 'react';
import { IconSearch, IconUserCircle } from '@tabler/icons-react';
import { Button } from '@/components/ui/button';
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';

// Langkah 1: Impor data dummy dan tipe
import { DUMMY_CUSTOMERS } from '../dummy-data-address'; // Sesuaikan path jika perlu
import { Customer } from '../types'; // Sesuaikan path jika perlu

export default function CustomerSearch() {
  const [open, setOpen] = React.useState(false);
  
  const customers = DUMMY_CUSTOMERS;

  const handleSelectCustomer = (customer: Customer) => {
    console.log('Customer dipilih:', customer.customer);
    setOpen(false); 
  };

  return (
    <>
      {/* Tombol Trigger */}
      <Button
        variant='outline'
        className='bg-background text-muted-foreground relative h-9 w-full justify-start rounded-[0.5rem] text-sm font-normal shadow-none sm:pr-12 md:w-40 lg:w-64'
        onClick={() => setOpen(true)}
      >
        <IconSearch className='mr-2 h-4 w-4' />
        <span>Cari customer...</span>
      </Button>

      {/* Dialog Command Palette */}
      <CommandDialog open={open} onOpenChange={setOpen}>
        <CommandInput placeholder='Ketik nama customer untuk mencari...' />
        <CommandList>
          <CommandEmpty>Tidak ada customer ditemukan.</CommandEmpty>
          
          {/* Langkah 3: Sederhanakan rendering karena tidak ada state loading */}
          <CommandGroup heading='Customers'>
            {customers.map((customer) => (
              <CommandItem
                key={customer.uuid}
                value={customer.customer} // Value ini digunakan untuk filtering/pencarian
                onSelect={() => handleSelectCustomer(customer)}
                className="cursor-pointer"
              >
                <IconUserCircle className='mr-2 h-4 w-4' />
                <div className="flex flex-col">
                  <span>{customer.customer}</span>
                  <span className="text-xs text-muted-foreground">
                    {customer.customer_sector_type}
                  </span>
                </div>
              </CommandItem>
            ))}
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  );
}