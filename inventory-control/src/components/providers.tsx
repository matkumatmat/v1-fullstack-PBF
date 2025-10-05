// src/components/providers.tsx (Versi yang Diperbaiki)
'use client';

import { Toaster } from '@/components/ui/sonner';
import ThemeProvider from '@/components/layout/ThemeToggle/theme-provider';
import { NuqsAdapter } from 'nuqs/adapters/next/app';
import TanstackQueryProvider from '@/components/layout/tanstack-query-provider';
// 1. Impor ActiveThemeProvider dari lokasi yang benar di proyek Anda
import { ActiveThemeProvider } from '@/components/active-theme'; // <-- GANTI PATH INI JIKA PERLU

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <NuqsAdapter>
      <ThemeProvider
        attribute='class'
        defaultTheme='system'
        enableSystem
        disableTransitionOnChange
        enableColorScheme
      >
        {/* 2. Bungkus semuanya dengan ActiveThemeProvider */}
        <ActiveThemeProvider>
          <TanstackQueryProvider>
            <Toaster />
            {children}
          </TanstackQueryProvider>
        </ActiveThemeProvider>
      </ThemeProvider>
    </NuqsAdapter>
  );
}