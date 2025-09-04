'use client';

import PageContainer from '@/components/layout/page-container';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardFooter,
  CardContent,
} from '@/components/ui/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { IconTrendingDown, IconTrendingUp } from '@tabler/icons-react';
import React from 'react';
import { Bar, BarChart, CartesianGrid, XAxis, Area, AreaChart, Pie, PieChart, Cell } from 'recharts';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Calendar as CalendarIcon } from "lucide-react"
import Link from "next/link"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
    ColumnDef,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
    SortingState,
    ColumnFiltersState,
    VisibilityState,
} from "@tanstack/react-table"
import { DataTableColumnHeader } from "@/components/ui/table/data-table-column-header";
import { DataTableViewOptions } from "@/components/ui/table/data-table-view-options";
import { DataTablePagination } from "@/components/ui/table/data-table-pagination";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { addDays, format } from "date-fns"
import { DateRange } from "react-day-picker"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Calendar } from "@/components/ui/calendar"
import { cn } from "@/lib/utils"

// Mock Data
const summaryData = [
  {
    title: 'Total Revenue',
    value: '$67,492.90',
    change: '+25.2%',
    description: 'from last month',
    Icon: IconTrendingUp,
  },
  {
    title: 'New Subscriptions',
    value: '+3,120',
    change: '+190.5%',
    description: 'from last month',
    Icon: IconTrendingUp,
  },
  {
    title: 'Total Sales',
    value: '+15,870',
    change: '+22.8%',
    description: 'from last month',
    Icon: IconTrendingUp,
  },
  {
    title: 'Churn Rate',
    value: '1.2%',
    change: '-0.5%',
    description: 'from last month',
    Icon: IconTrendingDown,
  },
];

const areaChartData = [
  { date: '2024-06-01', revenue: 4500 },
  { date: '2024-06-02', revenue: 4800 },
  { date: '2024-06-03', revenue: 5200 },
  { date: '2024-06-04', revenue: 5000 },
  { date: '2024-06-05', revenue: 5500 },
  { date: '2024-06-06', revenue: 6000 },
  { date: '2024-06-07', revenue: 5800 },
];

const barChartData = [
    { month: 'Jan', sales: 320 },
    { month: 'Feb', sales: 280 },
    { month: 'Mar', sales: 450 },
    { month: 'Apr', sales: 400 },
    { month: 'May', sales: 500 },
    { month: 'Jun', sales: 550 },
];

const pieChartData = [
  { category: 'Laptops', value: 45, fill: 'var(--color-laptops)' },
  { category: 'Desktops', value: 25, fill: 'var(--color-desktops)' },
  { category: 'Tablets', value: 15, fill: 'var(--color-tablets)' },
  { category: 'Accessories', value: 15, fill: 'var(--color-accessories)' },
];


// Chart Components
const ModernAreaChart = () => (
  <Card>
    <CardHeader>
      <CardTitle>Revenue Overview</CardTitle>
      <CardDescription>Total revenue from sales over the last 7 days.</CardDescription>
    </CardHeader>
    <CardContent>
      <ChartContainer config={{}} className='aspect-auto h-[250px] w-full'>
        <AreaChart data={areaChartData}>
          <defs>
            <linearGradient id="fillArea" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="var(--primary)" stopOpacity={0.1}/>
            </linearGradient>
          </defs>
          <CartesianGrid vertical={false} />
          <XAxis dataKey="date" tickLine={false} axisLine={false} tickMargin={8} tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { weekday: 'short' })} />
          <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="dot" />} />
          <Area type="monotone" dataKey="revenue" stroke="var(--primary)" fill="url(#fillArea)" />
        </AreaChart>
      </ChartContainer>
    </CardContent>
  </Card>
);

const ModernBarChart = () => (
  <Card>
    <CardHeader>
      <CardTitle>Monthly Sales</CardTitle>
      <CardDescription>Total sales for the last 6 months.</CardDescription>
    </CardHeader>
    <CardContent>
      <ChartContainer config={{}} className='aspect-auto h-[250px] w-full'>
        <BarChart data={barChartData}>
          <CartesianGrid vertical={false} />
          <XAxis dataKey="month" tickLine={false} axisLine={false} tickMargin={8} />
          <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="dot" />} />
          <Bar dataKey="sales" fill="var(--primary)" radius={4} />
        </BarChart>
      </ChartContainer>
    </CardContent>
  </Card>
);

