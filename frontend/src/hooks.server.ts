import type { Handle } from '@sveltejs/kit'
import { sequence } from '@sveltejs/kit/hooks';

const maxAge = 365 * 24 * 60 * 60;

const handleTheme: Handle = async ({ event, resolve }) => {
    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            let currentTheme = event.cookies.get('cogito-theme');
            if (!currentTheme) {
                const userPrefersDark = event.request.headers.get('sec-ch-prefers-color-scheme') === 'dark';
                currentTheme = userPrefersDark ? 'dark' : 'light';

                event.cookies.set('cogito-theme', currentTheme, {
                    path: '/',
                    expires: new Date(Date.now() + maxAge),
                    maxAge,
                    httpOnly: false,
                    sameSite: 'strict'
                });
            }

            return html
                .replace('data-theme=""', `data-theme="${currentTheme}"`)
        }
    })

    response.headers.set('Accept-CH', 'Sec-CH-Prefers-Color-Scheme');
    response.headers.set('Vary', 'Sec-CH-Prefers-Color-Scheme');
    response.headers.set('Critial-CH', 'Sec-CH-Prefers-Color-Scheme');

    return response;
}

const handleDevice: Handle = async({ event, resolve }) => {
    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            let currentDevice = event.cookies.get('cogito-device');
            if (!currentDevice) {
                const userOnMobile = event.request.headers.get('sec-ch-ua-mobile') === '?1';
                currentDevice = userOnMobile ? 'mobile' : 'desktop';

                event.cookies.set('cogito-device', currentDevice, {
                    path: '/',
                    expires: new Date(Date.now() + maxAge),
                    maxAge,
                    httpOnly: false,
                    sameSite: 'strict',
                })
            }

            return html
                .replace('data-device=""', `data-device="${currentDevice}"`)
        }
    })

    response.headers.set('Accept-CH', 'Sec-CH-UA-Mobile');
    response.headers.set('Vary', 'Sec-CH-UA-Mobile');
    response.headers.set('Critical-CH', 'Sec-CH-UA-Mobile');

    return response;
}

const handlePreloadFonts: Handle = async({ event, resolve }) => {
    const repsonse = await resolve(event, {
        preload: ({ type, path }) => type === 'font' || path.includes('/fonts/')
    })

    return repsonse;
}

export const handle = sequence(handleTheme, handleDevice, handlePreloadFonts);