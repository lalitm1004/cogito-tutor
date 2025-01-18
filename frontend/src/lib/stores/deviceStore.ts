import { browser } from "$app/environment";
import { writable } from "svelte/store";

const TOKEN_NAME = 'cogito-device'
const initialValue = browser ? window.localStorage.getItem(TOKEN_NAME) ?? 'desktop' : 'desktop';
const device = writable<Device>(initialValue as Device);
const setDevice = (value: Device) => {
    if (!browser) return;

    document.documentElement.dataset.device = value;
    document.cookie = `${TOKEN_NAME}=${value};path=/;max-age=${60 * 60 * 24 * 365}`;
    window.localStorage.setItem(TOKEN_NAME, value);
    device.set(value);
}

export { device, setDevice }