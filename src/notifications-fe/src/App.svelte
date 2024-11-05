<script lang="ts">
  import { onMount } from "svelte";
  import type { StatusResponse } from "./lib/types";
  import { API_BASE } from "./lib/types";
  import "./app.css";
  import Notifications from "./lib/Notifications.svelte";
  
  console.log("Hello from Svelte");
  console.log('API Base URL:', API_BASE);

  let loading: boolean = false;
  let statusData: StatusResponse | null = null;
  let statusMessage: string = "";

  onMount(async () => {
    try {
      const response = await fetch(`${API_BASE}/`);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Error fetching initial data:", error);
    }
  });

  const getStatus = async () => {
    loading = true;
    try {
      const response = await fetch(`${API_BASE}/status`);
      statusData = await response.json();
    } catch (error) {
      console.error("Error fetching status:", error);
    } finally {
      loading = false;
    }
  };

  const postStatus = async () => {
    loading = true;
    try {
      const response = await fetch(`${API_BASE}/status`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: statusMessage }),
      });
      statusData = await response.json();
    } catch (error) {
      console.error("Error posting status:", error);
    } finally {
      loading = false;
      statusMessage = "";
    }
  };
</script>

<main class="flex w-full h-full items-center justify-center p-3">
  <section class="h-full w-4/5 flex items-center justify-center flex-col font-roboto rounded-lg border-2 border-black p-1">
    <h1 class="text-2xl mb-4 font-medium">Notifications App</h1>
    
    <div class="flex flex-col border-2 border-black border-dashed items-center p-2 mb-3 w-full md:w-1/2">
      <p>Actions you can take</p>
      <div class="flex flex-col md:flex-row my-4 w-full gap-1">
        <button 
          class="p-4 bg-yellow-300 rounded transition duration-150 hover:bg-yellow-400 disabled:opacity-50 flex-1" 
          on:click={getStatus}
          disabled={loading}
          type="button"
        >
          {loading ? 'Loading...' : 'Get Status'}
        </button>
        <div class="flex flex-col gap-2 flex-1">
          <button
            class="p-4 bg-blue-300 rounded hover:bg-blue-400 transition duration-150 disabled:opacity-50 flex items-center justify-center flex-col gap-2"
            on:click={postStatus}
            disabled={loading}
            type="button"
          >
            {#if loading}
              Loading...
            {:else}
              Post Status
            {/if}
          
          </button>
          <input class="p-1 rounded bg-blue-300 text-black placeholder:text-black" type="text" placeholder="Enter a status message" bind:value={statusMessage}>
        </div>
      </div>
    </div>

    {#if statusData}
      <div class="mt-4 p-4 bg-green-100 rounded mb-4">
        <pre>{JSON.stringify(statusData, null, 2)}</pre>
      </div>
    {/if}

    <Notifications />
  </section>
</main>