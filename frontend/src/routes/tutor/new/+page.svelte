<script lang="ts">
    import { goto } from "$app/navigation";
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
    import { loadingStore } from "$lib/stores/loadingStore";
    import { sessionStore } from "$lib/stores/sessionStore";
    import { page } from "$app/stores";
    import { onMount } from "svelte";

    let error: boolean = $state(false);
    let topicValue: string = $state("");
    let descValue: string = $state("");

    onMount(() => {
        const urlParams = new URLSearchParams($page.url.search);
        const paramTopicValue = urlParams.get('topicValue');
        if (paramTopicValue) {
            topicValue = paramTopicValue;
        }
    });

    const handleTopicInput = (event: Event) => {
        const target = event.target as HTMLInputElement;
        topicValue = target.value;
        if (target.value.length > 0) {
            error = false
        }
    }

    const handleDescInput = (event: Event) => {
        const target = event.target as HTMLInputElement;
        descValue = target.value;
        if (target.value.length > 0) {
            error = false
        }
    }

    const handleClick = async () => {
        if (!topicValue || !descValue) {
            error = true;
            return;
        }

        $loadingStore = true;
        try {
            const payload = {
                topic: topicValue,
                description: descValue,
            };

            const response = await fetch(`${PUBLIC_BACKEND_URL}/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${$sessionStore?.token}`,
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                const result = await response.json();
                goto(`/tutor/${result.course.id}`)
            }
        } catch (err) {
            console.log(err)
        } finally {
            $loadingStore = false;
        }
    }
</script>

<main class={`h-dvh w-dvw py-10 px-8 flex flex-col items-center overflow-x-hidden`}>
    <p class={`absolute left-8 font-bespoke md:text-8xl text-6xl`}>Create Plan</p>

    <div class={`relative apply-card flex flex-col gap-4 px-4 py-5 mt-40 rounded-lg w-[350px] md:w-[450px]`}>
        <div class={`flex flex-col justify-center`}>
            <p class={`font-supreme text-xl`}>Topic</p>
            <p class={`text-sm text-neutral-700 mb-1`}>Populate the following with a simple one line topic.</p>
            <input
                    value={topicValue}
                    oninput={handleTopicInput}
                    placeholder={`Enter topic`}
                    class={`h-[40px] w-[300px] md:w-[400px] flex flex-grow text-start dark:bg-gray-800/70 bg-neutral-200 dark:caret-amber-50 caret-neutral-950 dark:text-amber-50 text-neutral-900 font-supreme px-4 rounded-lg outline-none`}
            />
        </div>

        <div class={`flex flex-col justify-center mt-2`}>
            <p class={`font-supreme text-xl`}>Brief Description</p>
            <p class={`text-sm text-neutral-700 mb-2`}>Populate the following with a brief description of the syllabus, your strengths and weaknesses. This allows cogito to personalize a study plan for you.</p>
            <textarea
                    oninput={handleDescInput}
                    placeholder={`Enter brief description`}
                    class={`h-[80px] w-[300px] md:w-[400px] flex flex-grow text-start dark:bg-gray-800/70 bg-neutral-200 dark:caret-amber-50 caret-neutral-950 dark:text-amber-50 text-neutral-900 font-supreme px-2 py-2 rounded-lg outline-none`}
            ></textarea>
        </div>

        <button
                onclick={handleClick}
                aria-labelledby={`Generate study plan`}
                class={`h-[50px] flex justify-center items-center gap-4 bg-green-500 dark:bg-green-500/60 px-4 rounded-lg cursor-pointer ring-0`}
        >
            <p class={`text-lg`}>Create Study Plan</p>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class={`dark:stroke-amber-50 stroke-neutral-800 lucide lucide-send-horizontal`}>
                <path d="M3.714 3.048a.498.498 0 0 0-.683.627l2.843 7.627a2 2 0 0 1 0 1.396l-2.842 7.627a.498.498 0 0 0 .682.627l18-8.5a.5.5 0 0 0 0-.904z"/>
                <path d="M6 12h16"/>
            </svg>
        </button>

        {#if error}
            <p class="absolute md:left-2  -bottom-[25px] text-red-400 text-sm">
                * Fields cannot be empty
            </p>
        {/if}
    </div>
</main>