const ModernPieChart = () => {
    const chartConfig = {
        value: { label: 'Value' },
        laptops: { label: 'Laptops', color: 'hsl(var(--chart-1))' },
        desktops: { label: 'Desktops', color: 'hsl(var(--chart-2))' },
        tablets: { label: 'Tablets', color: 'hsl(var(--chart-3))' },
        accessories: { label: 'Accessories', color: 'hsl(var(--chart-4))' },
    } satisfies ChartConfig;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Sales by Category</CardTitle>
                <CardDescription>Breakdown of sales by product category.</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig} className='aspect-square h-[250px] w-full'>
                    <PieChart>
                        <defs>
                            {pieChartData.map((entry, index) => (
                                <linearGradient key={entry.category} id={`fill${entry.category}`} x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stopColor="var(--primary)" stopOpacity={1 - index * 0.2} />
                                    <stop offset="100%" stopColor="var(--primary)" stopOpacity={0.8 - index * 0.2} />
                                </linearGradient>
                            ))}
                        </defs>
                        <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
                        <Pie 
                            data={pieChartData.map(item => ({...item, fill: `url(#fill${item.category})`}))} 
                            dataKey="value" 
                            nameKey="category" 
                            innerRadius={60} 
                            strokeWidth={2}
                            stroke="var(--background)"
                        />
                    </PieChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
};

const salesOrderData = [
    { SO: "SO-001", PO: "PO-101", poDate: "2024-06-01", customer: "John Doe", product: "Laptop Model X", quantity: 10, value: 10000, quantityRealisation: 10, valueRealisation: 10000, status: "Fulfilled" },
    { SO: "SO-002", PO: "PO-102", poDate: "2024-06-02", customer: "Jane Smith", product: "Desktop Model Y", quantity: 5, value: 7500, quantityRealisation: 0, valueRealisation: 0, status: "Pending" },
    { SO: "SO-003", PO: "PO-103", poDate: "2024-06-03", customer: "Sam Wilson", product: "Tablet Model Z", quantity: 20, value: 8000, quantityRealisation: 10, valueRealisation: 4000, status: "Partial" },
    { SO: "SO-004", PO: "PO-104", poDate: "2024-06-04", customer: "Sara Johnson", product: "Laptop Model X", quantity: 5, value: 5000, quantityRealisation: 0, valueRealisation: 0, status: "Cancelled" },
    { SO: "SO-005", PO: "PO-105", poDate: "2024-06-05", customer: "Michael Brown", product: "Accessories Kit", quantity: 50, value: 2500, quantityRealisation: 50, valueRealisation: 2500, status: "Fulfilled" },
    { SO: "SO-006", PO: "PO-106", poDate: "2024-06-06", customer: "Emily Davis", product: "Desktop Model Y", quantity: 2, value: 3000, quantityRealisation: 0, valueRealisation: 0, status: "Pending" },
    { SO: "SO-007", PO: "PO-107", poDate: "2024-06-07", customer: "Chris Miller", product: "Laptop Model X", quantity: 8, value: 8000, quantityRealisation: 8, valueRealisation: 8000, status: "Fulfilled" },
];

type SalesOrder = typeof salesOrderData[0];

