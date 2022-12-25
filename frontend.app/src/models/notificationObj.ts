export interface NotificationObj {
  id: number | undefined;
  createdAt: string | undefined;
  title: string | undefined;
  isRead: boolean | undefined;
  message: string | undefined;
  payload: string | undefined | null;
  type: string | undefined;
}
