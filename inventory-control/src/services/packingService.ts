// src/services/packingService.ts

const getApiUrl = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    throw new Error("NEXT_PUBLIC_API_URL is not set in environment variables.");
  }
  return apiUrl;
};

/**
 * Mengirim (POST) data manifest baru ke API.
 */
export async function createManifest(payload: object) {
  const apiUrl = getApiUrl();
  const response = await fetch(`${apiUrl}/api/v1/packing/manifests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(`Gagal mengirim manifest: ${errorData.message || response.statusText}`);
  }
  return response.json();
}

/**
 * Mengambil (GET) semua data manifest dari API.
 */
export async function getAllManifests() {
  const apiUrl = getApiUrl();
  const response = await fetch(`${apiUrl}/api/v1/packing/manifests?limit=25`);
  
  if (!response.ok) {
    throw new Error('Gagal mengambil daftar manifest');
  }
  return response.json();
}

/**
 * Mengambil (GET) detail satu manifest berdasarkan public_id.
 */
export async function getManifestById(publicId: string) {
  const apiUrl = getApiUrl();
  const response = await fetch(`${apiUrl}/api/v1/packing/manifests/${publicId}`);

  if (!response.ok) {
    throw new Error(`Gagal mengambil detail manifest ID: ${publicId}`);
  }
  return response.json();
}