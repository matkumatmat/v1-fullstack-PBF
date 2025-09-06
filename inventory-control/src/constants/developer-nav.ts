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
    title: 'Config',
    url: '/developer/config',
    icon: 'product',
    shortcut: ['p', 'p'],
    isActive: false,
    items: [],
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
      }
    ]
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
