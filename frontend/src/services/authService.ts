import { apiClient } from './apiClient';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  login: string;
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface AuthService {
  login: (credentials: LoginRequest) => Promise<AuthResponse>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => void;
}

export const authService: AuthService = {
  login: async (credentials: LoginRequest) => {
    const response = await apiClient.post<AuthResponse>('/tokens/', credentials);
    apiClient.setToken(response.access_token);
    return response;
  },

  register: async (userData: RegisterRequest) => {
    return apiClient.post<void>('/users/', userData);
  },

  logout: () => {
    apiClient.setToken(null);
  },
};

