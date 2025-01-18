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

    let heroParagraph: HTMLParagraphElement;
    let observer: IntersectionObserver;

    onMount(() => {
        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                $isHeroVisible = entry.isIntersecting;
            });
        }, {
            threshold: 0.75
        });

        if (heroParagraph) {
            observer.observe(heroParagraph);
        }

        return () => {
            $isHeroVisible = false;
            observer.disconnect();
        }
    });
</script>

<div class={`h-full w-full md:grid md:grid-cols-2 md:place-items-center flex flex-col items-center`}>
    <div class={`h-fit md:w-[590px] w-[350px] md:mt-0 mt-12 flex flex-col font-supreme`}>
        <p bind:this={heroParagraph} class={`font-bespoke tracking-tighter md:text-9xl text-8xl`}>
            Cogito
        </p>

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

    <div class={`md:mt-0 mt-8`}>
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class={`md:h-[400px] h-[250px] aspect-square stroke-current stroke-2 fill-current`} version="1.1" id="Layer_1" viewBox="0 0 512 512" xml:space="preserve">
            <path d="M427.869,183.668c-0.714-1.05-1.445-2.086-2.192-3.111c-3.436-4.714-10.045-5.75-14.76-2.311    c-4.714,3.438-5.749,10.045-2.311,14.76c0.614,0.842,1.214,1.694,1.801,2.555c2.045,3.002,5.363,4.619,8.741,4.619    c2.047,0,4.117-0.595,5.937-1.834C429.906,195.061,431.153,188.489,427.869,183.668z"/>
            <path d="M64.075,263.255h-5.383c-5.834,0-10.564,4.729-10.564,10.564c0,5.834,4.729,10.564,10.564,10.564h5.383    c5.834,0,10.564-4.729,10.564-10.564S69.909,263.255,64.075,263.255z"/>
            <path d="M501.436,249.704h-52.845c-0.154-13.291-2.449-26.324-6.868-38.757c-1.954-5.497-7.994-8.371-13.491-6.416    c-5.497,1.953-8.37,7.994-6.415,13.491c3.61,10.156,5.494,20.809,5.647,31.681h-84.045v-23.779l43.251-54.798    c1.576,1.144,3.128,2.32,4.629,3.551c4.511,3.7,11.167,3.041,14.867-1.47c3.7-4.512,3.041-11.167-1.471-14.867    c-4.606-3.777-9.531-7.229-14.629-10.271c-0.019-0.012-0.038-0.023-0.057-0.036c-0.078-0.047-0.154-0.097-0.231-0.144    c-18.432-10.946-39.569-16.732-61.126-16.732H222.203c-21.557,0-42.694,5.786-61.118,16.728c-0.086,0.051-0.17,0.106-0.256,0.156    c-0.011,0.006-0.021,0.013-0.032,0.019c-29.854,17.807-50.522,47.855-56.651,81.712H52.809c-14.109,0-27.372,5.492-37.346,15.465    C5.492,255.209,0,268.472,0,282.583c0,19.456,15.824,35.283,35.272,35.283h105.233v31.291c0,17.473,14.215,31.687,31.687,31.687    h4.387c17.473,0,31.687-14.215,31.687-31.687v-31.291h136.318v31.291c0,17.473,14.215,31.687,31.687,31.687h4.398    c17.473,0,31.687-14.215,31.687-31.687v-34.024c4.335-1.453,8.474-3.478,12.345-6.042h38.477c13.034,0,25.294-5.075,34.535-14.3    c9.214-9.229,14.289-21.489,14.289-34.523C512,254.434,507.271,249.704,501.436,249.704z M328.651,152.286v-0.001    c13.656,0,27.099,2.826,39.483,8.224l-34.85,44.155l-37.345-52.378H328.651z M322.291,225.639v24.066h-93.726v-24.066h-0.001    l46.868-65.722L322.291,225.639z M222.203,152.285h32.721l-37.353,52.379l-34.852-44.156    C195.102,155.111,208.546,152.285,222.203,152.285z M35.272,296.738v-0.001c-7.799,0-14.144-6.35-14.144-14.155    c0-8.467,3.295-16.424,9.276-22.405c5.981-5.982,13.938-9.276,22.405-9.276h49.428c0,0.075-0.003,0.15-0.003,0.225v9.142v4.431    c0,12.023,4.016,23.122,10.771,32.039H35.272z M123.833,241.406c2.741-28.102,17.618-53.765,40.347-70.288l43.257,54.806v23.779    h-84.04C123.436,246.909,123.565,244.123,123.833,241.406z M187.137,349.157c0,5.822-4.737,10.559-10.559,10.559h-4.387    c-5.822,0-10.559-4.737-10.559-10.559v-31.291h25.505V349.157z M391.227,349.157c0,5.822-4.737,10.559-10.559,10.559h-4.398    c-5.822,0-10.559-4.737-10.559-10.559v-31.291h25.515V349.157z M414.992,290.089c-0.027,0.02-0.056,0.036-0.082,0.057    c-5.619,4.312-12.347,6.591-19.458,6.591h-40.305H197.701h-42.3c-15.569,0-28.581-11.163-31.45-25.905H218h114.853h94.057    C425.45,278.433,421.283,285.242,414.992,290.089z M482.772,279.851c-5.24,5.231-12.198,8.112-19.595,8.112h-19.878    c2.594-5.336,4.289-11.111,4.974-17.132h40.523C487.423,274.165,485.392,277.227,482.772,279.851z"/>
        </svg>
    </div>
</div>