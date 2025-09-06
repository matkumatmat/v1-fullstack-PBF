import { z } from 'zod';

// Definisikan tipe untuk setiap field
export interface FieldConfig {
  key: string;
  label: string;
  type: 'text' | 'number' | 'textarea' | 'boolean' | 'decimal' |'datetime' | 'date';
  validation: z.ZodTypeAny;
  placeholder?: string;
  group?: string; // Properti untuk mengelompokkan field dalam satu baris
}

// "Kamus" utama untuk semua tipe konfigurasi
// Dioptimalkan dengan properti 'group' untuk layout form yang lebih baik.
export const configMetadata: Record<string, FieldConfig[]> = {
  status_types: [
    { key: 'entity_type', label: 'Entity Type', type: 'text', validation: z.string().min(1, "Entity Type is required"), placeholder: 'e.g., SO, SHIPMENT' },
    { key: 'sort_order', label: 'Sort Order', type: 'number', validation: z.coerce.number().int().default(0), group: 'timing' },
    { key: 'auto_transition_after_hours', label: 'Auto Transition (Hours)', type: 'number', validation: z.coerce.number().int().positive('Must be a positive number').optional().nullable(), group: 'timing' },
    { key: 'color_code', label: 'Color Code', type: 'text', validation: z.string().optional().nullable(), placeholder: '#4CAF50', group: 'styling' },
    { key: 'icon', label: 'Icon', type: 'text', validation: z.string().optional().nullable(), placeholder: 'icon-check-circle', group: 'styling' },
    { key: 'css_class', label: 'CSS Class', type: 'text', validation: z.string().optional().nullable(), placeholder: 'status-success', group: 'styling' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'is_initial_status', label: 'Initial Status', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_final_status', label: 'Final Status', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_error_status', label: 'Error Status', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'requires_approval', label: 'Requires Approval', type: 'boolean', validation: z.boolean().default(false), group: 'behavior' },
    { key: 'sends_notification', label: 'Sends Notification', type: 'boolean', validation: z.boolean().default(false), group: 'behavior' },
  ],
  priority_levels:  [
    { key: 'level', label: 'Level', type: 'number', validation: z.coerce.number().int().min(1, 'Level must be at least 1') },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true) },
    { key: 'sla_hours', label: 'SLA (Hours)', type: 'number', validation: z.coerce.number().int().positive('SLA must be positive').optional().nullable(), group: 'timing' },
    { key: 'escalation_hours', label: 'Escalation (Hours)', type: 'number', validation: z.coerce.number().int().positive('Escalation hours must be positive').optional().nullable(), group: 'timing' },
    { key: 'color_code', label: 'Color Code', type: 'text', validation: z.string().optional().nullable(), placeholder: '#FF0000', group: 'styling' },
    { key: 'icon', label: 'Icon', type: 'text', validation: z.string().optional().nullable(), placeholder: 'icon-priority-high', group: 'styling' },
  ],
  packaging_materials: [
    { key: 'material_type', label: 'Material Type', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., BOX, BUBBLE_WRAP' },
    { key: 'length_cm', label: 'Length (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'width_cm', label: 'Width (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'height_cm', label: 'Height (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'weight_g', label: 'Weight (g)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'metrics' },
    { key: 'cost_per_unit', label: 'Cost per Unit', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format. e.g., 12.34" }).optional().nullable(), group: 'metrics' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'is_reusable', label: 'Reusable', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_fragile_protection', label: 'Fragile Protection', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_temperature_protection', label: 'Temperature Protection', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
  ],
  temperature_types: [
    { key: 'min_celsius', label: 'Min Temp (°C)', type: 'number', validation: z.coerce.number().optional().nullable(), group: 'temperature' },
    { key: 'max_celsius', label: 'Max Temp (°C)', type: 'number', validation: z.coerce.number().optional().nullable(), group: 'temperature' },
    { key: 'optimal_celsius', label: 'Optimal Temp (°C)', type: 'number', validation: z.coerce.number().optional().nullable(), group: 'temperature' },
    { key: 'celsius_display', label: 'Display Temp', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., 2-8°C', group: 'display' },
    { key: 'humidity_range', label: 'Humidity Range', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., 40-60%', group: 'display' },
    { key: 'color_code', label: 'Color Code', type: 'text', validation: z.string().optional().nullable(), placeholder: '#3498DB', group: 'styling' },
    { key: 'icon', label: 'Icon', type: 'text', validation: z.string().optional().nullable(), placeholder: 'icon-thermometer', group: 'styling' },
    { key: 'special_storage_requirements', label: 'Special Storage Requirements', type: 'textarea', validation: z.string().optional().nullable() },
  ],
  product_types:  [
    { key: 'sort_order', label: 'Sort Order', type: 'number', validation: z.coerce.number().int().default(0) },
  ],
  package_types:  [
    { key: 'max_stack_height', label: 'Max Stack Height', type: 'number', validation: z.coerce.number().int().positive('Must be a positive number').optional().nullable() },
    { key: 'is_fragile', label: 'Fragile', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_stackable', label: 'Stackable', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'special_handling_required', label: 'Requires Special Handling', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'handling_instructions', label: 'Handling Instructions', type: 'textarea', validation: z.string().optional().nullable() },
  ],
  allocation_types:[
    { key: 'color_code', label: 'Color Code', type: 'text', validation: z.string().optional().nullable(), placeholder: '#A569BD', group: 'styling' },
    { key: 'icon', label: 'Icon', type: 'text', validation: z.string().optional().nullable(), placeholder: 'icon-sort-numeric-asc', group: 'styling' },
  ],
  sector_types:  [
    { key: 'default_payment_terms', label: 'Default Payment Terms (Days)', type: 'number', validation: z.coerce.number().int().positive('Must be a positive number').optional().nullable(), group: 'defaults' },
    { key: 'default_delivery_terms', label: 'Default Delivery Terms', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., FOB, CIF', group: 'defaults' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'requires_special_handling', label: 'Requires Special Handling', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'requires_temperature_monitoring', label: 'Requires Temp. Monitoring', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'requires_chain_of_custody', label: 'Requires Chain of Custody', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'special_documentation', label: 'Special Documentation', type: 'textarea', validation: z.string().optional().nullable() },
  ],
  customer_types:  [
    { key: 'default_credit_limit', label: 'Default Credit Limit', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format. e.g., 10000.00" }).optional().nullable(), group: 'financials' },
    { key: 'default_discount_percent', label: 'Default Discount (%)', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format. e.g., 5.50" }).optional().nullable(), group: 'financials' },
    { key: 'default_payment_terms_days', label: 'Default Payment Terms (Days)', type: 'number', validation: z.coerce.number().int().default(30), group: 'financials' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'allows_tender_allocation', label: 'Allows Tender Allocation', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'requires_pre_approval', label: 'Requires Pre-Approval', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
  ],
  document_types:  [
    { key: 'max_file_size_mb', label: 'Max File Size (MB)', type: 'number', validation: z.coerce.number().int().positive('Must be a positive number').default(10), group: 'file_specs' },
    { key: 'allowed_extensions', label: 'Allowed Extensions', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., .pdf,.jpg,.png', group: 'file_specs' },
    { key: 'template_path', label: 'Template Path', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., /templates/invoice.html' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'is_mandatory', label: 'Mandatory', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_customer_visible', label: 'Customer Visible', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'auto_generate', label: 'Auto Generate', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
  ],
  location_types: [
    { key: 'max_weight_capacity_kg', label: 'Max Weight Capacity (kg)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable() },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'type_flags' },
    { key: 'is_storage_location', label: 'Storage Location', type: 'boolean', validation: z.boolean().default(true), group: 'type_flags' },
    { key: 'is_picking_location', label: 'Picking Location', type: 'boolean', validation: z.boolean().default(true), group: 'type_flags' },
    { key: 'is_staging_location', label: 'Staging Location', type: 'boolean', validation: z.boolean().default(false), group: 'type_flags' },
    { key: 'supports_temperature_control', label: 'Supports Temp. Control', type: 'boolean', validation: z.boolean().default(false), group: 'capability_flags' },
    { key: 'requires_special_access', label: 'Requires Special Access', type: 'boolean', validation: z.boolean().default(false), group: 'capability_flags' },
  ],
  packaging_box_types: [
    { key: 'material_type', label: 'Material Type', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., CARDBOARD, PLASTIC' },
    { key: 'length_cm', label: 'Length (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'width_cm', label: 'Width (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'height_cm', label: 'Height (cm)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'dimensions' },
    { key: 'weight_g', label: 'Weight (g)', type: 'number', validation: z.coerce.number().positive('Must be a positive number').optional().nullable(), group: 'metrics' },
    { key: 'cost_per_unit', label: 'Cost per Unit', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format. e.g., 12.34" }).optional().nullable(), group: 'metrics' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'flags' },
    { key: 'is_reusable', label: 'Reusable', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_fragile_protection', label: 'Fragile Protection', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
    { key: 'is_temperature_protection', label: 'Temperature Protection', type: 'boolean', validation: z.boolean().default(false), group: 'flags' },
  ],
  product_prices:  [
    { key: 'product_id', label: 'Product ID', type: 'number', validation: z.coerce.number().int().positive('Product ID is required'), group: 'identity' },
    { key: 'effective_date', label: 'Effective Date', type: 'date', validation: z.coerce.date({ required_error: "Effective date is required" }), group: 'identity' },
    { key: 'HNA', label: 'HNA', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format" }).optional().nullable(), group: 'prices' },
    { key: 'HJP', label: 'HJP', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format" }).optional().nullable(), group: 'prices' },
    { key: 'HET', label: 'HET', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format" }).optional().nullable(), group: 'prices' },
  ],
  movement_types: [
    { key: 'direction', label: 'Direction', type: 'text', validation: z.string().min(1, "Direction is required"), placeholder: 'e.g., IN, OUT, INTERNAL', group: 'details' },
    { key: 'document_prefix', label: 'Document Prefix', type: 'text', validation: z.string().optional().nullable(), placeholder: 'e.g., GRN-, GI-', group: 'details' },
    { key: 'auto_generate_document', label: 'Auto Generate Document', type: 'boolean', validation: z.boolean().default(false) },
  ],
  notification_types:  [
    { key: 'retry_count', label: 'Retry Count', type: 'number', validation: z.coerce.number().int().default(3), group: 'retry' },
    { key: 'retry_interval_minutes', label: 'Retry Interval (Minutes)', type: 'number', validation: z.coerce.number().int().default(5), group: 'retry' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'channels' },
    { key: 'is_email_enabled', label: 'Email Enabled', type: 'boolean', validation: z.boolean().default(true), group: 'channels' },
    { key: 'is_sms_enabled', label: 'SMS Enabled', type: 'boolean', validation: z.boolean().default(false), group: 'channels' },
    { key: 'is_push_enabled', label: 'Push Enabled', type: 'boolean', validation: z.boolean().default(true), group: 'channels' },
    { key: 'is_system_notification', label: 'System Notification', type: 'boolean', validation: z.boolean().default(true), group: 'channels' },
    { key: 'email_template', label: 'Email Template', type: 'textarea', validation: z.string().optional().nullable() },
    { key: 'sms_template', label: 'SMS Template', type: 'textarea', validation: z.string().optional().nullable() },
    { key: 'push_template', label: 'Push Template', type: 'textarea', validation: z.string().optional().nullable() },
  ],
  delivery_types:[
    { key: 'estimated_days', label: 'Estimated Days', type: 'number', validation: z.coerce.number().int().positive('Must be a positive number').optional().nullable(), group: 'details' },
    { key: 'is_active', label: 'Active', type: 'boolean', validation: z.boolean().default(true), group: 'details' },
    { key: 'cost_per_kg', label: 'Cost per kg', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format" }).optional().nullable(), group: 'costing' },
    { key: 'cost_per_km', label: 'Cost per km', type: 'decimal', validation: z.string().refine((val) => !val || /^\d+(\.\d{1,2})?$/.test(val), { message: "Invalid decimal format" }).optional().nullable(), group: 'costing' },
  ],
};

// Fungsi helper untuk mendapatkan metadata, dengan fallback ke array kosong
export const getMetadataForType = (type: string): FieldConfig[] => {
  return configMetadata[type] || [];
};