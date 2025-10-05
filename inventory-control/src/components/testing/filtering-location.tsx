// components/testing/filtering-location.tsx

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

function processLocationDetails(locationDetails: any, allCustomers: CustomerLookup[]): object {
  let branchName = "Branch tidak ditemukan";
  for (const customer of allCustomers) {
    const foundBranch = findBranchForLocation(customer.branches, locationDetails.public_id);
    if (foundBranch) {
      branchName = foundBranch.name;
      break;
    }
  }

  const locations_id = locationDetails.public_id;
  const tujuan_kirim = locationDetails.name;
  const province = locationDetails.state_province || "";

  const fullAddress = [
    locationDetails.addr_line_1, 
    locationDetails.addr_line_2, 
    locationDetails.addr_line_3
  ].filter(Boolean).join(' ').trim();  

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
        line_3 = remaining_after_2; 
      }
    }
  }

  let pic = "";
  const picName = locationDetails.location_pic;
  const picContact = locationDetails.location_pic_contact;
  if (picName) {
    pic = picName;
    if (picContact) pic += ` (${picContact})`;
  } else if (picContact) {
    pic = picContact;
  }

  return { branches: branchName, locations_id, tujuan_kirim, line_1, line_2, line_3, pic, province };
}

export default function FilteringLocation({ onDataManipulated }: { onDataManipulated: (data: object | null) => void }) {
    const [allData, setAllData] = React.useState<CustomerLookup[]>([]);
    const [isLoading, setIsLoading] = React.useState(true);
    const [error, setError] = React.useState<string | null>(null);
    const [selectedCustomerId, setSelectedCustomerId] = React.useState<string | null>(null);
    const [selectedLocation, setSelectedLocation] = React.useState<LocationLookup | null>(null);
    const [locationDetails, setLocationDetails] = React.useState<any | null>(null);
    const [openCombobox, setOpenCombobox] = React.useState(false);

    React.useEffect(() => {
        async function fetchLookupData() {
            setIsLoading(true);
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL;
                if (!apiUrl) throw new Error("API_URL tidak diset.");
                const response = await fetch(`${apiUrl}/api/v1/customer/customers/lookup/all`);
                if (!response.ok) throw new Error(`Gagal mengambil data lookup: ${response.statusText}`);
                const data: CustomerLookup[] = await response.json();
                setAllData(data);
            } catch (err: any) { setError(err.message || "Terjadi kesalahan."); } 
            finally { setIsLoading(false); }
        }
        fetchLookupData();
    }, []);

    React.useEffect(() => {
        const fetchLocationDetails = async (location: LocationLookup) => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL;
                if (!apiUrl) throw new Error("API_URL tidak diset.");
                const response = await fetch(`${apiUrl}/api/v1/customer/customers/locations/${location.public_id}`);
                if (!response.ok) throw new Error(`Gagal mengambil detail lokasi: ${response.statusText}`);
                const detailsData = await response.json();
                setLocationDetails(detailsData);
            } catch (err: any) { console.error(err); }
        };
        if (selectedLocation) { fetchLocationDetails(selectedLocation); } 
        else { setLocationDetails(null); }
    }, [selectedLocation]); 

    React.useEffect(() => {
        if (locationDetails && allData.length > 0) {
            const processedData = processLocationDetails(locationDetails, allData);
            onDataManipulated(processedData);
        } else {
            onDataManipulated(null);
        }
    }, [locationDetails, allData, onDataManipulated]);

    const selectedCustomer = React.useMemo(() => allData.find(c => c.public_id === selectedCustomerId), [allData, selectedCustomerId]);
    const searchableItems = React.useMemo(() => { if (!selectedCustomer) return []; return flattenBranchesForSearch(selectedCustomer.branches); }, [selectedCustomer]);
    const handleCustomerChange = (customerId: string) => { setSelectedCustomerId(customerId); setSelectedLocation(null); };

    if (isLoading) return <Card><CardHeader><CardTitle>Tahap 1: Pilih Lokasi Tujuan</CardTitle></CardHeader><CardContent><p>Memuat data filter...</p></CardContent></Card>;
    if (error) return <Card><CardHeader><CardTitle>Error</CardTitle></CardHeader><CardContent><p className="text-destructive">{error}</p></CardContent></Card>;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Tahap 1: Pilih Lokasi Tujuan</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col sm:flex-row gap-4">
                    <div className="w-full sm:w-64">
                        <Select onValueChange={handleCustomerChange} defaultValue={selectedCustomerId ?? undefined}>
                            <SelectTrigger><SelectValue placeholder="Pilih Customer" /></SelectTrigger>
                            <SelectContent>{allData.map(customer => (<SelectItem key={customer.public_id} value={customer.public_id}>{customer.name}</SelectItem>))}</SelectContent>
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
                                                    return (<CommandItem key={item.data.public_id} value={`${item.data.name} ${item.parentBranchName}`} onSelect={() => { setSelectedLocation(item.data); setOpenCombobox(false); }}><Check className={cn("mr-2 h-4 w-4", selectedLocation?.public_id === item.data.public_id ? "opacity-100" : "opacity-0")} /><div className="flex items-center"><MapPin className="mr-2 h-4 w-4 text-muted-foreground" /><div className="flex flex-col"><span>{item.data.name}</span><span className="text-xs text-muted-foreground">{item.parentBranchName}</span></div></div></CommandItem>);
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
            </CardContent>
        </Card>
    );
}