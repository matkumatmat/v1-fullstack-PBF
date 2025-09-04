'use client';

import PageContainer from '@/components/layout/page-container';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from '@/components/ui/card';
import React from 'react';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal, CalendarIcon } from "lucide-react"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { cn } from "@/lib/utils"
import { format } from "date-fns"
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
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Calendar } from "@/components/ui/calendar"

const salesOrderFormSchema = z.object({
    so: z.string().min(1, "SO number is required."),
    po: z.string().min(1, "PO number is required."),
    poDate: z.date({ required_error: "PO date is required." }),
    customer: z.string({ required_error: "Please select a customer." }),
    product: z.string({ required_error: "Please select a product." }),
    quantity: z.coerce.number().min(1, "Quantity must be at least 1."),
    value: z.coerce.number().min(1, "Value must be at least 1."),
})

const customerData = [
    { id: "CUST-001", name: "John Doe" },
    { id: "CUST-002", name: "Jane Smith" },
    { id: "CUST-003", name: "Sam Wilson" },
    { id: "CUST-004", name: "Sara Johnson" },
    { id: "CUST-005", name: "Michael Brown" },
]

const productData = [
    { id: "PROD-001", name: "Laptop Model X" },
    { id: "PROD-002", name: "Desktop Model Y" },
    { id: "PROD-003", name: "Tablet Model Z" },
    { id: "PROD-004", name: "Accessories Kit" },
]

