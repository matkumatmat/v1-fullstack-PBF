// src/components/ui/outlined-input.tsx

import * as React from "react"
// BENAR
import { Input } from "@/components/ui/input"
type InputProps = React.ComponentProps<"input">

import { Label } from "@/components/ui/label"
import { cn } from "@/lib/utils"

// Definisikan props baru yang menyertakan 'label'
export interface OutlinedInputProps extends InputProps {
  label: string;
}

const OutlinedInput = React.forwardRef<HTMLInputElement, OutlinedInputProps>(
  ({ className, label, id, ...props }, ref) => {
    // Gunakan id yang diberikan atau buat id unik untuk menghubungkan label dan input
    const inputId = id || React.useId();

    return (
      // 1. Container harus relative untuk positioning label
      <div className="relative">
        <Input
          // 2. Gunakan 'peer' agar label bisa mendeteksi state input (focus, valid, etc.)
          className={cn(
            "peer h-10 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm placeholder:text-transparent focus:outline-none focus:ring-1 focus:ring-ring focus:ring-offset-0.5 disabled:cursor-not-allowed disabled:opacity-50",
            className
          )}
          ref={ref}
          id={inputId}
          placeholder={label} // Trik: placeholder harus ada, tapi kita buat transparan
          {...props}
        />
        <Label
          htmlFor={inputId}
          // 3. Styling label dengan transisi dan positioning
          className="
            absolute 
            left-3 
            top-2
            -translate-y-4.5
            scale-75
            origin-[0] 
            transform 
            cursor-text 
            bg-inherit 
            px-1 
            text-sm 
            text-muted-foreground 
            duration-300 
            
            
            peer-placeholder-shown:top-1/2
            peer-placeholder-shown:-translate-y-1/2 
            peer-placeholder-shown:scale-100 

            peer-focus:top-2
            peer-focus:-translate-y-4.5 
            peer-focus:scale-75 
            peer-focus:text-white
          "
        >
          {label}
        </Label>
      </div>
    );
  }
);
OutlinedInput.displayName = "OutlinedInput";

export { OutlinedInput };