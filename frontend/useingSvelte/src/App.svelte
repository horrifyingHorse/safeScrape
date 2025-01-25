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

<!-- <main class="flex w-svw h-svh p-4"> -->
<main class="flex w-svw h-svh">
  <div class="h-full w-[65%] bg-[#3d405b] p-2">
    <div class="text-center text-3xl text-[#f4f1de]">ControlPanel</div>
  </div>

  <div class="h-full w-[35%] bg-[#171717]">
    <Console />
  </div>
</main>
