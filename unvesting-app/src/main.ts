// import '/global.css';
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app'),
});

interface AppConfigs {
  NETWORK: string;
  SERVER_API_URL: string;
}

declare global {
  interface Window {
    config: AppConfigs;
  }
}

export default app;
