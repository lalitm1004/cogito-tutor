import { PUBLIC_BACKEND_URL } from "$env/static/public";
import type { PageLoad } from "../$types";
import type { DailyContent } from "$lib/types/DailyContent.types";

export const load: PageLoad = async ({ params, fetch }) => {

    const day_day_map_v2 = {
        'day_1': 1,
        'day_2': 2,
        'day_3': 3,
        'day_4': 4,
        'day_5': 5,
        'day_6': 6,
        'day_7': 7,
    }

    const response = await fetch(`${PUBLIC_BACKEND_URL}/generate-day-content`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('cogito-token')}`,
        },
        body: JSON.stringify({
            course_id: params.courseid,
            day_number: day_day_map_v2[params.day]
        }),
    });

    const data = await response.json();
    console.log(JSON.stringify(data))
    return data as DailyContent
}

export const ssr = false;
