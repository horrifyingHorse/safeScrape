<script lang="ts">
  import { onMount } from "svelte";
  import { logDisplay } from "./lib/store.svelte";
  import ConsoleTab from "./ConsoleTab.svelte";

  onMount(() => {
    logDisplay.init("console-log");
    logDisplay.log("Console Initialised");
  });
</script>

<div class="w-full h-[4%] min-h-[28px] font-mono">
  <div id="tab" class="flex">
    <div class="bg-[#282c34] p-1 px-4 z-10 flex items-center">
      <img src="ri-terminal-box-line.svg" alt="term" />
    </div>
    <ConsoleTab type="button" name="logs" idx={0} />
    <ConsoleTab type="button" name="data" idx={1} />
    <ConsoleTab type="button" name="terminal" idx={2} />
  </div>
</div>

<div class="overflow-hidden h-[96%] p-2">
  <ConsoleTab type="display" name="console-log" idx={0} />
  <ConsoleTab type="display" name="console-date" idx={1} />
  <ConsoleTab type="display" name="console-terminal" idx={2} />
</div>
