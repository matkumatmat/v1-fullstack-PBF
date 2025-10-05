// src/components/testing/filtering-testing.tsx

"use client";

import * as React from "react";
import { Check, ChevronsUpDown, Building, MapPin } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { CustomerLookup, BranchLookup, LocationLookup } from "@/lib/lookup/location-filtering";

type SearchableItem = 
  | { type: 'branch'; name: string; id: string; }
  | { type: 'location'; data: LocationLookup; parentBranchName: string; };

function flattenBranchesForSearch(branches: BranchLookup[]): SearchableItem[] {
  const items: SearchableItem[] = [];
  function recurse(branchList: BranchLookup[], depth = 0) {
    for (const branch of branchList) {
      items.push({ type: 'branch', name: `${'—'.repeat(depth)} ${branch.name}`, id: branch.public_id });
      for (const location of branch.locations) {
        items.push({ type: 'location', data: location, parentBranchName: branch.name });
      }
      if (branch.children && branch.children.length > 0) {
        recurse(branch.children, depth + 1);
      }
    }
  }
  recurse(branches);
  return items;
}

function findBranchForLocation(branches: BranchLookup[], locationId: string): BranchLookup | null {
  for (const branch of branches) {
    if (branch.locations.some(loc => loc.public_id === locationId)) {
      return branch;
    }
    if (branch.children && branch.children.length > 0) {
      const foundInChild = findBranchForLocation(branch.children, locationId);
      if (foundInChild) return foundInChild;
    }
  }
  return null;
}

function processLocationDetails(
  locationDetails: any, 
  allCustomers: CustomerLookup[]
): object {

  // 1. Dapatkan nama branch
  let branchName = "Branch tidak ditemukan";
  for (const customer of allCustomers) {
    const foundBranch = findBranchForLocation(customer.branches, locationDetails.public_id);
    if (foundBranch) {
      branchName = foundBranch.name;
      break;
    }
  }

  // 2. Dapatkan ID dan Nama Lokasi
  const locations_id = locationDetails.public_id;
  const tujuan_kirim = locationDetails.name;
  const province = locationDetails.state_province || ""; // Langsung ambil, beri fallback string kosong

  // 3. Logika manipulasi alamat (line 1, 2, 3)
  const fullAddress = [
    locationDetails.addr_line_1, 
    locationDetails.addr_line_2, 
    locationDetails.addr_line_3
  ].filter(Boolean).join(' ').trim(); // Gabungkan semua baris alamat yang tidak kosong  

  let line_1 = "";
  let line_2 = "";
  let line_3 = "";
  const maxLength = 51;

  if (fullAddress.length > 0) {
    if (fullAddress.length <= maxLength) {
      line_1 = fullAddress;
    } else {
      line_1 = fullAddress.substring(0, maxLength - 1) + "-";
      const remaining_after_1 = fullAddress.substring(maxLength - 1);

      if (remaining_after_1.length <= maxLength) {
        line_2 = remaining_after_1;
      } else {
        line_2 = remaining_after_1.substring(0, maxLength - 1) + "-";
        const remaining_after_2 = remaining_after_1.substring(maxLength - 1);
        
        // Sisa alamat dimasukkan ke line_3 tanpa pemotongan lebih lanjut
        line_3 = remaining_after_2; 
      }
    }
  }

    let pic = "";
  const picName = locationDetails.location_pic;
  const picContact = locationDetails.location_pic_contact;
  
  if (picName) {
    pic = picName;
    if (picContact) {
      pic += ` (${picContact})`; // Tambahkan kontak jika ada
    }
  } else if (picContact) {
    pic = picContact; // Jika hanya kontak yang ada
  }

  return {
    branches: branchName,
    locations_id,
    tujuan_kirim,
    line_1,
    line_2,
    line_3,
    pic,      // <-- TAMBAHKAN INI
    province, // <-- TAMBAHKAN INI    
  };
}

