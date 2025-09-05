const API_BASE_URL = '/api/v1';

export class ApiClient {
  private type: string;

  constructor(type: string) {
    this.type = type;
  }

  async getAll() {
    const response = await fetch(`${API_BASE_URL}/${this.type}/`);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${this.type}`);
    }
    return response.json();
  }

  async create(data: any) {
    const response = await fetch(`${API_BASE_URL}/${this.type}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      throw new Error(`Failed to create ${this.type}`);
    }
    return response.json();
  }

  async update(id: number, data: any) {
    const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      throw new Error(`Failed to update ${this.type}`);
    }
    return response.json();
  }

  async delete(id: number) {
    const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) {
      throw new Error(`Failed to delete ${this.type}`);
    }
    return response.json();
  }
}
