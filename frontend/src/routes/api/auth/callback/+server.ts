import { redirect } from "@sveltejs/kit";
import type { RequestEvent } from "./$types";
import { PUBLIC_BACKEND_URL } from "$env/static/public";

const maxAge = 30 * 24 * 60 * 60;

export const GET = async ({ url, cookies, fetch }: RequestEvent) => {
    const token = url.searchParams.get('token');
    if (!token) {
        throw redirect(302, "/error");
    }

    cookies.set('cogito-auth', token, {
        path: '/',
        expires: new Date(Date.now() + maxAge),
        maxAge,
        httpOnly: false,
        sameSite: 'strict',
    });

    const response = await fetch(`${PUBLIC_BACKEND_URL}/profile`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        throw redirect(302, "/error");
    }

    const profile: Profile = await response.json();
    cookies.set('cogito-profile', JSON.stringify(profile), {
        path: '/',
        expires: new Date(Date.now() + maxAge),
        maxAge,
        httpOnly: false,
        sameSite: 'strict',
    });

    throw redirect(302, "/");
}