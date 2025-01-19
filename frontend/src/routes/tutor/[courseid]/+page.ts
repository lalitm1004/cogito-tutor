import { PUBLIC_BACKEND_URL } from "$env/static/public";
import { loadingStore } from "$lib/stores/loadingStore";
import type { WeeklySchedule } from "$lib/types/WeeklySchedule.types";
import type { PageLoad } from "../$types";

export const load: PageLoad = async ({ params, fetch }) => {
    const cache = localStorage.getItem(params.courseid);
    if (cache) {
        return JSON.parse(cache) as WeeklySchedule;
    }
    loadingStore.set(true)

    const response = await fetch(`${PUBLIC_BACKEND_URL}/get-schedule`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('cogito-token')}`,
        },
        body: JSON.stringify({
            course_id: params.courseid
        }),
    });

    const data = await response.json();
    console.log(JSON.stringify(data))
    localStorage.setItem(params.courseid, JSON.stringify(data));
    loadingStore.set(false)
    return data as WeeklySchedule
}

export const ssr = false;
