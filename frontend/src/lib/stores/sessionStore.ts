import { writable } from "svelte/store";
export const sessionStore = writable<Session | null>(null);