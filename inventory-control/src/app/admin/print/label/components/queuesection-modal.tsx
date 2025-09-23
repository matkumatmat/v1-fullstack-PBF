// src/components/labeling/QueuesectionModal.tsx
import ManualTabContent from './manual-tabs'
import OtomatisTabContent from './auto-tabs' // <-- Impor komponen tab
// src/components/labeling/QueuesectionModal.tsx

import React from 'react'
import { PlusCircle } from 'lucide-react'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card" // Hanya butuh Card di sini
import { Button } from '@/components/ui/button' 

function QueuesectionModal() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button
          size="icon" 
          className="
            rounded-full       
            shadow-lg          
            transition-transform hover:scale-105 active:scale-95
            h-12 w-12          
            md:h-14 md:w-14
          "
        >
          <PlusCircle className="
            h-6 w-6
            md:h-12 md:w-12
            stroke-[2.5] 

          " />
        </Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-md"> 
        <DialogHeader className='gap-0'>
          <DialogTitle className="text-2xl font-bold tracking-tight">Tambah Antrian Baru</DialogTitle>
          <DialogDescription >
            Pilih metode input manual atau otomatis.
          </DialogDescription>
        </DialogHeader>

        {/* STRUKTUR BARU DI SINI */}
        <Tabs defaultValue="manual" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="manual">Manual</TabsTrigger>
            <TabsTrigger value="otomatis">Otomatis</TabsTrigger>
          </TabsList>
          
          {/* 2. Card membungkus SEMUA TabsContent */}
          <Card className="mt-4">
            <TabsContent value="manual" className="mt-0">
              <ManualTabContent />
            </TabsContent>
            <TabsContent value="otomatis" className="mt-0">
              <OtomatisTabContent />
            </TabsContent>
          </Card>
        </Tabs>
        
        <DialogFooter>
          <DialogClose asChild>
            <Button type="button" variant="outline">
              Batal
            </Button>
          </DialogClose>
          <Button type="submit" className="bg-primary hover:bg-primary/90 text-primary-foreground">
            Simpan Perubahan
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default QueuesectionModal