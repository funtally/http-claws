<script>
  import { pushState } from '$app/navigation';
  import { page } from '$app/state';
  import { Game } from '$lib/components';
  import { randomHttpCode, HASHCAT } from '$lib/game';
  import md5 from 'crypto-js/md5';

  const initHash = page.url.searchParams.get('h');
  const firstCode = initHash ? HASHCAT[initHash] : null;

  function getCode(initial = [firstCode]) {
    const code = initial.pop() || randomHttpCode();
    pushState('', { h: md5(code).toString() });
    return code;
  }
</script>

<main>
  <Game {getCode} />
</main>
