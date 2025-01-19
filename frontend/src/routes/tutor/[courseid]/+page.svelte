<script lang="ts">
    let { data } = $props();
    import {page} from '$app/stores'

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

<div class="w-dvw h-dvh px-8 py-10 overflow-x-hidden">
    <div class="max-w-7xl mx-auto">
        <!-- Header Section -->
        <div class="flex flex-col space-y-4 mb-12">
            <h1 class="font-bespoke md:text-7xl text-6xl bg-gradient-to-r from-slate-900 to-slate-700 dark:from-slate-100 dark:to-slate-300 bg-clip-text text-transparent">
                {data.topic}
            </h1>
            <div class="flex items-center space-x-2 text-slate-600 dark:text-slate-400">
                <!-- Calendar Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span class="text-lg">7-Day Study Plan</span>
            </div>
        </div>

        <!-- Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 justify-items-center">
            {#each Object.entries(data.schedule) as [day, daySchedule]}
                {#if day !== 'topic'}
                    <div class="w-full max-w-[400px] h-[340px] bg-white dark:bg-slate-900 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 dark:hover:shadow-slate-800/30">
                        <div class="h-full p-6 flex flex-col justify-between">
                            <!-- Card Header -->
                            <div class="space-y-6">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <h2 class="font-inter font-bold text-2xl text-slate-900 dark:text-slate-100">
                                            {Object(day_day_map)[day]}
                                        </h2>
                                        <p class="text-slate-600 dark:text-slate-400 mt-1">
                                            {daySchedule.subtopic}
                                        </p>
                                    </div>
                                    <div class="bg-green-100 dark:bg-green-900/30 p-2 rounded-lg">
                                        <!-- Book Icon -->
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-600 dark:text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                                            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                                        </svg>
                                    </div>
                                </div>

                                <!-- Revision Section -->
                                <div class="space-y-2">
                                    <p class="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                                        <!-- Brain Icon -->
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M12 2a5 5 0 0 1 5 5c0 1.55-.6 2.95-1.57 4a3.5 3.5 0 0 0 4.57 5.25h0a7 7 0 0 0-7-12.25zm0 0a7 7 0 0 0-7 12.25h0a3.5 3.5 0 0 0 4.57-5.25A5 5 0 0 1 7 7a5 5 0 0 1 5-5z"></path>
                                        </svg>
                                        Revision Topic
                                    </p>
                                    <p class="text-sm text-slate-600 dark:text-slate-400">
                                        {daySchedule.progress_revision_topic}
                                    </p>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="space-y-3 mt-4">
                                <a data-sveltekit-preload-data="off" href="/flashcards/{$page.params.courseid}/{day}"
                                   class="w-full bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 group">
                                    <span>Flashcards</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 transform transition-transform group-hover:translate-x-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M5 12h14"></path>
                                        <path d="m12 5 7 7-7 7"></path>
                                    </svg>
                                </a>
                                <a data-sveltekit-preload-data="off" href="/quiz/{$page.params.courseid}/{day}"
                                   class="w-full bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-slate-200 text-white dark:text-slate-900 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 group">
                                    <span>Quiz</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 transform transition-transform group-hover:translate-x-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M5 12h14"></path>
                                        <path d="m12 5 7 7-7 7"></path>
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                {/if}
            {/each}
        </div>
    </div>
</div>
