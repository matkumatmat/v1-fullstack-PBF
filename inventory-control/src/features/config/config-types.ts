// inventory-control/src/features/config/config-types.ts

// Mendefinisikan struktur objek untuk setiap item di dropdown
interface ConfigType {
  value: string;
  label: string;
}

// Array yang berisi semua tipe konfigurasi yang tersedia
export const configTypes: ConfigType[] = [
  { value: 'status_types', label: 'Status Type' },
  { value: 'priority_levels', label: 'Priority Level' },
  { value: 'packaging_materials', label: 'Packaging Material' },
  { value: 'temperature_types', label: 'Temperature Type' },
  { value: 'document_types', label: 'Document Type' },
  { value: 'allocation_types', label: 'Allocation Type' },
  { value: 'customer_types', label: 'Customer Type' },
  { value: 'delivery_types', label: 'Delivery Type' },
  { value: 'location_types', label: 'Location Type' },
  { value: 'movement_types', label: 'Movement Type' },
  { value: 'notification_types', label: 'Notification Type' },
  { value: 'package_types', label: 'Package Type' },
  { value: 'packaging_box_types', label: 'Packaging Box Type' },
  { value: 'product_prices', label: 'Product Price' },
  { value: 'product_types', label: 'Product Type' },
  { value: 'sector_types', label: 'Sector Type' },
];