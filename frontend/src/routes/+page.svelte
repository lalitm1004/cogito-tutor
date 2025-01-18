<svelte:head>
    <title>Cogito</title>
    <meta name="description" content="A revolutionary AI-Tutor">
</svelte:head>

<script lang="ts">
    import Hero from "$lib/components/home/Hero.svelte";
</script>

<main>
    <section>
        <div class={`h-dvh w-dvw`}>
            <Hero />
        </div>
    </section>

    <section>
        <div class={`h-dvh w-dvw`}>
            somethnig and all bro
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