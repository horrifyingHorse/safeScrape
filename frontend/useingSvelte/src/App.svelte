<script lang="ts">
  import { scrapeState } from "./lib/store.svelte";
  import { getStorageStates, startContext, getServices } from "./lib/in.svelte";
  import { onMount } from "svelte";

  onMount(() => {
    getServices();
    getStorageStates();
  });
</script>

<!--
Features:
  [ ] Launch new page (in a new Context) of the headful playwright
      (+) Select state (cookies, auth)
      (+) URL to start context with
      ( ) Auto Log in?
-->

<main>
  <div class="text-3xl w-svw text-center mb-4">App Controls</div>
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
        onclick={() => startContext()}>Start New Context</button
      >
    </div>
  </div>
</main>