export default function FilteringTesting({ onDataManipulated }: { onDataManipulated: (data: object | null) => void }) {
    const [allData, setAllData] = React.useState<CustomerLookup[]>([]);
    const [isLoading, setIsLoading] = React.useState(true);
    const [error, setError] = React.useState<string | null>(null);

    const [selectedCustomerId, setSelectedCustomerId] = React.useState<string | null>(null);
    const [selectedLocation, setSelectedLocation] = React.useState<LocationLookup | null>(null);

    const [locationDetails, setLocationDetails] = React.useState<any | null>(null);
    const [isDetailsLoading, setIsDetailsLoading] = React.useState(false);
    const [detailsError, setDetailsError] = React.useState<string | null>(null);

    const [openCombobox, setOpenCombobox] = React.useState(false);
    const [manipulatedData, setManipulatedData] = React.useState<object | null>(null);


    React.useEffect(() => {
        async function fetchLookupData() {
        setIsLoading(true);
        setError(null);
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL;
            if (!apiUrl) throw new Error("API_URL tidak diset di environment variables.");
            const response = await fetch(`${apiUrl}/api/v1/customer/customers/lookup/all`);
            if (!response.ok) throw new Error(`Gagal mengambil data lookup: ${response.statusText}`);
            const data: CustomerLookup[] = await response.json();
            setAllData(data);
        } catch (err: any) {
            setError(err.message || "Terjadi kesalahan yang tidak diketahui.");
        } finally {
            setIsLoading(false);
        }
        }
        fetchLookupData();
    }, []);

    React.useEffect(() => {
        // ==========================================================
        // INI BAGIAN YANG DIPERBAIKI DENGAN STRUKTUR BARU
        // ==========================================================
        
        // Definisikan fungsi async di luar, yang menerima parameter
        // dengan tipe yang jelas (bukan null).
        const fetchLocationDetails = async (location: LocationLookup) => {
        setIsDetailsLoading(true);
        setDetailsError(null);
        setLocationDetails(null);
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL;
            if (!apiUrl) throw new Error("API_URL tidak diset.");
            
            // Sekarang TypeScript 100% yakin `location` punya `public_id`
            const response = await fetch(`${apiUrl}/api/v1/customer/customers/locations/${location.public_id}`);
            if (!response.ok) throw new Error(`Gagal mengambil detail lokasi: ${response.status} ${response.statusText}`);

            const detailsData = await response.json();
            setLocationDetails(detailsData);
        } catch (err: any) {
            setDetailsError(err.message || "Gagal memuat detail lokasi.");
        } finally {
            setIsDetailsLoading(false);
        }
        };

        // Logika kondisional:
        if (selectedLocation) {
        // Jika ada lokasi, panggil fungsi fetch dengan lokasi tersebut sebagai argumen.
        fetchLocationDetails(selectedLocation);
        } else {
        // Jika tidak ada lokasi (null), reset state.
        setLocationDetails(null);
        setDetailsError(null);
        setIsDetailsLoading(false); // Pastikan loading juga false
        }
    }, [selectedLocation]); 

    React.useEffect(() => {
    if (locationDetails && allData.length > 0) {
        const processedData = processLocationDetails(locationDetails, allData);
        setManipulatedData(processedData);
        onDataManipulated(processedData); // <-- TAMBAHKAN BARIS INI
    } else {
        setManipulatedData(null);
        onDataManipulated(null); // <-- TAMBAHKAN BARIS INI
    }
    }, [locationDetails, allData, onDataManipulated]); // Tambahkan onDataManipulated ke dependency array

  const selectedCustomer = React.useMemo(() => 
    allData.find(c => c.public_id === selectedCustomerId)
  , [allData, selectedCustomerId]);

  const searchableItems = React.useMemo(() => {
    if (!selectedCustomer) return [];
    return flattenBranchesForSearch(selectedCustomer.branches);
  }, [selectedCustomer]);

  const handleCustomerChange = (customerId: string) => {
    setSelectedCustomerId(customerId);
    setSelectedLocation(null); 
  };

  if (isLoading) return <p>Memuat data filter...</p>;
  if (error) return <p className="text-destructive">Error: {error}</p>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="w-full sm:w-64">
          <Select onValueChange={handleCustomerChange} defaultValue={selectedCustomerId ?? undefined}>
            <SelectTrigger><SelectValue placeholder="Pilih Customer" /></SelectTrigger>
            <SelectContent>
              {allData.map(customer => (<SelectItem key={customer.public_id} value={customer.public_id}>{customer.name}</SelectItem>))}
            </SelectContent>
          </Select>
        </div>
        <div className="w-full sm:w-80">
          <Popover open={openCombobox} onOpenChange={setOpenCombobox}>
            <PopoverTrigger asChild>
              <Button variant="outline" role="combobox" className="w-full justify-between" disabled={!selectedCustomerId}>
                {selectedLocation ? selectedLocation.name : "Pilih Cabang / Lokasi..."}
                <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[320px] p-0" align="start">
              <Command>
                <CommandInput placeholder="Cari cabang atau lokasi..." />
                <CommandList>
                  <CommandEmpty>Tidak ada hasil.</CommandEmpty>
                  <CommandGroup>
                    {searchableItems.map((item) => {
                      if (item.type === 'location') {
                        return (
                          <CommandItem key={item.data.public_id} value={`${item.data.name} ${item.parentBranchName}`} onSelect={() => { setSelectedLocation(item.data); setOpenCombobox(false); }}>
                            <Check className={cn("mr-2 h-4 w-4", selectedLocation?.public_id === item.data.public_id ? "opacity-100" : "opacity-0")} />
                            <div className="flex items-center"><MapPin className="mr-2 h-4 w-4 text-muted-foreground" /><div className="flex flex-col"><span>{item.data.name}</span><span className="text-xs text-muted-foreground">{item.parentBranchName}</span></div></div>
                          </CommandItem>
                        );
                      } else {
                        return (<div key={item.id} className="px-2 py-1.5 text-sm font-semibold flex items-center text-muted-foreground"><Building className="mr-2 h-4 w-4" /> {item.name}</div>);
                      }
                    })}
                  </CommandGroup>
                </CommandList>
              </Command>
            </PopoverContent>
          </Popover>
        </div>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Data Lookup Terpilih</CardTitle>
          <CardDescription>Ini adalah data ringan dari hasil filter pertama.</CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="p-4 bg-muted rounded-md overflow-x-auto text-sm">{selectedLocation ? JSON.stringify(selectedLocation, null, 2) : "Belum ada lokasi yang dipilih."}</pre>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Data Detail Lengkap Lokasi</CardTitle>
          {/* CardDescription ini adalah teks statis, errornya bukan dari sini */}
          <CardDescription>Ini adalah hasil fetch dari endpoint `/locations/&#123;public_id&#125;`.</CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="p-4 bg-muted rounded-md overflow-x-auto text-sm">
            {isDetailsLoading && "Memuat detail..."}
            {detailsError && <span className="text-destructive">Error: {detailsError}</span>}
            {locationDetails && JSON.stringify(locationDetails, null, 2)}
            {!isDetailsLoading && !detailsError && !locationDetails && "Pilih sebuah lokasi untuk melihat detail lengkapnya."}
          </pre>
        </CardContent>
      </Card>

      {/* Card 3: Menampilkan Hasil Manipulasi */}
      <Card>
        <CardHeader>
          <CardTitle>Hasil Manipulasi String</CardTitle>
          <CardDescription>
            Ini adalah objek JSON yang dihasilkan dari logika pemrosesan.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="p-4 bg-muted rounded-md overflow-x-auto text-sm">
            {manipulatedData 
              ? JSON.stringify(manipulatedData, null, 2) 
              : "Pilih sebuah lokasi untuk melihat hasil manipulasi."}
          </pre>
        </CardContent>
      </Card>      
    </div>
  );
}

