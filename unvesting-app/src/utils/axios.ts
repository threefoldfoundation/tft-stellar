import axios from 'axios';

const noConfigs = () => {
  throw new Error(
    'Invalid config. Please fill the config.json file with the correct data',
  );
};

const http = axios.create({
  baseURL: window.config ? window.config.SERVER_API_URL : noConfigs(),
  headers: {
    'Content-Type': 'application/json',
  },
});

export default http;
