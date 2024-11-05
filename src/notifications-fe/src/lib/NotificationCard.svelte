<script lang='ts'>
    import type { Notification } from "./types";
    import { API_BASE } from "./types";
    import { createEventDispatcher } from "svelte";

    export let nofitication: Notification;
    export let isUnread: boolean = true;
    const dispatcher = createEventDispatcher();

    const handleRead = async () => {
        try {
            const response = await fetch(`${API_BASE}/notifications/${nofitication.id}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            if (response.ok) {
                console.log("Notification read successfully");
                dispatcher("read", nofitication.id);
            } else {
                console.error("Error reading notification");
            }
        } catch (error) {
            console.error("Error reading notification:", error);
        }
    }
</script>

<div class=" p-2 bg-orange-200 flex items-center justify-between">
    <!-- info -->
     <div class="flex flex-col gap-0.5">
        <p >{nofitication.message}</p>
        <span class=" font-light text-gray-800 text-sm">{nofitication.time_since}</span>
     </div>

    <!-- actions -->
    {#if isUnread}
        <button class="p-1 bg-red-500 text-white rounded" on:click={handleRead}>
            Read
        </button>
    {/if}
</div>