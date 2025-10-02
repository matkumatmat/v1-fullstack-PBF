"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

// ini adjust ya
const customer = [
  { value: "kftd", label: "KIMIA FARMA" },
  { value: "ppi", label: "PERUSAHAAN PERDAGANGAN INDONESIA" },
  { value: "mup", label: "MERAPI UTAMA PHARMA" },
]

export function CustomerComboBox() {
  const [open, setOpen] = React.useState(false)
  const [value, setValue] = React.useState("")

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between h-10 font-normal"
        >
          {value
            ? customer.find((customer) => customer.value === value)?.label
            : "customer..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[--radix-popover-trigger-width] p-0">
        <Command>
          <CommandInput placeholder="Cari satuan..." />
          <CommandEmpty>customer tidak ditemukan.</CommandEmpty>
          <CommandGroup>
            {customer.map((customer) => (
              <CommandItem
                key={customer.value}
                value={customer.value}
                onSelect={(currentValue) => {
                  setValue(currentValue === value ? "" : currentValue)
                  setOpen(false)
                }}
              >
                <Check
                  className={cn(
                    "mr-2 h-4 w-4",
                    value === customer.value ? "opacity-100" : "opacity-0"
                  )}
                />
                {customer.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  )
}