const salesOrderData = [
    { SO: "SO-001", PO: "PO-101", poDate: "2024-06-01", customer: "John Doe", product: "Laptop Model X", quantity: 10, value: 10000, quantityRealisation: 10, valueRealisation: 10000, status: "Fulfilled" },
    { SO: "SO-002", PO: "PO-102", poDate: "2024-06-02", customer: "Jane Smith", product: "Desktop Model Y", quantity: 5, value: 7500, quantityRealisation: 0, valueRealisation: 0, status: "Pending" },
    { SO: "SO-003", PO: "PO-103", poDate: "2024-06-03", customer: "Sam Wilson", product: "Tablet Model Z", quantity: 20, value: 8000, quantityRealisation: 10, valueRealisation: 4000, status: "Partial" },
    { SO: "SO-004", PO: "PO-104", poDate: "2024-06-04", customer: "Sara Johnson", product: "Laptop Model X", quantity: 5, value: 5000, quantityRealisation: 0, valueRealisation: 0, status: "Cancelled" },
    { SO: "SO-005", PO: "PO-105", poDate: "2024-06-05", customer: "Michael Brown", product: "Accessories Kit", quantity: 50, value: 2500, quantityRealisation: 50, valueRealisation: 2500, status: "Fulfilled" },
    { SO: "SO-006", PO: "PO-106", poDate: "2024-06-06", customer: "Emily Davis", product: "Desktop Model Y", quantity: 2, value: 3000, quantityRealisation: 0, valueRealisation: 0, status: "Pending" },
    { SO: "SO-007", PO: "PO-107", poDate: "2024-06-07", customer: "Chris Miller", product: "Laptop Model X", quantity: 8, value: 8000, quantityRealisation: 8, valueRealisation: 8000, status: "Fulfilled" },
    { SO: "SO-008", PO: "PO-108", poDate: "2024-06-08", customer: "James Taylor", product: "Tablet Model Z", quantity: 15, value: 6000, quantityRealisation: 0, valueRealisation: 0, status: "Pending" },
    { SO: "SO-009", PO: "PO-109", poDate: "2024-06-09", customer: "Patricia Anderson", product: "Accessories Kit", quantity: 100, value: 5000, quantityRealisation: 100, valueRealisation: 5000, status: "Fulfilled" },
    { SO: "SO-010", PO: "PO-110", poDate: "2024-06-10", customer: "Robert Thomas", product: "Laptop Model X", quantity: 3, value: 3000, quantityRealisation: 0, valueRealisation: 0, status: "Cancelled" },
    { SO: "SO-011", PO: "PO-111", poDate: "2024-06-11", customer: "Linda Jackson", product: "Desktop Model Y", quantity: 4, value: 6000, quantityRealisation: 4, valueRealisation: 6000, status: "Fulfilled" },
    { SO: "SO-012", PO: "PO-112", poDate: "2024-06-12", customer: "David White", product: "Tablet Model Z", quantity: 10, value: 4000, quantityRealisation: 5, valueRealisation: 2000, status: "Partial" },
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
    const [isModalOpen, setIsModalOpen] = React.useState(false);

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

    const form = useForm<z.infer<typeof salesOrderFormSchema>>({
        resolver: zodResolver(salesOrderFormSchema),
        defaultValues: {
            so: "",
            po: "",
            customer: "",
            product: "",
            quantity: 0,
            value: 0,
        },
    });

    function onSubmit(values: z.infer<typeof salesOrderFormSchema>) {
        console.log(values)
        setIsModalOpen(false);
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Sales Orders</CardTitle>
                <CardDescription>A list of all sales orders.</CardDescription>
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
                        <Button variant="outline">Export</Button>
                        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                            <DialogTrigger asChild>
                                <Button>Add New SO</Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                    <DialogTitle>Add New Sales Order</DialogTitle>
                                    <DialogDescription>
                                        Fill in the details for the new sales order.
                                    </DialogDescription>
                                </DialogHeader>
                                <Form {...form}>
                                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                                        <FormField
                                            control={form.control}
                                            name="so"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>SO Number</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="SO-001" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="po"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>PO Number</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="PO-123" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="poDate"
                                            render={({ field }) => (
                                                <FormItem className="flex flex-col">
                                                    <FormLabel>PO Date</FormLabel>
                                                    <Popover>
                                                        <PopoverTrigger asChild>
                                                            <FormControl>
                                                                <Button
                                                                    variant={"outline"}
                                                                    className={cn(
                                                                        "pl-3 text-left font-normal",
                                                                        !field.value && "text-muted-foreground"
                                                                    )}
                                                                >
                                                                    {field.value ? (
                                                                        format(field.value, "PPP")
                                                                    ) : (
                                                                        <span>Pick a date</span>
                                                                    )}
                                                                    <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                                                </Button>
                                                            </FormControl>
                                                        </PopoverTrigger>
                                                        <PopoverContent className="w-auto p-0" align="start">
                                                            <Calendar
                                                                mode="single"
                                                                selected={field.value}
                                                                onSelect={field.onChange}
                                                                initialFocus
                                                            />
                                                        </PopoverContent>
                                                    </Popover>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="customer"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Customer</FormLabel>
                                                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                        <FormControl>
                                                            <SelectTrigger>
                                                                <SelectValue placeholder="Select a customer" />
                                                            </SelectTrigger>
                                                        </FormControl>
                                                        <SelectContent>
                                                            {customerData.map(customer => (
                                                                <SelectItem key={customer.id} value={customer.name}>{customer.name}</SelectItem>
                                                            ))}
                                                        </SelectContent>
                                                    </Select>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="product"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Product</FormLabel>
                                                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                        <FormControl>
                                                            <SelectTrigger>
                                                                <SelectValue placeholder="Select a product" />
                                                            </SelectTrigger>
                                                        </FormControl>
                                                        <SelectContent>
                                                            {productData.map(product => (
                                                                <SelectItem key={product.id} value={product.name}>{product.name}</SelectItem>
                                                            ))}
                                                        </SelectContent>
                                                    </Select>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="quantity"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Quantity</FormLabel>
                                                    <FormControl>
                                                        <Input type="number" placeholder="0" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={form.control}
                                            name="value"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Value</FormLabel>
                                                    <FormControl>
                                                        <Input type="number" placeholder="0.00" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <Button type="submit">Submit</Button>
                                    </form>
                                </Form>
                            </DialogContent>
                        </Dialog>
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
            </CardContent>
        </Card>
    )
}

export default function SalesOrderPage() {
    return (
        <PageContainer>
            <div className="space-y-4 w-full">
                <SalesOrderTable />
            </div>
        </PageContainer>
    )
}
