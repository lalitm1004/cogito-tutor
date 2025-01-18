import plugin from 'tailwindcss/plugin';

/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,ts,svelte}'],
	theme: {
		extend: {},
	},
	plugins: [
		plugin(({ addVariant }) => {
			addVariant('mobile', 'html[data-device="mobile"] &');
			addVariant('desktop', 'html[data-device="desktop"] &');
		}),
	],
	darkMode: ['selector', '[data-theme="dark"]']
}

