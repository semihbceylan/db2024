// src/utils/axiosConfig.js
import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5002', // Updated to port 5001
    // You can add headers or other configurations here if needed
});

export default axiosInstance;
