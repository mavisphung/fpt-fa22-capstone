import { EventInput } from '@fullcalendar/react';

let eventGuid = 0;
let todayStr = new Date().toISOString().replace(/T.*$/, ''); // YYYY-MM-DD of today
export const createEventId = () => String(eventGuid++);
export const INITIAL_EVENTS: EventInput[] = [
  {
    id: createEventId(),
    title: 'Huy Phùng',
    start: todayStr + 'T12:12:00',
  },
  {
    id: createEventId(),
    title: 'Hoàng Phong',
    start: todayStr + 'T36:30:00',
  },
];
