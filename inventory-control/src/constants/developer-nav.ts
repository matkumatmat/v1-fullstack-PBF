import { NavItem } from '@/types';

//Info: The following data is used for the sidebar navigation and Cmd K bar.
export const navItems: NavItem[] = [
  {
    title: 'Dashboard',
    url: '/developer/dashboard/overview',
    icon: 'dashboard',
    isActive: false,
    shortcut: ['d', 'd'],
    items: [] // Empty array as there are no child items for Dashboard
  },
  {
    title: 'Sales',
    url: '/developer',
    icon: 'product',
    shortcut: ['p', 'p'],
    isActive: false,
    items: [
      {
        title: 'Sales Order',
        url: '/developer/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Packing Slip',
        url: '/developer/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Customer',
        url: '/developer/reports',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
    ] // No child items
  },
  {
    title: 'Product',
    url: '/developer/dashboard/product',
    icon: 'product',
    shortcut: ['p', 'p'],
    isActive: false,
    items: [
      {
        title: 'Inbound',
        url: '/developer/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Outbound',
        url: '/developer/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Reports',
        url: '/developer/reports',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
    ] // No child items
  },
  {
    title: 'Shipment',
    url: '#', // Placeholder as there is no direct link for the parent
    icon: 'billing',
    isActive: true,

    items: [
      {
        title: 'Shipping Plan',
        url: '/developer/dashboard/profile',
        icon: 'userPen',
        shortcut: ['m', 'm']
      },
      {
        title: 'Shipment',
        shortcut: ['l', 'l'],
        url: '/developer',
        icon: 'login'
      },
      {
        title: 'Packing',
        shortcut: ['l', 'l'],
        url: '/developer',
        icon: 'login'
      },
    ]
  },
  {
    title: 'Document',
    url: '#', // Placeholder as there is no direct link for the parent
    icon: 'billing',
    isActive: true,

    items: [
      {
        title: 'Import',
        url: '/developer/dashboard/profile',
        icon: 'userPen',
        shortcut: ['m', 'm']
      },
      {
        title: 'Export',
        shortcut: ['l', 'l'],
        url: '/developer',
        icon: 'login'
      },
      {
        title: 'Dashboard',
        shortcut: ['l', 'l'],
        url: '/developer/dashboard/document',
        icon: 'login'
      }
    ]
  },
  {
    title: 'Kanban',
    url: '/developer/dashboard/kanban',
    icon: 'kanban',
    shortcut: ['k', 'k'],
    isActive: false,
    items: [] // No child items
  },
  {
    title: 'Label',
    url: '/developer/dashboard/print/label',
    icon: 'kanban',
    shortcut: ['k', 'k'],
    isActive: false,
    items: [] // No child items
  }
];
