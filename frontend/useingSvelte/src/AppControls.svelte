<script lang="ts">
  import {
    getStorageStates,
    startNewPage,
    killBrowser,
    getServices,
  } from "./lib/in.svelte";
  import { services, storageStates } from "./lib/store.svelte";
  import { onMount } from "svelte";
  import InputComponent from "./InputComponent.svelte";

  let newStateWanted: boolean = $state(false);

  onMount(() => {
    getServices();
    getStorageStates();
  });
</script>

<div class="flex flex-col items-center select-none">
  <div class="flex w-svw justify-evenly items-center mb-4">
    <div>
      <span>Select Service:</span>
      <select
        class="p-2 rounded-md"
        id="ServiceDisplay"
        onfocus={async () => await getServices()}
        onchange={() => {}}
      >
        {#each $services as service}
          <option value={service}>{service}</option>
        {/each}
      </select>
    </div>

    <div class="flex items-center gap-1">
      <span>Select Storage State:</span>
      {#if newStateWanted}
        <InputComponent />
      {:else}
        <select
          class="p-2 rounded-md w-56"
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
        class="p-1 px-3 text-xl font-mono font-bold rounded-md bg-violet-800 hover:bg-violet-700"
        title={!newStateWanted
          ? "Add New State"
          : "Select from Existing States"}
        onclick={() => (newStateWanted = !newStateWanted)}
      >
        {#if !newStateWanted}
          +
        {:else}
          -
        {/if}
      </button>
    </div>

    <div>
      <span>Context for URL:</span>
      <input
        type="text"
        class="p-2 rounded-sm"
        name="contextURL"
        id="ContextURL"
      />
    </div>

    <div>
      <label for="Autologin">
        <span>Auto Log in</span>
      </label>
      <input
        type="checkbox"
        class="p-2 outline-none"
        name="autologin"
        id="Autologin"
      />
    </div>
  </div>

  <div>
    <button
      class="bg-violet-800 hover:bg-violet-700 active:italic p-2 rounded-md text-gray-50"
      onclick={() => startNewPage()}>Start New Context</button
    >
    <button
      class="bg-orange-700 hover:bg-orange-600 active:italic p-2 rounded-md text-gray-50"
      onclick={() => killBrowser()}>Close Bowser</button
    >
  </div>
</div>
