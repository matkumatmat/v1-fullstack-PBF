// Enhanced API Client with robust response handling
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

interface ApiResponse<T = any> {
  data?: T;
  items?: T;
  message?: string;
  error?: string;
}

export class ApiClient {
  private type: string;

  constructor(type: string) {
    this.type = type;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('content-type');
    
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      
      if (contentType?.includes('application/json')) {
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorData.error || errorMessage;
        } catch {
          // If JSON parsing fails, use the default error message
        }
      }
      
      throw new Error(errorMessage);
    }

    // Handle empty responses (like 204 No Content)
    if (response.status === 204 || !contentType?.includes('application/json')) {
      return { success: true } as T;
    }

    try {
      return await response.json();
    } catch (error) {
      throw new Error('Invalid JSON response from server');
    }
  }

  async getAll(): Promise<any[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });

      const result = await this.handleResponse<ApiResponse>(response);
      
      // Handle different response structures
      if (Array.isArray(result)) {
        return result;
      }
      
      if (result.data && Array.isArray(result.data)) {
        return result.data;
      }
      
      if (result.items && Array.isArray(result.items)) {
        return result.items;
      }
      
      // If single object, wrap in array
      if (typeof result === 'object' && result !== null && !Array.isArray(result)) {
        return [result];
      }
      
      return [];
      
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to fetch ${this.type}: ${error.message}`);
      }
      throw new Error(`Failed to fetch ${this.type}: Unknown error`);
    }
  }

  async create(data: any): Promise<any> {
    try {
      // Remove id and any system fields for creation
      const { id, created_at, updated_at, ...createData } = data;
      
      const response = await fetch(`${API_BASE_URL}/${this.type}/`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(createData)
      });

      return await this.handleResponse(response);
      
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to create ${this.type}: ${error.message}`);
      }
      throw new Error(`Failed to create ${this.type}: Unknown error`);
    }
  }

  async update(id: number | string, data: any): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      return await this.handleResponse(response);
      
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to update ${this.type}: ${error.message}`);
      }
      throw new Error(`Failed to update ${this.type}: Unknown error`);
    }
  }

  async delete(id: number | string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json'
        }
      });

      return await this.handleResponse(response);
      
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to delete ${this.type}: ${error.message}`);
      }
      throw new Error(`Failed to delete ${this.type}: Unknown error`);
    }
  }

  async getById(id: number | string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/${this.type}/${id}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });

      return await this.handleResponse(response);
      
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to fetch ${this.type} by ID: ${error.message}`);
      }
      throw new Error(`Failed to fetch ${this.type} by ID: Unknown error`);
    }
  }
}