import axios from 'axios';


// Create an instance of axios
const api = axios.create();

// Add a request interceptor to the api instance
api.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export default api;