import { writable } from 'svelte/store';
import type { AlertType, OnSelectAddress } from './types';
export const alertStore = writable<AlertType>({});
export const activatePKStore = writable<OnSelectAddress>({});
