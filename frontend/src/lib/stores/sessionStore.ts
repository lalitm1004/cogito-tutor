import { browser } from "$app/environment";
import { writable } from "svelte/store";

const sessionStore = writable<Session | null>(null);
const setSession = (value: Session | null) => {
    if (!browser) return;

    window.localStorage.setItem('cogito-token', value?.token!);
    sessionStore.set(value)
}

export { sessionStore, setSession }