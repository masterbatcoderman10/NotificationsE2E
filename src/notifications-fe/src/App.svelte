<script>
  import { onMount } from "svelte";
  import "./app.css";

  onMount(async () => {
    const response = await fetch("http://localhost:3000/");
    
    if (response.ok) {
      const data = await response.json();
      console.log(data);
    } else {
      console.error("Failed to fetch notifications");
    }
  });
</script>

<main class="">
  <h1>Notifications Test</h1>
</main>