import { browser } from "$app/environment";
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import { loadingStore } from "$lib/stores/loadingStore";
import type { CourseMeta } from "$lib/types/CourseMeta.types";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
    const response = await fetch(`${PUBLIC_BACKEND_URL}/tutor`, {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${localStorage.getItem('cogito-token')}`
        }
    });
    const data = await response.json();
    
    return {
        courses: data.courses as CourseMeta[],
    }
}

export const ssr = false;