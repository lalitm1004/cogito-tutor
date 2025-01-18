import { PUBLIC_BACKEND_URL } from "$env/static/public";
import type { WeeklySchedule } from "$lib/types/WeeklySchedule.types";
import type { PageLoad } from "../$types";

export const load: PageLoad = async ({ params, fetch }) => {
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
    return data as WeeklySchedule
}

export const ssr = false;