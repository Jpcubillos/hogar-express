import axios from 'axios';

// Get CSRF token from Django cookie
function getCookie(name: string): string | null {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  withCredentials: true, // Crucial for session cookies
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor to automatically add CSRF token header
api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response interceptor to handle global errors (401/403)
api.interceptors.response.use((response) => {
  return response;
}, (error) => {
  if (error.response) {
    const status = error.response.status;
    if (status === 401) {
      // Handle unauthorized session expiration
      console.warn("Session unauthorized. User might need to login.");
      // Option to redirect to /login if routing is established
    } else if (status === 403) {
      console.error("Forbidden. User does not have appropriate permissions.");
    }
  }
  return Promise.reject(error);
});

export default api;
