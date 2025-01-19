<script lang="ts">
    import type { DailyContent } from "$lib/types/DailyContent.types";
    import { fly, fade } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
    import {page} from '$app/stores'

    export let data: DailyContent;

    let currentIndex = 0;
    let isFlipped = false;
    let showHint = false;

    $: currentCard = data.flashcards.flashcard_pairs[currentIndex];
    $: progress = ((currentIndex + 1) / data.flashcards.flashcard_pairs.length) * 100;

    function nextCard() {
        if (currentIndex < data.flashcards.flashcard_pairs.length - 1) {
            isFlipped = false;
            showHint = false;
            currentIndex++;
        }
    }

    function previousCard() {
        if (currentIndex > 0) {
            isFlipped = false;
            showHint = false;
            currentIndex--;
        }
    }

    function flipCard() {
        isFlipped = !isFlipped;
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'ArrowRight') nextCard();
        if (event.key === 'ArrowLeft') previousCard();
        if (event.key === ' ') flipCard();
    }
</script>

<svelte:window on:keydown={handleKeydown}/>

<div class="min-h-[calc(100dvh-80px)] w-full px-4 py-8 bg-slate-50 dark:bg-slate-950">
    <div class="max-w-5xl mx-auto">
        <!-- Back Button -->
        <div class="mb-6">
            <a href={`/tutor/${$page.params.courseid}`}
               class="inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all duration-200 shadow-sm hover:shadow text-slate-600 dark:text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 12H5"/>
                    <path d="M12 19l-7-7 7-7"/>
                </svg>
                <span>Back to Course</span>
            </a>
        </div>

        <!-- Header Section -->
        <div class="mb-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h1 class="font-bespoke md:text-5xl text-4xl bg-gradient-to-r from-slate-900 to-slate-700 dark:from-slate-100 dark:to-slate-300 bg-clip-text text-transparent">
                    {data.flashcards.topic}
                </h1>
                <div class="flex items-center space-x-4 text-slate-600 dark:text-slate-400 mt-4">
                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="4" width="20" height="16" rx="2"/>
                            <path d="M12 8v8"/>
                            <path d="M8 12h8"/>
                        </svg>
                        <span>Total Cards: {data.flashcards.flashcard_pairs.length}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <path d="M12 6v6l4 2"/>
                        </svg>
                        <span>Current: {currentIndex + 1}</span>
                    </div>
                </div>
            </div>

            <!-- Progress Section -->
            <div class="flex flex-col justify-center">
                <div class="flex justify-between text-sm text-slate-600 dark:text-slate-400 mb-2">
                    <span>Progress</span>
                    <span>{progress.toFixed(0)}%</span>
                </div>
                <div class="h-2 bg-slate-200 dark:bg-slate-900 rounded-full overflow-hidden">
                    <div class="h-full bg-green-500 dark:bg-green-400 transition-all duration-300 ease-out"
                         style="width: {progress}%">
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Flashcard Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Sidebar Info -->
            <div class="space-y-4">
                <div class="bg-white dark:bg-slate-900 rounded-xl p-6 shadow-sm">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">Current Topic</h3>
                    <p class="text-slate-600 dark:text-slate-400">{currentCard.subtopic}</p>
                </div>
                <div class="bg-white dark:bg-slate-900 rounded-xl p-6 shadow-sm">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">Navigation</h3>
                    <div class="text-sm text-slate-600 space-y-2 dark:text-slate-400">
                        <p><kbd class="inline-block px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 border border-gray-300 rounded dark:text-gray-200 dark:bg-gray-700 dark:border-gray-600">←</kbd> Previous Card</p>
                        <p><kbd class="inline-block px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 border border-gray-300 rounded dark:text-gray-200 dark:bg-gray-700 dark:border-gray-600">→</kbd> Next Card</p>
                        <p><kbd class="inline-block px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 border border-gray-300 rounded dark:text-gray-200 dark:bg-gray-700 dark:border-gray-600">Space</kbd> to Flip</p>
                    </div>
                </div>
            </div>

            <!-- Flashcard -->
            <div class="md:col-span-2"
                 in:fly={{ y: 20, duration: 300, easing: quintOut }}>
                <div class="bg-white dark:bg-slate-900 rounded-xl shadow-lg p-8 min-h-[400px] cursor-pointer relative overflow-hidden"
                     on:click={flipCard}>
                    {#key isFlipped}
                        <div in:fly={{ x: isFlipped ? 100 : -100, duration: 300, easing: quintOut }}
                             class="h-full">
                            <div class="flex flex-col h-full">
                                <div class="mb-4 flex justify-between items-center">
                                    <span class="text-sm font-medium px-3 py-1 bg-slate-100 dark:bg-slate-700 rounded-full text-slate-600 dark:text-slate-400">
                                        {isFlipped ? 'Answer' : 'Question'}
                                    </span>
                                </div>

                                <div class="flex-grow flex items-center justify-center">
                                    <p class="text-2xl text-center text-slate-900 dark:text-slate-100">
                                        {isFlipped ? currentCard.answer : currentCard.question}
                                    </p>
                                </div>

                                <div class="mt-4 text-center">
                                    <span class="text-sm text-slate-500 dark:text-slate-400">
                                        Click to {isFlipped ? 'see question' : 'reveal answer'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    {/key}
                </div>
            </div>
        </div>

        <!-- Navigation Controls -->
        <div class="flex justify-center gap-4">
            <button
                    class="px-6 py-3 rounded-lg bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                    disabled={currentIndex === 0}
                    on:click={previousCard}>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m15 18-6-6 6-6"/>
                </svg>
                <span>Previous</span>
            </button>

            <button
                    class="px-6 py-3 rounded-lg bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                    disabled={currentIndex === data.flashcards.flashcard_pairs.length - 1}
                    on:click={nextCard}>
                <span>Next</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m9 18 6-6-6-6"/>
                </svg>
            </button>
        </div>
    </div>
</div>

<style>
    /* Add any additional custom styles here if needed */
</style>
