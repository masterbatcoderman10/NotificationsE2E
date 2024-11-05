export const API_BASE: string = import.meta.env["VITE_API_URL"];
export const WS_BASE: string = import.meta.env["VITE_WS_URL"];

export interface StatusResponse {
    status: string;
    timestamp?: string;
    message?: string;
  }

export interface Notification {
    id: number;
    message: string;
    time_since: string;

}

export interface NotificationsResponse {
    unread: Notification[];
    read: Notification[];

}