<script lang="ts">
  import AppControls from "./AppControls.svelte";
  import PageControls from "./PageControls.svelte";
  import { pgInstances } from "./lib/store.svelte";
  import type { PageState } from "./lib/store.svelte";
</script>

<!--
Features:
  [+] Launch new page (in a new Context) of the headful playwright
      (+) Select state (cookies, auth)
      (+) URL to start context with
      (+) Auto Log in?
      + (+) Kill Browser
  => AppControls


-->

<main>
  <div class="text-3xl w-svw text-center mb-4">App Controls</div>
  <AppControls />
  <!-- <button -->
  <!--   onclick={() => { -->
  <!--     const ps: PageState = { -->
  <!--       auto_login: !pgState.pageState[0].auto_login, -->
  <!--       storage_state: "", -->
  <!--       service: "autoGyatt", -->
  <!--       custom_url: "sigmaRizz.ohio", -->
  <!--       scrape: true, -->
  <!--       allow_delay: false, -->
  <!--       execute: false, -->
  <!--     }; -->
  <!--     const id: number = Math.round(Math.random() * 10); -->
  <!--     const doc = document.getElementById("PageControlsDisplay"); -->
  <!--     if (doc != null) doc.style.display = "block"; -->
  <!---->
  <!--     pgState.update(id, ps); -->
  <!--   }}>Click to Rune</button -->
  <!-- > -->

  {#if pgInstances.instanceCount() != 0}
    <PageControls />
  {/if}
</main>
