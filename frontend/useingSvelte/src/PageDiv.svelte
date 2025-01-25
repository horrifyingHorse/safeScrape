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

  if (category == "Service ID") {
    addedStyles = "italic text-zinc-400";
    addedDetails = "#";
  }
</script>

{#if detailType === "text"}
  <div class="flex flex-col">
    <div class="flex w-full justify-center">
      <span class="text-[#babbf1]">{category}</span> :
    </div>
    <div
      class="flex justify-around {addedStyles} {detail === true
        ? 'text-[#81b29a]'
        : 'text-[#e07a5f]'}"
    >
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
    <div>
      <span class="select-none cursor-pointer">{category} : </span>
      <input id={inputId} type="checkbox" checked={detail} />
    </div>
  </div>
{/if}
