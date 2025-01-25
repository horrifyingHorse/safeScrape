<script lang="ts">
  import {
    getStorageStates,
    startNewPage,
    killBrowser,
    getServices,
  } from "./lib/in.svelte";
  import { services, storageStates, newStateWanted } from "./lib/store.svelte";
  import { onMount } from "svelte";
  import InputComponent from "./InputComponent.svelte";

  onMount(async () => {
    getServices();
    await getStorageStates();
  });
</script>

<div class="w-[676px] h-[211px] border-[#babbf1] border-2 m-10">
  <div
    class="text-xl w-full min-h-[32px] px-[25px] py-[5px] border-b-2 border-b-[#babbf1] flex justify-between mb-4"
  >
    <div class="flex gap-x-[10px] text-[#babbf1] select-none">
      <img src="ri-user-settings-line.svg" alt="" />
      AppControls
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

  <div class="h-[80%] w-full">
    <div class="w-full flex justify-around pb-2">
      <div class="w-[40%] flex justify-between items-center gap-4 px-6">
        <span>Service:</span>
        <select
          class="rounded-md p-1 bg-[#babbf1] text-[#171717]"
          id="ServiceDisplay"
          onfocus={async () => await getServices()}
          onchange={() => {}}
        >
          {#each $services as service}
            <option value={service}>{service}</option>
          {/each}
        </select>
      </div>

      <div class="w-[60%] flex justify-between items-center gap-4 px-6">
        <span>Storage:</span>
        {#if $newStateWanted}
          <InputComponent />
        {:else}
          <select
            class="w-48 rounded-md p-1 bg-[#babbf1] text-[#171717]"
            id="StorageDisplay"
            onfocus={async () => await getStorageStates()}
            onchange={() => {}}
          >
            {#each $storageStates as storageState}
              <option value={storageState}>{storageState}</option>
            {/each}
          </select>
        {/if}
        <button
          class="p-1 px-3 text-xl font-mono rounded-md text-[#171717] bg-[#babbf1]"
          title={!$newStateWanted
            ? "Add New State"
            : "Select from Existing States"}
          onclick={() => {
            if ($newStateWanted && $storageStates.length == 0) {
              console.log("No existing states");
              return;
            }
            newStateWanted.set(!$newStateWanted);
          }}
        >
          {#if !$newStateWanted}
            +
          {:else}
            -
          {/if}
        </button>
      </div>
    </div>

    <div class="w-full flex justify-around pb-2">
      <div class="w-[40%] flex justify-between items-center gap-4 px-6">
        <label
          for="Autologin"
          title={$newStateWanted
            ? "Cannot automate in a New State"
            : "Automate service login"}
        >
          <span>Auto Log in:</span>
        </label>

        <!-- Uncheck this input when newStateWanted disables it -->
        <input
          type="checkbox"
          class="p-2 outline-none"
          name="autologin"
          id="Autologin"
          disabled={$newStateWanted}
        />
      </div>

      <div class="w-[60%] flex justify-around items-center gap-4 px-6">
        <span>URL:</span>
        <input
          type="text"
          class="p-1 outline-none bg-[#babbf1] text-[#171717] rounded-sm"
          name="contextURL"
          id="ContextURL"
        />
      </div>
    </div>

    <div class="w-full flex justify-around mt-2 px-12">
      <button
        class="bg-[#81b29a] active:italic p-2 rounded-md text-gray-50"
        onclick={() => startNewPage()}>Start New Context</button
      >
      <button
        class="bg-[#e07a5f] active:italic p-2 rounded-md text-gray-50"
        onclick={() => killBrowser()}>Close Bowser</button
      >
    </div>
  </div>
</div>
