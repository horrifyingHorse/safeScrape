<script>
  import { selectedConsole } from "./lib/store.svelte";
  const { type = "display", idx, name } = $props();
</script>

{#if type == "button"}
  <button
    aria-hidden="true"
    class={`text-xl p-1 px-4 cursor-pointer ${$selectedConsole == idx ? "bg-[#282c34] text-[#babbf1]" : "text-[#ebebeb]"}`}
    onclick={() => ($selectedConsole = idx)}
  >
    {#if $selectedConsole == idx}
      <span>{idx + 1}» {name}</span>
    {:else}
      <span>{idx + 1}: {name}</span>
    {/if}
  </button>
{:else}
  <div
    id={`${name}`}
    class={`font-mono overflow-hidden h-full overflow-y-auto ${$selectedConsole == idx ? "block" : "hidden"}`}
  ></div>
{/if}
