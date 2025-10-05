// src/components/layout/tanstack-query-provider.tsx
'use client';

import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

export default function TanstackQueryProvider({ children }: { children: React.ReactNode }) {
  // Gunakan useState untuk memastikan QueryClient hanya dibuat sekali
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        // Opsi default yang bagus untuk produksi
        staleTime: 60 * 1000, // 1 menit
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {/* Devtools sangat membantu saat development */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}