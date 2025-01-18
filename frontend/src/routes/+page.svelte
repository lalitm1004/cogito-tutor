<script lang="ts">
    import Hero from "$lib/components/home/Hero.svelte";
    import { sessionStore } from "$lib/stores/sessionStore";
    import { getCookie } from "$lib/utils/cookie";
    import { onMount } from "svelte";

    onMount(() => {
        const token = getCookie(document.cookie, 'cogito-auth')!;
        const profile: Profile = JSON.parse(decodeURIComponent(getCookie(document.cookie, 'cogito-profile')!))

        sessionStore.set({
            token,
            profile
        });
    })
</script>

<main>
    <section>
        <div class={`h-dvh w-dvw`}>
            <Hero />
        </div>
    </section>

    <section>
        <div class={`h-dvh w-dvw`}>
            sex2
        </div>
    </section>
</main>

<style>
    main {
        scroll-snap-type: y mandatory;
        overflow-y: scroll;
        overflow-x: hidden;
        height: 100dvh;
    }

    section {
        scroll-snap-align: start;
    }
</style>