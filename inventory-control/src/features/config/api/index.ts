// Fixed API Client
// inventory-control/src/features/config/api/index.ts
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

export class ApiClient {
  private type: string;

  constructor(type: string) {
    this.type = type;
  }

  async getAll() {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/`);
      if (!response.ok) {
        throw new Error(`Failed to fetch ${this.type}: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      console.error(`Error fetching ${this.type}:`, error);
      throw error;
    }
  }

  async create(data: any) {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error(`Failed to create ${this.type}: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      console.error(`Error creating ${this.type}:`, error);
      throw error;
    }
  }

  async update(id: number, data: any) {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error(`Failed to update ${this.type}: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      console.error(`Error updating ${this.type}:`, error);
      throw error;
    }
  }

  async delete(id: number) {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        throw new Error(`Failed to delete ${this.type}: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      console.error(`Error deleting ${this.type}:`, error);
      throw error;
    }
  }
}