<script lang="ts">
    import { goto } from "$app/navigation";
    import { isHeroVisible } from "$lib/stores/heroVisibility";
    import { onMount } from "svelte";

    let error: boolean = $state(false);
    let topicValue: string = $state("");

    const handleInput = (event: Event) => {
        const target = event.target as HTMLInputElement;

        topicValue = target.value;

        if (target.value.length > 0) {
            error = false
        }
    }

    const handleClick = () => {
        if (!topicValue) {
            error = true;
            return;
        }

        const params = new URLSearchParams({
            topicValue
        });

        goto(`/tutor?${params.toString()}`)
    }

    let heroDiv: HTMLDivElement;
    let observer: IntersectionObserver;

    onMount(() => {
        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                $isHeroVisible = entry.isIntersecting;
            });
        }, {
            threshold: 0.2
        });

        if (heroDiv) {
            observer.observe(heroDiv);
        }

        return () => {
            $isHeroVisible = false;
            observer.disconnect();
        }
    });
</script>

<div bind:this={heroDiv} class={`h-full w-full md:grid md:grid-cols-2 md:place-items-center flex flex-col items-center`}>
    <div class={`h-fit md:w-[590px] w-[350px] md:mt-0 mt-24 flex flex-col font-supreme`}>
        <h1 class={`font-bespoke tracking-tighter md:text-9xl text-8xl`}>
            Cogito
        </h1>

        <p class={`text-xl mt-8`}>
            Revolutionize learning with our AI-powered tutor. Generate study plans,
            quizzes and flashcards personalized to you.
        </p>

        <div class={`relative md:h-[80px] h-[150px] w-full flex flex-col gap-4 justify-center rounded-lg mt-4 px-2 py-2 dark:bg-gray-800/40 border-2 dark:border-gray-800 border-neutral-300`}>
            <input
                oninput={handleInput}
                placeholder={`Enter topic`}
                class={`h-[40px] flex flex-grow text-start dark:bg-gray-800/70 bg-neutral-200  dark:caret-amber-50 caret-neutral-950 dark:text-amber-50 text-neutral-900 font-supreme px-4 rounded-lg outline-none`}
            />

            {#if error}
                <p class="absolute md:left-2 md:top-[80px] -bottom-[25px] text-red-400 text-sm">
                    * Topic field cannot be empty
                </p>
            {/if}

            <button
                aria-labelledby={`Generate study plan`}
                onclick={handleClick}
                class={`md:absolute md:right-4 h-[40px] md:block flex justify-center items-center gap-4 md:flex-grow-0 flex-grow bg-green-500 dark:bg-green-500/60 px-4 rounded-lg cursor-pointer ring-0`}
            >
                <p class={`desktop:hidden text-lg`}>Create Study Plan</p>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class={`dark:stroke-amber-50 stroke-neutral-800 lucide lucide-send-horizontal`}>
                    <path d="M3.714 3.048a.498.498 0 0 0-.683.627l2.843 7.627a2 2 0 0 1 0 1.396l-2.842 7.627a.498.498 0 0 0 .682.627l18-8.5a.5.5 0 0 0 0-.904z"/>
                    <path d="M6 12h16"/>
                </svg>
            </button>
        </div>
    </div>

    <div class={`bg-red-100/10`}>
        <!---->
    </div>
</div>