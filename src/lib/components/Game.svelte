<script>
  import { randomHttpCode, imageForHttpCode, phraseForHttpCode } from '$lib/game';
  import { scale } from 'svelte/transition';

  let httpCode = $state(0);
  let imageSrc = $derived(httpCode ? imageForHttpCode(httpCode) : 'cats/frame.png');
  let phrase = $derived(httpCode ? phraseForHttpCode(httpCode) : '');

  const missingElements = {
    imageBlock: 1 << 0,
    codeBlock: 1 << 1,
    phraseBlock: 1 << 2
  };

  const flags = Object.values(missingElements);

  const gameModes = {
    ...missingElements,
    anyOne: 1 << 3,
    anyTwo: (1 << 3) | (1 << 4)
  };

  let missingFlag = $state(0);
  let gameMode = gameModes.codeBlock;

  function draw() {
    httpCode = randomHttpCode();
    if (gameMode & gameModes.anyOne) {
      const indexPool = [0, 1, 2];
      const firstIdx = indexPool.splice(Math.floor(Math.random() * 3))[0];
      missingFlag = flags[firstIdx];
      if (gameMode & gameModes.anyTwo) {
        const secondIdx = indexPool.splice(Math.floor(Math.random() * 2))[0];
        missingFlag |= flags[secondIdx];
      }
    } else {
      missingFlag = gameMode;
    }
  }

  setTimeout(draw, 100);
</script>

{#snippet imageBlock(/** @type { string } */ src, missing = false)}
  {#if missing}
    <img src="cats/frame.png" class="max-h-200" alt="" />
  {:else}
    <img {src} class="max-h-200" alt="" />
  {/if}
{/snippet}

{#snippet codeBlock(/** @type { number } */ code, missing = false)}
  {#if missing}
    <input class="bg-transparent text-center text-5xl" />
  {:else}
    <h2 class="text-5xl">{code}</h2>
  {/if}
{/snippet}

{#snippet phraseBlock(/** @type { string } */ text, missing = false)}
  {#if missing}
    <input class="bg-transparent text-center text-2xl" />
  {:else}
    <p class="text-2xl">{text}</p>
  {/if}
{/snippet}

{#if httpCode}
  <div transition:scale class="flex flex-col items-center gap-4">
    {@render imageBlock(imageSrc, !!(missingFlag & missingElements.imageBlock))}
    <div class="flex flex-col items-center">
      {@render codeBlock(httpCode, !!(missingFlag & missingElements.codeBlock))}
      {@render phraseBlock(phrase, !!(missingFlag & missingElements.phraseBlock))}
    </div>
  </div>
{/if}