const salesOrderColumns: ColumnDef<SalesOrder>[] = [
    {
        id: "select",
        header: ({ table }) => (
            <Checkbox
                checked={table.getIsAllPageRowsSelected()}
                onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
                aria-label="Select all"
            />
        ),
        cell: ({ row }) => (
            <Checkbox
                checked={row.getIsSelected()}
                onCheckedChange={(value) => row.toggleSelected(!!value)}
                aria-label="Select row"
            />
        ),
        enableSorting: false,
        enableHiding: false,
    },
    { accessorKey: "SO", header: ({ column }) => <DataTableColumnHeader column={column} title="SO" /> },
    { accessorKey: "PO", header: ({ column }) => <DataTableColumnHeader column={column} title="PO" /> },
    { accessorKey: "poDate", header: ({ column }) => <DataTableColumnHeader column={column} title="PO Date" /> },
    { accessorKey: "customer", header: ({ column }) => <DataTableColumnHeader column={column} title="Customer" /> },
    { accessorKey: "product", header: ({ column }) => <DataTableColumnHeader column={column} title="Product" /> },
    { accessorKey: "quantity", header: ({ column }) => <DataTableColumnHeader column={column} title="Quantity" /> },
    { accessorKey: "value", header: ({ column }) => <DataTableColumnHeader column={column} title="Value" /> },
    { accessorKey: "quantityRealisation", header: ({ column }) => <DataTableColumnHeader column={column} title="Qty Realisation" /> },
    { accessorKey: "valueRealisation", header: ({ column }) => <DataTableColumnHeader column={column} title="Value Realisation" /> },
    {
        accessorKey: "status",
        header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
        cell: ({ row }) => {
            const status = row.getValue("status") as string;
            const statusColor =
                status === "Fulfilled" ? "bg-green-500" :
                status === "Pending" ? "bg-yellow-500" :
                status === "Partial" ? "bg-blue-500" :
                "bg-red-500";
            return <Badge className={statusColor}>{status}</Badge>
        }
    },
    {
        id: "actions",
        cell: ({ row }) => {
            const order = row.original
            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem onClick={() => navigator.clipboard.writeText(order.SO)}>
                            Copy SO Number
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>View Details</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]


const SalesOrderTable = () => {
    const [sorting, setSorting] = React.useState<SortingState>([])
    const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
    const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
    const [rowSelection, setRowSelection] = React.useState({})

    const table = useReactTable({
        data: salesOrderData,
        columns: salesOrderColumns,
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        onColumnVisibilityChange: setColumnVisibility,
        onRowSelectionChange: setRowSelection,
        state: {
            sorting,
            columnFilters,
            columnVisibility,
            rowSelection,
        },
    });

    return (
        <Card>
            <CardHeader>
                <CardTitle>Sales Orders</CardTitle>
                <CardDescription>A list of recent sales orders.</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="flex items-center py-4 gap-2">
                    <Input
                        placeholder="Filter by customer..."
                        value={(table.getColumn("customer")?.getFilterValue() as string) ?? ""}
                        onChange={(event) =>
                            table.getColumn("customer")?.setFilterValue(event.target.value)
                        }
                        className="max-w-sm"
                    />
                    <DataTableViewOptions table={table} />
                    <div className="ml-auto flex gap-2">
                        <Button variant="outline">Import</Button>
                        <Button variant="outline">Export</Button>
                    </div>
                </div>
                <div className="rounded-md border">
                    <Table>
                        <TableHeader>
                            {table.getHeaderGroups().map(headerGroup => (
                                <TableRow key={headerGroup.id}>
                                    {headerGroup.headers.map(header => (
                                        <TableHead key={header.id}>
                                            {header.isPlaceholder
                                                ? null
                                                : flexRender(
                                                    header.column.columnDef.header,
                                                    header.getContext()
                                                )}
                                        </TableHead>
                                    ))}
                                </TableRow>
                            ))}
                        </TableHeader>
                        <TableBody>
                            {table.getRowModel().rows.map(row => (
                                <TableRow key={row.id}>
                                    {row.getVisibleCells().map(cell => (
                                        <TableCell key={cell.id}>
                                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
                <DataTablePagination table={table} />
                <div className="flex justify-end pt-4">
                    <Link href="/admin/sales/sales-order">
                        <Button variant="outline">Show More</Button>
                    </Link>
                </div>
            </CardContent>
        </Card>
    )
}

function DateRangePicker({ className }: React.HTMLAttributes<HTMLDivElement>) {
    const [date, setDate] = React.useState<DateRange | undefined>({
        from: new Date(2024, 0, 20),
        to: addDays(new Date(2024, 0, 20), 20),
    })

    return (
        <div className={cn("grid gap-2", className)}>
            <Popover>
                <PopoverTrigger asChild>
                    <Button
                        id="date"
                        variant={"outline"}
                        className={cn(
                            "w-[300px] justify-start text-left font-normal",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date?.from ? (
                            date.to ? (
                                <>
                                    {format(date.from, "LLL dd, y")} -{" "}
                                    {format(date.to, "LLL dd, y")}
                                </>
                            ) : (
                                format(date.from, "LLL dd, y")
                            )
                        ) : (
                            <span>Pick a date</span>
                        )}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                        initialFocus
                        mode="range"
                        defaultMonth={date?.from}
                        selected={date}
                        onSelect={setDate}
                        numberOfMonths={2}
                    />
                </PopoverContent>
            </Popover>
        </div>
    )
}


export default function SalesDashboardPage() {
  return (
    <PageContainer>
      <div className='flex flex-1 flex-col space-y-2'>
        <div className='flex items-center justify-between space-y-2'>
          <h2 className='text-2xl font-bold tracking-tight'>
            Sales Dashboard
          </h2>
          <DateRangePicker />
        </div>

        <div className='grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4'>
          {summaryData.map((data, i) => (
            <Card key={i}>
              <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
                <CardTitle className='text-sm font-medium'>{data.title}</CardTitle>
                <data.Icon className='h-4 w-4 text-muted-foreground' />
              </CardHeader>
              <CardContent>
                <div className='text-2xl font-bold'>{data.value}</div>
                <p className='text-xs text-muted-foreground'>
                  {data.change} {data.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
        <div className='grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-7'>
            <div className='col-span-7'>
                <ModernAreaChart />
            </div>
            <div className='col-span-4'>
                <ModernBarChart />
            </div>
            <div className='col-span-4 md:col-span-3'>
                <ModernPieChart />
            </div>
        </div>
        <div className='py-4'>
            <SalesOrderTable />
        </div>
      </div>
    </PageContainer>
  );
}