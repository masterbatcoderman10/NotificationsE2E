<script lang="ts">
  import NotificationCard from "./NotificationCard.svelte";
    import { API_BASE, WS_BASE } from "./types";
    import type { Notification, NotificationsResponse } from "./types";
    import { onMount } from "svelte";

    let unreadNotifications: Notification[] = [];
    let readNotifications: Notification[] = [];
    let socket: WebSocket;
    // let message: string;

    onMount(async () => {
        try {
            const response = await fetch(`${API_BASE}/notifications`);
            const data: NotificationsResponse = await response.json();
            unreadNotifications = data.unread;
            readNotifications = data.read;
        } catch (error) {
            console.error("Error fetching notifications:", error);
        }

        try {
            socket = new WebSocket(`${WS_BASE}/ws/1`);
    
            socket.onopen = () => {
            console.log('Connected to server');
            }

            socket.onmessage = (event) => {
            console.log('Message received:', event.data);
            }
        } catch (error) {
            console.error('Error connecting to server:', error);
        }
    });

</script>

<!-- Notifications Section -->
<div class="p-4 flex bg-orange-300 flex-col rounded w-full md:w-1/2">
  <h2 class="text-xl font-medium">Notifications</h2>
  <!-- Unread -->
  <div class="flex flex-col gap-2 mt-2">
    <h3 class="text-lg font-medium">Unread</h3>
    <div class="flex flex-col gap-2">
      {#each unreadNotifications as notification (notification.id)}
        <NotificationCard nofitication={notification} on:read={() => {
            unreadNotifications = unreadNotifications.filter((n) => n.id !== notification.id);
            readNotifications = [...readNotifications, notification];
        }}/>
      {/each}
    </div>
  </div>
  <!-- Read -->
  <div class="flex flex-col gap-2 mt-2">
    <h3 class="text-lg font-medium">Read</h3>
    <div class="flex flex-col gap-2">
      {#each readNotifications as notification (notification.id)}
        <NotificationCard nofitication={notification}  isUnread={false}/>
      {/each}
    </div>
  </div>
</div>
