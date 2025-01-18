// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	interface ViewTransition {
		updateCallbackDone: Promise<void>;
		ready: Promise<void>;
		finished: Promise<void>;
		skipTransition: () => void;
	}
	interface Document {
		startViewTransition(updateCallback: () => Promise<void>): ViewTransition
	}
	type Theme = 'light' | 'dark';
	type Device = 'mobile' | 'desktop';
	interface Profile {
		id: string,
		email: string,
		first_name: string,
		last_name: string,
		avatar_url: string,
	}
	interface Session {
		token: string,
		profile: Profile
	}
}

export {};