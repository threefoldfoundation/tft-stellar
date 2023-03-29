import axios from 'axios';
import { setConfig } from './helpers';

setConfig();

const http = axios.create({
  baseURL: window.config.SERVER_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;
