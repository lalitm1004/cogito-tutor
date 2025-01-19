<script lang="ts">
    import { Brain, Clock, Turtle, ArrowRight } from "lucide-svelte";

    const whyCogitoItems = [
        {
            icon: Brain,
            text: "Learning's hard enough. Let AI do the organizing."
        },
        {
            icon: Clock,
            text: "Take it one day at a time. That's all you need."
        },
        {
            icon: Brain,
            text: "Every mind learns differently. We get that."
        },
        {
            icon: Turtle,
            text: "Like our turtle friend says: steady wins the race."
        }
    ];
</script>

<div class="min-h-dvh w-full flex flex-col lg:grid lg:grid-cols-2 lg:place-items-center px-4 sm:px-8 md:px-12 lg:px-16 py-12 lg:py-0 gap-12 lg:gap-8">
    <!-- Left Column - ASCII Art -->
    <div class="w-full sm:max-w-[540px] md:max-w-[640px] lg:w-[590px] flex flex-col items-center justify-center order-2 lg:order-1">
        <pre class="font-mono text-lg sm:text-2xl md:text-3xl lg:text-4xl text-center whitespace-pre leading-snug">
/^\
|   |
/\     |_|     /\
| \___/' `\___/ |
\_/  \___/  \_/
|\__/   \__/|
|/  \___/  \|
./\__/   \__/\,
| /  \___/  \ |
\/     V     \/
        </pre>
    </div>

    <!-- Right Column - The Vision -->
    <div class="w-full sm:max-w-[540px] md:max-w-[640px] lg:w-[590px] flex flex-col order-1 lg:order-2">
        <h2 class="font-bespoke tracking-tighter text-4xl sm:text-5xl md:text-6xl lg:text-7xl">
            Why Cogito?
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mt-6 sm:mt-8">
            {#each whyCogitoItems as item}
                <div class="p-4 sm:p-6 rounded-lg dark:bg-gray-800/40 border-2 dark:border-gray-800 border-neutral-300 space-y-2 sm:space-y-3 transition-all hover:border-green-500/30">
                    <svelte:component this={item.icon} class="h-5 w-5 sm:h-6 sm:w-6 dark:text-green-500/60 text-green-600" />
                    <p class="text-base sm:text-lg dark:text-amber-50 text-neutral-900">{item.text}</p>
                </div>
            {/each}
        </div>
    </div>
</div>
