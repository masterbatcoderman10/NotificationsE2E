<script>
  import { onMount } from "svelte";
  import "./app.css";
  import { get } from "svelte/store";

  onMount(async () => {
    try {
      const response = await fetch("http://localhost:3000/");
      
      if (response.ok) {
        const data = await response.json();
        console.log(data);
      } else {
        console.error("Failed to fetch notifications");
      }
    } catch (error) {
      console.error("An error occurred while fetching notifications:", error);
    }
  });

  const getStatus = async () => {
    try {
      const response = await fetch("http://localhost:3000/status");
      
      if (response.ok) {
        const data = await response.json();
        console.log(data);
      } else {
        console.error("Failed to fetch status");
      }
    } catch (error) {
      console.error("An error occurred while fetching status:", error);
    }
  };

  const postStatus = async () => {
    try {
      const response = await fetch("http://localhost:3000/status", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: "Hello from Svelte" }),
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(data);
      } else {
        console.error("Failed to post status");
      }
    } catch (error) {
      console.error("An error occurred while posting status:", error);
    }
  };
</script>

<main class="flex w-full h-full items-center justify-center p-3">
  <section class="h-full w-4/5 flex items-center justify-center flex-col font-roboto rounded-lg border-2 border-black">
    <h1 class="text-2xl mb-4 font-medium">Notifications App</h1>
    <div class="flex flex-col border-2 border-black border-dashed items-center p-2 mb-3 ">
      <p>Actions you can take</p>
      <div class="flex gap-10 my-4">
      <button class="p-4 bg-yellow-300 rounded transition duration-150 hover:bg-yellow-400" on:click|preventDefault={getStatus}>Get Status</button>
      <button class="p-4 bg-blue-300 rounded hover:bg-blue-400 transition duration-150" on:click|preventDefault={postStatus}>Post Status</button>
      </div>
    </div>
  </section>
</main>