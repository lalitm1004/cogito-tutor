<script lang="ts">
    let { data } = $props();

    const NUM_IMAGES = 11;
</script>

<main class={`h-dvh w-dvw py-10 px-8 overflow-x-hidden`}>
    <p class={`font-bespoke md:text-8xl text-6xl`}>Tutor</p>

    <div class={`flex md:flex-row flex-col flex-wrap justify-center items-center gap-4 mt-10`}>
        <a aria-labelledby="Create New Study Plan" class={`group h-[310px] w-[250px] apply-card flex flex-col gap-2 justify-center items-center rounded-lg overflow-hidden`} href={`/tutor/new`}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-plus"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
            <p>Create New Study Plan</p>
        </a>

        {#each data.courses as course (course.id)}
            <a class={`group h-[310px] w-[250px] apply-card flex flex-col rounded-lg overflow-hidden`} href={`/tutor/${course.id}`}>
                <div class={`h-[250px]`}>
                    <img class={`h-full w-[250px]`} alt="" src={`/images/${Math.floor(course.img_id % NUM_IMAGES)}.jpg`}/>
                </div>
                <div class={`h-[60px] w-full dark:group-hover:bg-gray-800 group-hover:bg-neutral-300 transition-colors duration-300 text-lg font-supreme flex items-center px-4 leading-6`}>
                    {course.topic}
                </div>
            </a>
        {/each}
    </div>
</main>
