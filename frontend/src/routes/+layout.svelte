<script lang="ts">
    import Navbar from '$lib/components/Navbar.svelte';
    import { setDevice } from '$lib/stores/deviceStore';
    import { setTheme, theme, TOKEN_NAME as theme_token } from '$lib/stores/themeStore';
    import '$lib/styles/tailwind.css';    
    import { getCookie } from '$lib/utils/cookie';
    import { onMount } from 'svelte';

    let { children } = $props();

    const handleResize = () => {
        setDevice(
            window.matchMedia('(max-width: 767px)').matches ?
            'mobile' : 'desktop'
        );
    }

    onMount(() => {
        // handle theme
        const themeCookie = getCookie(document.cookie, theme_token) as Theme | null;
        if (themeCookie) theme.set(themeCookie);
        else if (window.matchMedia('(prefers-color-scheme: light)').matches) setTheme('light');
        else setTheme('dark');

        // handle device
        if (window.matchMedia('(max-width: 767px)').matches) setDevice('mobile');
        else setDevice('desktop');
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    })
</script>

<Navbar />
{@render children()}
