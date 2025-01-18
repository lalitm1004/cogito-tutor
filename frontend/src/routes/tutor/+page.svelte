<script lang="ts">
    let { data } = $props();

    const NUM_IMAGES = 11;
</script>

<main class={`h-dvh w-dvw py-10 px-8 overflow-x-hidden`}>
    <p class={`font-bespoke md:text-8xl text-6xl`}>Tutor</p>

    <div class={`flex md:flex-row flex-col flex-wrap justify-center items-center gap-4 mt-10`}>
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