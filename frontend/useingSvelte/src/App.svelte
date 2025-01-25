<script lang="ts">
  import AppControls from "./AppControls.svelte";
  import PageControls from "./PageControls.svelte";
  import Console from "./Console.svelte";
  import { pgInstances, selectedConsole } from "./lib/store.svelte";
  import { onMount } from "svelte";

  let activeModi: boolean = false;

  onMount(() => {
    document.addEventListener("keydown", (event) => {
      if (activeModi && event.key >= "1" && event.key <= "9") {
        const index = parseInt(event.key, 10);
        if (index < 1 || index > 3) return;
        $selectedConsole = index - 1;
      }

      activeModi = false;
      if (event.altKey && event.key.toLowerCase() == "a") {
        activeModi = true;
        console.log("Active Modi");
      }
    });
  });
</script>

<!--
Features:
  [+] Launch new page (in a new Context) of the headful playwright
      (+) Select state (cookies, auth)
      (+) URL to start context with
      (+) Auto Log in?
      + (+) Kill Browser
      + (+) Create New State
  => AppControls

  [ ] Console area
      ( ) logs
      ( ) data display
      (?) terminal?
-->

<!-- <main class="flex w-svw h-svh p-4"> -->
<main class="flex w-svw h-svh text-[#f4f1de]">
  <div
    class="h-full w-[65%] bg-[#3d405b] p-2 flex-col justify-center items-center"
  >
    <div class="text-center text-3xl text-[#f4f1de]">ControlPanel</div>

    <div class="flex justify-center">
      <AppControls />
    </div>

    {#if pgInstances.instanceCount() != 0}
      <div class="flex justify-center">
        <PageControls />
      </div>
    {/if}
  </div>

  <div class="h-full w-[35%] bg-[#171717]">
    <Console />
  </div>
</main>
