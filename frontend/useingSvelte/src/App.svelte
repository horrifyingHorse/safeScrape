<script lang="ts">
  import AppControls from "./AppControls.svelte";
  import PageControls from "./PageControls.svelte";
  import Console from "./Console.svelte";
  import { pgInstances } from "./lib/store.svelte";
  import { onMount } from "svelte";

  let paddingItem: string = "";

  onMount(() => {
    function updateFontVariations() {
      const elements = document.getElementsByClassName("sixtyfour-normal");
      Array.from(elements).forEach((element) => {
        const bled = Math.random() * 100;
        const scan = Math.random() * (50 - -50) + -20;
        (element as HTMLDivElement).style.fontVariationSettings =
          `"BLED" ${bled.toFixed(1)}, "SCAN" ${scan.toFixed(1)}`;
      });
    }

    function staticGen() {
      const el = document.getElementById("StaticNoise");
      if (!el) return;
      const listItem = Math.round(Math.random())
        ? `pl-${Math.floor(Math.random() * 51)}`
        : `pr-${Math.floor(Math.random() * 51)}`;
      if (paddingItem === "") {
        el.classList.add("sixtyfour-normal", `${listItem}`);
      } else {
        el.classList.replace(paddingItem, listItem);
      }
      paddingItem = listItem;
    }

    const interval = setInterval(updateFontVariations, 1500);
    const intervalNoise = setInterval(staticGen, 1500);
    return () => {
      clearInterval(intervalNoise);
      clearInterval(interval);
    };
  });

  // var ws = new WebSocket("ws://localhost:8000/foo");
  // ws.onmessage = function (event) {
  //   console.log(event.data);
  // };
  // function sendMessage(event: Event | undefined) {
  //   var input = document.getElementById("messageText") as HTMLInputElement;
  //   ws.send(input.value);
  //   input.value = "";
  //   event?.preventDefault();
  // }
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

<main class="flex flex-col justify-center gap-2 w-svw h-svh">
  <div class="h-1/4">
    <div
      class="flex z-0 justify-center py-4 text-3xl w-svw text-center mb-4 select-none"
    >
      <div class="flex absolute text-[#39ff14] z-0">
        <div class="sixtyfour-normal">App Controls</div>
      </div>
      <div
        class="flex relative transition-all z-10 text-[#86ff70] hover:text-[#a9ff99] blur-sm"
      >
        <div id="StaticNoise" class="sixtyfour-normal">App Controls</div>
      </div>
    </div>

    <AppControls />
  </div>

  <!-- <form action="" onsubmit={() => sendMessage(event)}> -->
  <!--   <input type="text" id="messageText" autocomplete="off" /> -->
  <!--   <button>Send</button> -->
  <!-- </form> -->

  <div class="flex w-svw h-3/4 pt-4 overflow-hidden">
    <div class="w-1/2">
      {#if pgInstances.instanceCount() != 0}
        <PageControls />
      {/if}
    </div>

    <div
      class="flex flex-col w-1/2 p-2 bg-[#000000] border-[#39ff14] border rounded-lg"
    >
      <Console />
    </div>
  </div>
</main>
