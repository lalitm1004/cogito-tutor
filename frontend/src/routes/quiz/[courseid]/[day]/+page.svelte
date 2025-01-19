<script lang="ts">
    import type { DailyContent } from "$lib/types/DailyContent.types";
    import { fly, fade } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
    import { page } from '$app/stores'
    import { writable } from 'svelte/store';

    export let data: DailyContent;

    // Quiz state management
    let currentQuestionIndex = 0;
    let selectedOption: string | null = null;
    let hasSubmitted = false;
    let showExplanation = false;
    let score = writable(0);
    let answeredQuestions = writable(new Set<number>());

    $: currentQuestion = data.quiz.quiz_questions[currentQuestionIndex];
    $: progress = ((currentQuestionIndex + 1) / data.quiz.quiz_questions.length) * 100;
    $: isLastQuestion = currentQuestionIndex === data.quiz.quiz_questions.length - 1;
    $: hasAnswered = $answeredQuestions.has(currentQuestionIndex);

    function handleOptionSelect(option: string) {
        if (!hasAnswered) {
            selectedOption = option;
        }
    }

    function submitAnswer() {
        if (selectedOption && !hasAnswered) {
            hasSubmitted = true;
            $answeredQuestions = $answeredQuestions.add(currentQuestionIndex);

            if (selectedOption === currentQuestion.answer) {
                score.update(n => n + 1);
            }
        }
    }

    function nextQuestion() {
        if (currentQuestionIndex < data.quiz.quiz_questions.length - 1) {
            currentQuestionIndex++;
            selectedOption = null;
            hasSubmitted = false;
            showExplanation = false;
        }
    }

    function previousQuestion() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            selectedOption = null;
            hasSubmitted = false;
            showExplanation = false;
        }
    }

    function resetQuiz() {
        currentQuestionIndex = 0;
        selectedOption = null;
        hasSubmitted = false;
        showExplanation = false;
        score.set(0);
        answeredQuestions.set(new Set());
    }
</script>

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
                    {data.quiz.topic}
                </h1>
                <div class="flex items-center flex-wrap gap-4 text-slate-600 dark:text-slate-400 mt-4">
                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                        </svg>
                        <span>Difficulty: {data.quiz.difficulty}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 20v-6M6 20V10M18 20V4"/>
                        </svg>
                        <span>Score: {$score}/{data.quiz.quiz_questions.length}</span>
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

        <!-- Main Quiz Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Sidebar Info -->
            <div class="space-y-4">
                <div class="bg-white dark:bg-slate-900 rounded-xl p-6 shadow-sm">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">Question Topic</h3>
                    <p class="text-slate-600 dark:text-slate-400">{currentQuestion.subtopic}</p>
                </div>
                <div class="bg-white dark:bg-slate-900 rounded-xl p-6 shadow-sm">
                    <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-3">Quiz Progress</h3>
                    <div class="space-y-2">
                        <div class="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                            <span>Questions Answered</span>
                            <span>{$answeredQuestions.size}/{data.quiz.quiz_questions.length}</span>
                        </div>
                        <div class="flex justify-between text-sm text-slate-600 dark:text-slate-400">
                            <span>Current Score</span>
                            <span>{(($score / data.quiz.quiz_questions.length) * 100).toFixed(1)}%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quiz Question Card -->
            <div class="md:col-span-2">
                <div class="bg-white dark:bg-slate-900 rounded-xl shadow-lg p-8 space-y-6"
                     in:fly={{ y: 20, duration: 300, easing: quintOut }}>
                    <!-- Question -->
                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium px-3 py-1 bg-slate-100 dark:bg-slate-700 rounded-full text-slate-600 dark:text-slate-400">
                                Question {currentQuestionIndex + 1}/{data.quiz.quiz_questions.length}
                            </span>
                        </div>
                        <p class="text-xl text-slate-900 dark:text-slate-100">
                            {currentQuestion.question}
                        </p>
                    </div>

                    <!-- Options -->
                    <div class="space-y-3">
                        {#each ['A', 'B', 'C', 'D'] as option}
                            {@const optionContent = currentQuestion[`option_${option}`]}
                            {@const isCorrect = currentQuestion.answer === option}
                            <button
                                    class="w-full p-4 rounded-lg border-2 transition-all duration-200 flex items-center space-x-3
                                    {selectedOption === option ? 'border-blue-500 dark:border-blue-400' : 'border-slate-200 dark:border-slate-700'}
                                    {hasSubmitted && isCorrect ? 'bg-green-50 dark:bg-green-900/20 border-green-500' : ''}
                                    {hasSubmitted && selectedOption === option && !isCorrect ? 'bg-red-50 dark:bg-red-900/20 border-red-500' : ''}
                                    {!hasAnswered ? 'hover:border-blue-500 dark:hover:border-blue-400' : ''}"
                                    on:click={() => handleOptionSelect(option)}
                                    disabled={hasAnswered}>
                                <span class="w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                                    {option}
                                </span>
                                <span class="flex-grow text-left text-slate-700 dark:text-slate-300">
                                    {optionContent}
                                </span>
                                {#if hasSubmitted && isCorrect}
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M20 6L9 17l-5-5"/>
                                    </svg>
                                {/if}
                            </button>
                        {/each}
                    </div>

                    <!-- Explanation Section -->
                    {#if hasSubmitted}
                        <div class="mt-6" in:fade={{ duration: 200 }}>
                            <button
                                    class="text-blue-500 dark:text-blue-400 text-sm font-medium flex items-center space-x-2"
                                    on:click={() => showExplanation = !showExplanation}>
                                <span>{showExplanation ? 'Hide' : 'Show'} Explanation</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-200 {showExplanation ? 'rotate-180' : ''}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="m6 9 6 6 6-6"/>
                                </svg>
                            </button>
                            {#if showExplanation}
                                <div class="mt-4 p-4 bg-slate-50 dark:bg-slate-800 rounded-lg" in:fade={{ duration: 200 }}>
                                    <p class="text-slate-700 dark:text-slate-300">
                                        {currentQuestion.explanation}
                                    </p>
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            </div>
        </div>

        <!-- Navigation Controls -->
        <div class="flex justify-center gap-4">
            <button
                    class="px-6 py-3 rounded-lg bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                    disabled={currentQuestionIndex === 0}
                    on:click={previousQuestion}>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="m15 18-6-6 6-6"/>
                </svg>
                <span>Previous</span>
            </button>

            {#if !hasAnswered}
                <button
                        class="px-6 py-3 rounded-lg bg-blue-500 hover:bg-blue-600 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                        disabled={!selectedOption}
                        on:click={submitAnswer}>
                    <span>Submit Answer</span>
                </button>
            {:else if !isLastQuestion}
                <button
                        class="px-6 py-3 rounded-lg bg-green-500 hover:bg-green-600 text-white transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                        on:click={nextQuestion}>
                    <span>Next Question</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </button>
            {:else}
                <button
                        class="px-6 py-3 rounded-lg bg-purple-500 hover:bg-purple-600 text-white transition-all duration-200 shadow-sm hover:shadow flex items-center space-x-2"
                        on:click={resetQuiz}>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                        <path d="M3 3v5h5"/>
                    </svg>
                    <span>Restart Quiz</span>
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    /* Add any additional custom styles here if needed */
</style>
