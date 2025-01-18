export const getCookie = (cookies: string, key: string): string | null => {
    const cookie = cookies
        .split(';')
        .find(cookie => cookie.trim().startsWith(`${key}=`));
    if (!cookie) return null;
    return cookie.split('=')[1];
}