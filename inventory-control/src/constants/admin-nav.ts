import { NavItem } from '@/types';

//Info: The following data is used for the sidebar navigation and Cmd K bar.
export const navItems: NavItem[] = [
  {
    title: 'Dashboard',
    url: '/admin/dashboard/overview',
    icon: 'dashboard',
    isActive: false,
    shortcut: ['d', 'd'],
    items: [] // Empty array as there are no child items for Dashboard
  },
  {
    title: 'Sales',
    url: '/admin',
    icon: 'product',
    shortcut: ['p', 'p'],
    isActive: false,
    items: [
      {
        title: 'Sales Order',
        url: '/admin/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Packing Slip',
        url: '/admin/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Customer',
        url: '/admin/reports',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
    ] // No child items
  },
  {
    title: 'Product',
    url: '/admin/dashboard/product',
    icon: 'product',
    shortcut: ['p', 'p'],
    isActive: false,
    items: [
      {
        title: 'Inbound',
        url: '/admin/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Outbound',
        url: '/admin/inbound',
        icon: 'userPen',
        shortcut: ['m', 'm']        
      },
      {
        title: 'Reports',
        url: '/admin/reports',
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
        url: '/admin/dashboard/profile',
        icon: 'userPen',
        shortcut: ['m', 'm']
      },
      {
        title: 'Shipment',
        shortcut: ['l', 'l'],
        url: '/admin',
        icon: 'login'
      },
      {
        title: 'Packing',
        shortcut: ['l', 'l'],
        url: '/admin',
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
        url: '/admin/dashboard/profile',
        icon: 'userPen',
        shortcut: ['m', 'm']
      },
      {
        title: 'Export',
        shortcut: ['l', 'l'],
        url: '/admin',
        icon: 'login'
      },
      {
        title: 'Dashboard',
        shortcut: ['l', 'l'],
        url: '/admin/dashboard/document',
        icon: 'login'
      }
    ]
  },
  {
    title: 'User',
    url: '#', // Placeholder as there is no direct link for the parent
    icon: 'billing',
    isActive: true,

    items: [
      {
        title: 'Employee Management',
        url: '/admin/dashboard/profile',
        icon: 'userPen',
        shortcut: ['m', 'm']
      },
      {
        title: 'Overtime management',
        shortcut: ['l', 'l'],
        url: '/admin',
        icon: 'login'
      }
    ]
  },
  {
    title: 'Kanban',
    url: '/admin/dashboard/kanban',
    icon: 'kanban',
    shortcut: ['k', 'k'],
    isActive: false,
    items: [] // No child items
  },
  {
    title: 'Label',
    url: '/admin/dashboard/print/label',
    icon: 'kanban',
    shortcut: ['k', 'k'],
    isActive: false,
    items: [] // No child items
  }
];
