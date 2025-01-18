export interface WeeklySchedule {
    topic: string,
    schedule: {
        day_1: DaySchedule,
        day_2: DaySchedule,
        day_3: DaySchedule,
        day_4: DaySchedule,
        day_5: DaySchedule,
        day_6: DaySchedule,
        day_7: DaySchedule,
        topic: string,
    }
}

export interface DaySchedule {
    subtopic: string,
    subtopic_description: string,
    progress_revision_topic: string,
}