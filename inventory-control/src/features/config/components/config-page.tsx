'use client';

import PageContainer from '@/components/layout/page-container';
import { Heading } from '@/components/ui/heading';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useEffect, useState, useCallback, useMemo } from 'react';
import { ConfigTable } from './config-table';
import { configTypes } from '../config-types';
import { ApiClient } from '../api/index';
import { ConfigFormDialog } from './config-form-dialog';
import { toast } from 'sonner';

export interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  [key: string]: any;
}

export default function ConfigPage() {
  const [selectedType, setSelectedType] = useState<string>('');
  const [data, setData] = useState<ConfigItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiClient = useMemo(() => {
    if (selectedType) {
      return new ApiClient(selectedType);
    }
    return null;
  }, [selectedType]);

  const fetchData = useCallback(async () => {
    if (!apiClient) return;

    setIsLoading(true);
    setError(null);
    try {
      const result = await apiClient.getAll();
      setData(result);
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch data';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [apiClient]);

  useEffect(() => {
    if (selectedType) {
      fetchData();
    } else {
      setData([]);
    }
  }, [selectedType, fetchData]);

  const handleSave = async (itemData: ConfigItem) => {
    if (!apiClient) return;
    
    try {
      if (itemData.id) {
        await apiClient.update(itemData.id, itemData);
      } else {
        await apiClient.create(itemData);
      }
      toast.success(`Item in ${selectedType} has been saved successfully!`);
      await fetchData();
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to save item.';
      toast.error(errorMessage);
      console.error('Save error:', err);
      throw err;
    }
  };

  const handleDelete = async (id: number) => {
    if (!apiClient) return;
    
    try {
      await apiClient.delete(id);
      toast.success(`Item has been deleted successfully!`);
      await fetchData();
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to delete item.';
      toast.error(errorMessage);
      console.error('Delete error:', err);
    }
  };

  return (
    <PageContainer>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Heading title="Configuration Management" description="Manage various types and settings for the application." />
          {selectedType && (
            <ConfigFormDialog 
              onSave={handleSave} 
              isLoading={isLoading} 
              selectedType={selectedType}
            />
          )}
        </div>

        <Select onValueChange={setSelectedType} value={selectedType}>
          <SelectTrigger className="w-[280px]">
            <SelectValue placeholder="Select a configuration type" />
          </SelectTrigger>
          <SelectContent>
            {/* FIX: Menggunakan `type.value` untuk `key` dan `value` sesuai dengan 
              struktur data di `config-types.ts`.
            */}
            {configTypes.map(type => (
              <SelectItem key={type.value} value={type.value}>
                {type.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {error && !isLoading && <p className="text-red-500">Error: {error}</p>}

        {selectedType && (
          <ConfigTable
            data={data}
            selectedType={selectedType}
            onSave={handleSave}
            onDelete={handleDelete}
            isLoading={isLoading}
          />
        )}
      </div>
    </PageContainer>
  );
}