<script lang="ts">
  import { stateName } from "./lib/store.svelte";
  let editMode: boolean = $state(false);

  function focusOnMount(node: HTMLElement) {
    node.focus();
  }
</script>

<div
  id="NewStateName"
  class={`flex justify-center w-56`}
  aria-hidden="true"
  role="button"
  tabindex="0"
  onclick={() => {
    editMode = true;
  }}
>
  {#if editMode}
    <div class="flex w-full">
      <div class="w-3/4">
        <input
          class="italic w-full outline-none border-none bg-transparent text-center p-2"
          type="text"
          bind:value={$stateName}
          onblur={() => {
            editMode = false;
          }}
          onkeydown={(event) => {
            if (event.key === "Enter") {
              editMode = false;
            }
          }}
          use:focusOnMount
        />
      </div>
      <div
        class="rounded-xl rounded-l-none border-0 w-1/4 text-zinc-500 bg-zinc-800 text-center p-2"
      >
        .state
      </div>
    </div>
  {:else}
    <div class="cursor-text p-2 border-none">
      {$stateName}.state
    </div>
  {/if}
</div>
