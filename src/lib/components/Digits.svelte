<script module>
  /**
   * @param {HTMLElement?} ref
   * @param {number} idx
   */
  export function getInput(ref, idx = 0) {
    return ref?.querySelectorAll('input')[idx];
  }

  /**
   * @param {HTMLElement?} ref
   * @param {number} idx
   */
  export function focus(ref, idx = 0) {
    const input = getInput(ref, idx);
    input?.focus();
    input?.setSelectionRange(0, 0);
  }
</script>

<script>
  let { ref = $bindable(), digits = $bindable() } = $props();

  /**
   * @param {number} idx
   * @param {string} digit
   * @returns {number}
   */
  function setDigitAt(idx, digit) {
    digit = digit.trim();
    const first = digit[0];
    const last = digit[digit.length - 1];
    if (digit.match(/^\d?\d$/)) digits[idx] = digits[idx] == first ? last : first;
    else return 0;
    return digits[idx] ? 1 : -1;
  }

  /**
   * @param {number} idx
   * @param {KeyboardEvent} ev
   */
  function handleKey(idx, ev) {
    /** @type {HTMLInputElement} */
    // @ts-ignore
    const target = ev.target;
    if (['Delete', 'Backspace'].includes(ev.code)) target.value = '';
    if (['Backspace', 'ArrowLeft'].includes(ev.code)) focus(ref, idx - 1);
    else if (['Delete', 'ArrowRight'].includes(ev.code)) focus(ref, idx + 1);
  }
</script>

<div class="flex" bind:this={ref}>
  {#each Array(3).keys() as idx}
    <input
      bind:value={() => digits[idx], (digit) => focus(ref, idx + setDigitAt(idx, digit))}
      onkeydown={(ev) => handleKey(idx, ev)}
      type="text"
      class="w-20 bg-transparent text-center text-5xl"
      required={true}
    />
  {/each}
</div>
