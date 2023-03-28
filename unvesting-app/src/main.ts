// import '/global.css';
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app'),
});

interface AppConfigs {
  SERVER_API_URL: string;
  STELLAR_HORIZON_URL: string;
  STELLAR_NETWORK: string;
}

declare global {
  interface Window {
    config: AppConfigs;
  }
}

export default app;
