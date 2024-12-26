<script module>
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
</script>

<script>
  import { Digits, focus } from '$lib/components';
  import { imageForHttpCode, phraseForHttpCode } from '$lib/game';
  import { popFrom, randInt } from '$lib/utils';

  import { scale } from 'svelte/transition';
  import { getInput } from './Digits.svelte';

  let { getCode, gameMode: curGameMode = gameModes.codeBlock } = $props();
  let missingFlag = $derived(getMissingFlag(curGameMode));

  let nextIndex = 0;
  let digitInputRef = $state();
  let httpCode = $state();
  let imageSrc = $derived(httpCode ? imageForHttpCode(httpCode) : 'cats/frame.png');
  let phrase = $derived(httpCode ? phraseForHttpCode(httpCode) : '');
  let correctDigits = $derived(httpCode.toString());
  let digits = $state(['', '', '']);

  /**
   * @param {number} gameMode
   */
  function getMissingFlag(gameMode) {
    let newMissingFlag;
    if (gameMode & gameModes.anyOne) {
      const indexPool = Array.from(Array(3).keys());
      const firstIdx = popFrom(indexPool, randInt(3));
      newMissingFlag = flags[firstIdx];
      if (gameMode & gameModes.anyTwo) {
        const secondIdx = popFrom(indexPool, randInt(2));
        newMissingFlag |= flags[secondIdx];
      }
    } else newMissingFlag = gameMode;
    return newMissingFlag;
  }

  function next() {
    httpCode = null;
    setTimeout(() => {
      httpCode = getCode();
      clearDigits();
      setTimeout(focusOnInput, 100);
    }, 100);
  }

  function focusOnInput() {
    focus(digitInputRef, nextIndex);
    nextIndex = 0;
  }

  function clearDigits() {
    for (let idx = 2; idx > -1; idx--) {
      console.log(digits[idx], correctDigits[idx]);
      if (digits[idx] != correctDigits[idx]) {
        digits[idx] = '';
        nextIndex = idx;
      } else getInput(digitInputRef, idx)?.setAttribute('disabled', 'true');
    }
    setTimeout(focusOnInput, 100);
  }

  function onSubmit() {
    if (digits.join('') == httpCode) setTimeout(next, 100);
    else clearDigits();
  }

  setTimeout(next, 100);
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
    <Digits bind:digits bind:ref={digitInputRef}></Digits>
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

<div class="flex"></div>

{#if httpCode}
  <form transition:scale onsubmit={onSubmit} class="flex flex-col items-center gap-4">
    {@render imageBlock(imageSrc, !!(missingFlag & missingElements.imageBlock))}
    <div class="flex flex-col items-center">
      {@render codeBlock(httpCode, !!(missingFlag & missingElements.codeBlock))}
      {@render phraseBlock(phrase, !!(missingFlag & missingElements.phraseBlock))}
    </div>
    <input type="submit" hidden />
  </form>
{/if}
