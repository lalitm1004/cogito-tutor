<script lang="ts">
    import Hero from "$lib/components/home/Hero.svelte";
    import WhyCogito from "$lib/components/home/WhyCogito.svelte";
</script>

<svelte:head>
    <title>Cogito</title>
    <meta name="description" content="Revolutionize learning with Cogito">
</svelte:head>

<main>
    <section>
        <div class="h-dvh w-dvw">
            <Hero />
        </div>
    </section>

    <section>
        <div class="h-dvh w-dvw">
            <WhyCogito />
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
