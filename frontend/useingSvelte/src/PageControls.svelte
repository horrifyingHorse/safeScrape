<script lang="ts">
  import {
    getPageInfoById,
    saveStorageState,
    toggleScrape,
  } from "./lib/in.svelte";
  import { pgState, pgInstances } from "./lib/store.svelte";
  import PageDiv from "./PageDiv.svelte";
</script>

<div id="PageControlsDisplay">
  <div class="text-3xl pl-3">Page Controls</div>
  <div class="w-full flex p-3 h-auto">
    <div class="w-full p-2" id="InfoDisplay">
      <select
        name="page"
        id="PageSelction"
        class="p-2 px-4 rounded-sm"
        onchange={async (event: Event) =>
          await getPageInfoById(
            Number((event.target as HTMLSelectElement).value),
          )}
      >
        {#each pgInstances.iterableInstanceStore as pgInstance, idx}
          {#if pgInstance !== undefined}
            <option value={idx}>{pgInstance}</option>
          {/if}
        {/each}
      </select>
      <div class="h-full pt-3 space-y-4 select-none">
        <PageDiv category="Id" detailType="text" detail={pgState.pageId} />

        <PageDiv
          category="Service"
          detailType="text"
          detail={pgState.pageState[0].service}
        />

        <PageDiv
          category="Storage State"
          detailType="text"
          detail={pgState.pageState[0].storage_state}
        />

        <PageDiv
          category="Auto Login"
          detailType="checkbox"
          detail={pgState.pageState[0].auto_login}
          inputId="auto_login"
        />

        <PageDiv
          category="Allow Human Like Delay"
          detailType="checkbox"
          detail={pgState.pageState[0].allow_delay}
          inputId="allow_delay"
        />

        <PageDiv
          category="Scrape Status"
          detailType="text"
          detail={pgState.pageState[0].scrape}
        />

        <div class="flex justify-around">
          <button
            class="p-2 rounded-lg bg-violet-800 hover:bg-violet-700"
            onclick={saveStorageState}>Save State</button
          >
          <button
            class="p-2 w-32 rounded-lg bg-violet-800 hover:bg-violet-700"
            onclick={toggleScrape}
          >
            {#if pgState.pageState[0].scrape}
              Stop Scrape
            {:else}
              Start Scrape
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
