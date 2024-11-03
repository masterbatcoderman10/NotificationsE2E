<script lang="ts">
  import { onMount } from "svelte";
  import "./app.css";
  
  interface StatusResponse {
    status: string;
    timestamp?: string;
    message?: string;
  }

  const API_BASE: string = import.meta.env["VITE_API_URL"];
  console.log("Hello from Svelte");
  console.log('API Base URL:', API_BASE);

  let loading: boolean = false;
  let statusData: StatusResponse | null = null;

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
        body: JSON.stringify({ status: "Hello from Svelte" }),
      });
      statusData = await response.json();
    } catch (error) {
      console.error("Error posting status:", error);
    } finally {
      loading = false;
    }
  };
</script>

<main class="flex w-full h-full items-center justify-center p-3">
  <section class="h-full w-4/5 flex items-center justify-center flex-col font-roboto rounded-lg border-2 border-black">
    <h1 class="text-2xl mb-4 font-medium">Notifications App</h1>
    
    <div class="flex flex-col border-2 border-black border-dashed items-center p-2 mb-3">
      <p>Actions you can take</p>
      <div class="flex gap-10 my-4">
        <button 
          class="p-4 bg-yellow-300 rounded transition duration-150 hover:bg-yellow-400 disabled:opacity-50" 
          on:click={getStatus}
          disabled={loading}
          type="button"
        >
          {loading ? 'Loading...' : 'Get Status'}
        </button>
        <button 
          class="p-4 bg-blue-300 rounded hover:bg-blue-400 transition duration-150 disabled:opacity-50" 
          on:click={postStatus}
          disabled={loading}
          type="button"
        >
          {loading ? 'Loading...' : 'Post Status'}
        </button>
      </div>
    </div>

    {#if statusData}
      <div class="mt-4 p-4 bg-green-100 rounded">
        <pre>{JSON.stringify(statusData, null, 2)}</pre>
      </div>
    {/if}
  </section>
</main>