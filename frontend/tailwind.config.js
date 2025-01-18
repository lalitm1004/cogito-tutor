import plugin from 'tailwindcss/plugin'

/** @type {import('tailwindcss').Config} */
export default {
	content: ['src/**/*.{html,js,ts,svelte}'],
	theme: {
		extend: {
			fontFamily: {
				'bespoke': ['Bespoke-Stencil', 'sans-serif'],
				'supreme': ['Supreme', 'sans-serif'],
				'inter': ["Inter", 'sans-serif']
			},
			fontWeight: {
				thin: '100',
				extralight: '200',
				light: '300',
				regular: '400',
				medium: '500',
				semibold: '600',
				bold: '700',
				extrabold: '800',
				black: '900',
			}
		},
	},
	plugins: [
		plugin(({ addVariant }) => {
			addVariant('mobile', 'html[data-device="mobile"] &');
			addVariant('desktop', 'html[data-device="desktop"] &');
		}),
	],
	darkMode: ['selector', '[data-theme="dark"]']
}
