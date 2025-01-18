<script lang="ts">
    let { data } = $props();
    console.log(Object.entries(data.schedule))

    const day_day_map = {
        'day_1': 'Day 1',
        'day_2': 'Day 2',
        'day_3': 'Day 3',
        'day_4': 'Day 4',
        'day_5': 'Day 5',
        'day_6': 'Day 6',
        'day_7': 'Day 7',
    }
</script>

<div class={`w-dvw h-dvh px-8 py-10 overflow-x-hidden`}>
    <p class={`font-bespoke md:text-7xl text-6xl`}>
        {data.topic}
    </p>

    <div class={`flex flex-row justify-center flex-wrap gap-8 overflow-x-hidden mt-8`}>
        {#each Object.entries(data.schedule) as [day, daySchedule]}
            {#if day !== 'topic'}
                <div class={`apply-card w-[400px] h-[300px] flex flex-col justify-between gap-2 px-4 py-4 rounded-lg`}>
                    <div class={`flex flex-col justify-between`}>
                        <div>
                            <p class={`font-inter font-bold text-2xl`}>{Object(day_day_map)[day]}</p>
                            <p class={`text-base`}>{daySchedule.subtopic}</p>
                        </div>
    
                        <div class={`flex flex-col mt-4`}>
                            <p class={`text-neutral-700`}>Revision Topic</p>
                            <p class={`text-sm`}>{daySchedule.progress_revision_topic}</p>
                        </div>
                    </div>

                    <div class={`flex flex-col gap-1`}>
                        <a href="" class={`apply-card py-2 flex justify-center items-center rounded-lg`}>Flashcards</a>
                        <a href="" class={`apply-card py-2 flex justify-center items-center rounded-lg`}>Quiz</a>
                    </div>
                </div>

            {/if}
        {/each}
    </div>
</div>