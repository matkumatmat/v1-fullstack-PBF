// Fixed Config Page with Better Error Handling
// inventory-control/src/features/config/components/config-page.tsx
'use client';

import PageContainer from '@/components/layout/page-container';
import { Heading } from '@/components/ui/heading';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import { useEffect, useState, useCallback } from 'react';
import { toast } from 'sonner'; // Assuming you're using sonner for toast notifications
import { ApiClient } from '../api';
import { ConfigTable } from './config-table';
import { ConfigFormDialog } from './config-form-dialog';

interface ConfigItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  [key: string]: any;
}

const types = [
  { value: 'product_types', label: 'Product Type' },
  { value: 'customer_types', label: 'Customer Type' },
  { value: 'delivery_types', label: 'Delivery Type' },
  { value: 'document_types', label: 'Document Type' },
  { value: 'location_types', label: 'Location Type' },
  { value: 'movement_types', label: 'Movement Type' },
  { value: 'notification_types', label: 'Notification Type' },
  { value: 'package_types', label: 'Package Type' },
  { value: 'packaging_box_types', label: 'Packaging Box Type' },
  { value: 'packaging_materials', label: 'Packaging Material' },
  { value: 'priority_levels', label: 'Priority Level' },
  { value: 'product_prices', label: 'Product Price' },
  { value: 'sector_types', label: 'Sector Type' },
  { value: 'status_types', label: 'Status Type' },
  { value: 'temperature_types', label: 'Temperature Type' }
];

export default function ConfigPage() {
  const [selectedType, setSelectedType] = useState<string>('');
  const [data, setData] = useState<ConfigItem[]>([]);
  const [apiClient, setApiClient] = useState<ApiClient | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = useCallback(async () => {
    if (!apiClient) return;
    
    try {
      setIsLoading(true);
      const result = await apiClient.getAll();
      setData(result);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      toast.error('Failed to load data');
      setData([]);
    } finally {
      setIsLoading(false);
    }
  }, [apiClient]);

  useEffect(() => {
    if (selectedType) {
      const client = new ApiClient(selectedType);
      setApiClient(client);
    } else {
      setApiClient(null);
      setData([]);
    }
  }, [selectedType]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSave = async (item: any) => {
    if (!apiClient) return;

    try {
      if (item.id) {
        await apiClient.update(item.id, item);
        toast.success('Item updated successfully');
      } else {
        await apiClient.create(item);
        toast.success('Item created successfully');
      }
      await fetchData();
    } catch (error) {
      console.error('Failed to save item:', error);
      toast.error('Failed to save item');
      throw error; // Re-throw to handle in the dialog
    }
  };

  const handleDelete = async (id: number) => {
    if (!apiClient) return;

    if (!window.confirm('Are you sure you want to delete this item?')) {
      return;
    }

    try {
      await apiClient.delete(id);
      toast.success('Item deleted successfully');
      await fetchData();
    } catch (error) {
      console.error('Failed to delete item:', error);
      toast.error('Failed to delete item');
    }
  };

  const selectedTypeLabel = types.find(type => type.value === selectedType)?.label;

  return (
    <PageContainer>
      <div className='space-y-4'>
        <div className='flex items-center justify-between'>
          <Heading 
            title={selectedTypeLabel ? `Configuration - ${selectedTypeLabel}` : 'Configuration'} 
            description='Manage application types' 
          />
          {selectedType && (
            <ConfigFormDialog onSave={handleSave} isLoading={isLoading} />
          )}
        </div>

        <div className='w-full max-w-xs'>
          <Select value={selectedType} onValueChange={setSelectedType}>
            <SelectTrigger>
              <SelectValue placeholder='Select a type' />
            </SelectTrigger>
            <SelectContent>
              {types.map((type) => (
                <SelectItem key={type.value} value={type.value}>
                  {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {selectedType && (
          <ConfigTable 
            data={data} 
            onSave={handleSave} 
            onDelete={handleDelete}
            isLoading={isLoading}
          />
        )}
      </div>
    </PageContainer>
  );
}
