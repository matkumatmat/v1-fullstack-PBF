'use client';
import { Button } from '@/components/ui/button';
import { IconUserCircle } from '@tabler/icons-react';

export function UserNav() {
  return (
    <Button variant='ghost' className='relative h-8 w-8 rounded-full'>
      <IconUserCircle />
    </Button>
  );
}
