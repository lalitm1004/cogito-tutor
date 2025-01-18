import { browser } from "$app/environment";
import { writable } from "svelte/store";

const TOKEN_NAME = 'cogito-theme'
const initialValue = browser ? window.localStorage.getItem(TOKEN_NAME) ?? 'dark' : 'dark';
const theme = writable<Theme>(initialValue as Theme);
const setTheme = (value: Theme) => {
    if (!browser) return

    document.documentElement.dataset.theme = value;
    document.cookie = `${TOKEN_NAME}=${value};path=/;max-age=${60 * 60 * 24 * 365}`;
    window.localStorage.setItem(TOKEN_NAME, value);
    theme.set(value);
}

export { TOKEN_NAME, theme, setTheme }