<script lang="ts">
    let { children } = $props();
</script>

<svelte:head>
    <title>Flashcards</title>
</svelte:head>

{@render children()}
