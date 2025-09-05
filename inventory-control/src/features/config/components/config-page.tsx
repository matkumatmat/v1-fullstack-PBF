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
import { useEffect, useState } from 'react';
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
  { value: 'product_type', label: 'Product Type' },
  { value: 'customer_type', label: 'Customer Type' },
  { value: 'delivery_type', label: 'Delivery Type' },
  { value: 'document_type', label: 'Document Type' },
  { value: 'location_type', label: 'Location Type' },
  { value: 'movement_type', label: 'Movement Type' },
  { value: 'notification_type', label: 'Notification Type' },
  { value: 'package_type', label: 'Package Type' },
  { value: 'packaging_box_type', label: 'Packaging Box Type' },
  { value: 'packaging_material', label: 'Packaging Material' },
  { value: 'priority_level', label: 'Priority Level' },
  { value: 'product_price', label: 'Product Price' },
  { value: 'sector_type', label: 'Sector Type' },
  { value: 'status_type', label: 'Status Type' },
  { value: 'temperature_type', label: 'Temperature Type' }
];

export default function ConfigPage() {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [data, setData] = useState<ConfigItem[]>([]);
  const [apiClient, setApiClient] = useState<ApiClient | null>(null);

  useEffect(() => {
    if (selectedType) {
      const client = new ApiClient(selectedType);
      setApiClient(client);
      client.getAll().then(setData);
    }
  }, [selectedType]);

  const handleSave = (item: any) => {
    if (apiClient) {
      if (item.id) {
        apiClient.update(item.id, item).then(() => {
          apiClient.getAll().then(setData);
        });
      } else {
        apiClient.create(item).then(() => {
          apiClient.getAll().then(setData);
        });
      }
    }
  };

  const handleDelete = (id: number) => {
    if (apiClient) {
      apiClient.delete(id).then(() => {
        apiClient.getAll().then(setData);
      });
    }
  };

  return (
    <PageContainer>
      <div className='space-y-4'>
        <div className='flex items-center justify-between'>
          <Heading title={`Configuration`} description='Manage application types' />
          <ConfigFormDialog onSave={handleSave} />
        </div>

        <div className='w-full max-w-xs'>
          <Select onValueChange={setSelectedType}>
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
          <ConfigTable data={data} onSave={handleSave} onDelete={handleDelete} />
        )}
      </div>
    </PageContainer>
  );
}
