<script lang="ts">
  import { updatePageState } from "./lib/in.svelte";
  import { pgState } from "./lib/store.svelte";
  const { category, detail, detailType, inputId = "" } = $props();
  let addedStyles: string = "";
  let addedDetails: string = "";
  let handleClick =
    inputId === "auto_login"
      ? pgState.toggleAutoLogin
      : pgState.toggleAllowDelay;

  if (category == "Id") {
    addedStyles = "italic text-zinc-400";
    addedDetails = "#";
  }
</script>

{#if detailType === "text"}
  <div class="flex">
    <div class="w-1/3 flex justify-around">{category}</div>
    <div class="w-1/3 flex justify-around">:</div>
    <div class="w-1/3 flex justify-around {addedStyles}">
      {addedDetails}{detail}
    </div>
  </div>
{:else if detailType === "checkbox"}
  <div
    aria-hidden="true"
    class="flex"
    onclick={() => {
      handleClick();
      updatePageState();
    }}
  >
    <div class="w-1/3 flex justify-around">{category}</div>
    <div class="w-1/3 flex justify-around">:</div>
    <div class="w-1/3 flex justify-around">
      <input id={inputId} type="checkbox" checked={detail} />
    </div>
  </div>
{/if}
