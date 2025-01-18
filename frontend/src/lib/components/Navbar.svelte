<script lang="ts">
    import { onNavigate } from "$app/navigation";
    import { page } from "$app/state";
    import { setTheme, theme } from "$lib/stores/themeStore";
    import { onMount } from "svelte";
    import { fade, fly, slide } from "svelte/transition";

    let toggleThemeButtonDesktop: HTMLButtonElement | null = $state(null);
    let toggleThemeButtonMobile: HTMLButtonElement | null = $state(null);

    const internalAnchors = [
        { id: 0, href: "/", display: "Home" },
        { id: 1, href: "/tutor", display: "Tutor" },
    ]

    const toggleTheme = () => {
        if (
            !(toggleThemeButtonDesktop || toggleThemeButtonMobile) ||
            !document.startViewTransition ||
            window.matchMedia('(prefers-reduced-motin: reduce)').matches
        ) {
            setTheme($theme === 'dark' ? 'light' : 'dark');
            return;
        }

        document.startViewTransition(async() => {
            setTheme($theme === 'dark' ? 'light' : 'dark');
        })
    }

    let isMenuOpen: boolean = $state(false);
    const toggleMenuDisplay = () => {
        isMenuOpen = !isMenuOpen;
    }

    onNavigate(() => {
        isMenuOpen = false;
    })

    $effect(() => {
        document.body.style.overflow = isMenuOpen ? 'hidden' : 'auto';
    })

    let display: boolean = $state(false);
    onMount(() => {
        display = true;
    })
</script>

{#if display}
<nav transition:fly={{ y: '-100%' }} class={`fixed top-0 left-0 h-[40px] w-full z-30`}>
    <!-- desktop navbar -->
    <div class={`mobile:hidden h-full mt-4 px-6 flex flex-row justify-end items-center gap-3`}>
        <!-- internal achors -->
        <div
            class={`apply-card h-full rounded-full flex items-center px-5 gap-4`}
        >
            {#each internalAnchors as item (item.id)}
                <a
                    data-currentpage={page.url.pathname === item.href}
                    class={`data-[currentpage="true"]:scale-[1.1] hover:scale-[1.0] scale-[0.9] data-[currentpage="true"]:font-bold data-[currentpage="true"]:cursor-default dark:data-[currentpage="true"]:text-amber-50 dark:hover:text-amber-50 dark:text-neutral-400 transition-all duration-200`}
                    aria-label={`${item.display.toLowerCase()}-href`}
                    href={item.href}
                >{item.display}</a>
            {/each}
        </div>

        <!-- theme toggle -->
        <button
            bind:this={toggleThemeButtonDesktop}
            class={`apply-card group h-full aspect-square rounded-full grid place-items-center`}
            aria-label="toggle-theme"
            onclick={() => toggleTheme()}
        >
            {#if $theme === 'light'}
                <svg class="h-[20px] aspect-square group-hover:stroke-[2.8] stroke-2 stroke-neutral-800 transition-all duration-300 lucide lucide-moon" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" >
                    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
                </svg>
            {:else}
                <svg class="h-[20px] aspect-square group-hover:stroke-[2.5] stroke-2 group-hover:stroke-amber-50 stroke-neutral-400 transition-all duration-300 lucide lucide-sun" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" >
                    <circle cx="12" cy="12" r="4"/>
                    <path d="M12 2v2"/>
                    <path d="M12 20v2"/>
                    <path d="m4.93 4.93 1.41 1.41"/>
                    <path d="m17.66 17.66 1.41 1.41"/>
                    <path d="M2 12h2"/>
                    <path d="M20 12h2"/>
                    <path d="m6.34 17.66-1.41 1.41"/>
                    <path d="m19.07 4.93-1.41 1.41"/>
                </svg>
            {/if}
        </button>
    </div>

    <!-- mobile navbar -->
    <div class={`desktop:hidden mt-4 px-4 h-full flex justify-end`}>
        {#if isMenuOpen}
            <!-- screen effect -->
            <button transition:fade={{ duration: 100 }} aria-label={`exit-menu`} onclick={() => toggleMenuDisplay()} class={`absolute top-0 left-0 h-dvh w-dvw bg-black/70`}></button>
        {/if}

        <button
            data-menuopen={isMenuOpen}
            onclick={() => toggleMenuDisplay()} class={`apply-card rounded-xl grid place-items-center px-4 dark:data-[menuopen="true"]:bg-neutral-800/40 data-[menuopen="true"]:bg-neutral-50/80`}
        >
            Menu
        </button>

        {#if isMenuOpen}
            <div
                transition:slide
                data-menuopen={isMenuOpen}
                class={`absolute right-4 top-16 apply-card w-[150px] flex flex-col items-center rounded-xl py-3 dark:data-[menuopen="true"]:bg-neutral-800/40 data-[menuopen="true"]:bg-neutral-50/80`}
            >
                <!-- internal anchors -->
                <div
                    class={`w-[90%] flex flex-col items-center gap-4 px-2 text-lg`}
                >
                    {#each internalAnchors as item (item.id)}
                        <a
                            data-currentpage={page.url.pathname === item.href}
                            class={`w-full text-right data-[currentpage="true"]:scale-[1.1] data-[currentpage="true"]:-translate-x-2 hover:scale-[1.0] scale-[0.9] data-[currentpage="true"]:font-bold data-[currentpage="true"]:cursor-default dark:data-[currentpage="true"]:text-amber-100 dark:hover:text-amber-100 dark:text-amber-50 transition-all duration-200`}
                            aria-label={`${item.display.toLowerCase()}-href`}
                            href={item.href}
                        >{item.display}</a>
                    {/each}
                </div>

                <hr class={`w-[80%] mt-2 border-neutral-400/40`}/>

                <!-- title + theme toggle -->
                <div class={`w-[90%] mt-3 flex items-center justify-center gap-4`}>
                    <p class={`font-bespoke text-xl`}>Cogito</p>

                    <!-- theme toggle -->
                    <button
                        bind:this={toggleThemeButtonMobile}
                        class={`group h-[25px] aspect-square rounded-full grid place-items-center`}
                        aria-label="toggle-theme"
                        onclick={() => toggleTheme()}
                    >
                        {#if $theme === 'light'}
                            <svg class="h-[25px] aspect-square group-hover:stroke-[2.8] stroke-2 stroke-neutral-800 transition-all duration-300 lucide lucide-moon" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" >
                                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
                            </svg>
                        {:else}
                            <svg class="h-[25px] aspect-square group-hover:stroke-[2.5] stroke-2 group-hover:stroke-neutral-50 stroke-neutral-400 transition-all duration-300 lucide lucide-sun" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" >
                                <circle cx="12" cy="12" r="4"/>
                                <path d="M12 2v2"/>
                                <path d="M12 20v2"/>
                                <path d="m4.93 4.93 1.41 1.41"/>
                                <path d="m17.66 17.66 1.41 1.41"/>
                                <path d="M2 12h2"/>
                                <path d="M20 12h2"/>
                                <path d="m6.34 17.66-1.41 1.41"/>
                                <path d="m19.07 4.93-1.41 1.41"/>
                            </svg>
                        {/if}
                    </button>
                </div>
            </div>
        {/if}
    </div>
</nav>
{/if}