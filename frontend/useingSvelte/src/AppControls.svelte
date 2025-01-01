<script lang="ts">
  import {
    getStorageStates,
    startNewPage,
    killBrowser,
    getServices,
  } from "./lib/in.svelte";
  import { services, storageStates } from "./lib/store.svelte";
  import { onMount } from "svelte";

  onMount(() => {
    getServices();
    getStorageStates();
  });
</script>

<div class="flex flex-col items-center">
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

    <div>
      <span>Select Storage State:</span>
      <select
        class="p-2 rounded-md"
        id="StorageDisplay"
        onfocus={async () => await getStorageStates()}
        onchange={() => {}}
      >
        {#each $storageStates as storageState}
          <option value={storageState}>{storageState}</option>
        {/each}
      </select>
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
      class="bg-lime-700 hover:bg-lime-600 active:italic p-2 rounded-md text-gray-50"
      onclick={() => startNewPage()}>Start New Context</button
    >
    <button
      class="bg-rose-600 hover:bg-rose-700 active:italic p-2 rounded-md text-gray-50"
      onclick={() => killBrowser()}>Close Bowser</button
    >
  </div>
</div>
