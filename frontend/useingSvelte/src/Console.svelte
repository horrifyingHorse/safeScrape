<script lang="ts">
  import { onMount } from "svelte";
  import { logDisplay } from "./lib/store.svelte";

  let selectedConsole: number = $state(0);

  onMount(() => {
    logDisplay.init("console-log");
    logDisplay.log("Console Initialised");
  });
</script>

<div
  class="flex text-center gap-x-4 pb-2 border border-b-[#39ff14] border-transparent"
>
  <button
    class={selectedConsole == 0 ? "italic px-4 w-12" : "px-4 w-12"}
    onclick={() => (selectedConsole = 0)}>logs</button
  >
  <button
    class={selectedConsole == 1 ? "italic px-4 w-12" : "px-4 w-12"}
    onclick={() => (selectedConsole = 1)}>data</button
  >
  <button
    class={selectedConsole == 2 ? "italic px-4 w-12" : "px-4 w-12"}
    onclick={() => (selectedConsole = 2)}>terminal</button
  >
</div>

<div class="overflow-hidden h-full">
  <div
    id="console-log"
    class={`font-mono overflow-hidden h-full overflow-y-auto ${selectedConsole == 0 ? "block" : "hidden"}`}
  ></div>
  <div
    id="console-data"
    class={`overflow-hidden h-full ${selectedConsole == 1 ? "block" : "hidden"}`}
  ></div>
  <div
    id="console-terminal"
    class={`font-mono overflow-hidden overflow-y-auto h-full ${selectedConsole == 2 ? "block" : "hidden"}`}
  ></div>
</div>
