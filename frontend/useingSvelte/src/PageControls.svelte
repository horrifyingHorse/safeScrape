<script lang="ts">
  import {
    getPageInfoById,
    saveStorageState,
    toggleScrape,
  } from "./lib/in.svelte";
  import { pgState, pgInstances } from "./lib/store.svelte";
  import PageDiv from "./PageDiv.svelte";
</script>

<div class="w-[839px] h-[378px] border-[#babbf1] border-2">
  <div
    class="w-full min-h-[32px] px-[25px] py-[5px] border-b-2 border-b-[#babbf1] flex justify-between mb-2"
  >
    <div class="text-xl flex gap-x-[10px] text-[#babbf1] select-none">
      <img src="ri-file-settings-line.svg" alt="" />
      PageControls
    </div>
    <div>
      <select
        name="page"
        id="PageSelction"
        class="rounded-md px-4 bg-[#babbf1] text-[#babbf1] bg-opacity-20"
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
    </div>
    <div class="flex gap-x-6 justify-center">
      <div class="flex justify-center">
        <img src="svg-path.svg" alt="" />
      </div>
      <div>
        <img src="ri-close-large-line.svg" alt="" title="Close" />
      </div>
    </div>
  </div>

  <div class="w-full h-[85%] flex px-4">
    <div class="h-full w-[40%] space-y-4 border-r-2 border-r-[#babbf1]">
      <div class="underline font-bold">Status</div>

      <PageDiv
        category="Service ID"
        detailType="text"
        detail={pgState.pageId}
      />

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
        category="Scrape Status"
        detailType="text"
        detail={pgState.pageState[0].scrape}
      />
    </div>

    <div class="px-4 h-full flex flex-col justify-between">
      <div class="flex flex-col space-y-4">
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
      </div>
      <div class="flex flex-col space-y-4">
        <button
          class="p-2 rounded-lg bg-[#f2cc8f] text-[#171717]"
          onclick={null}>Pause Playwritght</button
        >
        <button
          class="p-2 rounded-lg bg-[#f2cc8f] text-[#171717]"
          onclick={saveStorageState}>Save State</button
        >
        <button class="p-2 rounded-lg bg-[#81b29a]" onclick={toggleScrape}>
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
