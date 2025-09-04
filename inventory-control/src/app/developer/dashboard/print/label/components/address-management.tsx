"use client";

import { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Destination } from "../types";
import { AddressModal } from "./address-modal";

type ApiResponse = {
  items: Destination[];
  total_pages: number;
  current_page: number;
};

export function AddressManagement() {
    const [destinations, setDestinations] = useState<Destination[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [searchTerm, setSearchTerm] = useState("");
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingAddress, setEditingAddress] = useState<Destination | null>(null);

    const fetchAddresses = async (page: number, search: string) => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:5000/api/destinations?page=${page}&search=${search}`);
            if (!response.ok) {
                throw new Error('Failed to fetch addresses');
            }
            const data: ApiResponse = await response.json();
            setDestinations(data.items);
            setCurrentPage(data.current_page);
            setTotalPages(data.total_pages);
        } catch (error) {
            console.error("Error fetching addresses:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const debounceTimer = setTimeout(() => {
            fetchAddresses(1, searchTerm);
        }, 300);

        return () => clearTimeout(debounceTimer);
    }, [searchTerm]);

    const handlePageChange = (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            fetchAddresses(newPage, searchTerm);
        }
    }

    const handleOpenModal = (address: Destination | null) => {
        setEditingAddress(address);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setEditingAddress(null);
    };

    const handleSaveAddress = async (data: Destination) => {
        const url = data.id
            ? `http://localhost:5000/api/destinations/${data.id}`
            : `http://localhost:5000/api/destinations`;
        const method = data.id ? 'PUT' : 'POST';

        // A bit of data wrangling to match the backend expectations from the form data
        const payload = {
          ...data,
          pt: data.pt,
          instansi: data.instansi,
          tujuan: data.tujuan,
          alamat: data.alamat,
          provinsi: data.provinsi,
          kontak: data.kontak || null
        };


        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!response.ok) {
                throw new Error('Failed to save address');
            }
            fetchAddresses(data.id ? currentPage : 1, searchTerm);
            handleCloseModal();
        } catch (error) {
            console.error("Error saving address:", error);
        }
    };


    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <Input
                    placeholder="Cari alamat..."
                    value={searchTerm}
                    onChange={(e) => {
                        setSearchTerm(e.target.value);
                        setCurrentPage(1); // Reset to page 1 on search
                    }}
                    className="max-w-sm"
                />
                <Button onClick={() => handleOpenModal(null)}>+ Tambah Alamat Baru</Button>
            </div>
            <div className="rounded-md border scroll-auto">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>ID</TableHead>
                            <TableHead>PT Tujuan</TableHead>
                            <TableHead>Instansi</TableHead>
                            <TableHead className="text-right">Aksi</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center">Memuat data...</TableCell>
                            </TableRow>
                        ) : destinations.length > 0 ? (
                            destinations.map((dest) => (
                                <TableRow key={dest.id}>
                                    <TableCell>{dest.id}</TableCell>
                                    <TableCell>{dest.pt_tujuan}</TableCell>
                                    <TableCell>{dest.instansi}</TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm" onClick={() => handleOpenModal(dest)}>Edit</Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={4} className="text-center">Data alamat tidak ditemukan.</TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            <div className="flex items-center justify-between space-x-2 py-4">
                <div className="text-sm text-muted-foreground">
                    Page {currentPage} of {totalPages}
                </div>
                <div className="space-x-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handlePageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </Button>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handlePageChange(currentPage + 1)}
                        disabled={currentPage >= totalPages}
                    >
                        Next
                    </Button>
                </div>
            </div>
            <AddressModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onSave={handleSaveAddress}
                address={editingAddress}
            />
        </div>
    )
}
