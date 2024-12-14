<script>
	import { Nav, Footer } from '$lib/components';
	import '../app.css';
	let { children } = $props();
</script>

<div class="p-4 sm:px-16 sm:py-4 lg:px-32 lg:py-4">
	<Nav />
	{@render children()}
	<Footer />
</div>
