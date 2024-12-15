<script>
  import { page } from '$app/stores';
  import { Nav, Footer } from '$lib/components';

  import '../app.css';
  let { children } = $props();

  const pageName = $derived($page.data.name);
  const siteName = 'HTTP Claws Game';
  const titleSuffix = $derived(pageName ? ' • ' + pageName : '');
</script>

<svelte:head>
  <title>{siteName}{titleSuffix}</title>
</svelte:head>

<div class="m-auto max-w-screen-2xl p-4 sm:px-16 sm:py-4 lg:px-32 lg:py-4">
  <Nav />
  {@render children()}
  <Footer />
</div>
