import { useCallback, useState } from 'react';
import FullCalendar, { DateSelectArg, EventApi, EventClickArg } from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import allLocales from '@fullcalendar/core/locales-all';
import interactionPlugin from '@fullcalendar/interaction';
import { INITIAL_EVENTS, createEventId } from './event-utils';
import './ScheduleCalendar.scss';

function ScheduleCalendar() {
  const [currentEvents, setCurrentEvents] = useState<EventApi[]>([]);
  const handleEvents = useCallback((events: EventApi[]) => setCurrentEvents(events), []);
  const handleDateSelect = useCallback((selectInfo: DateSelectArg) => {
    let title = prompt('Vui lòng nhập tiêu đề sự kiện')?.trim();
    let calendarApi = selectInfo.view.calendar;
    calendarApi.unselect();
    if (title) {
      calendarApi.addEvent({
        id: createEventId(),
        title,
        start: selectInfo.startStr,
        end: selectInfo.endStr,
        allDay: selectInfo.allDay,
      });
    }
  }, []);
  const handleEventClick = useCallback((clickInfo: EventClickArg) => {
    if (window.confirm(`Bạn có muốn xóa sự kiện 「${clickInfo.event.title}」 không?`)) {
      clickInfo.event.remove();
    }
  }, []);
  return (
    <div className="demo-app">
      <div className="demo-app-main">
        <FullCalendar
          plugins={[dayGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          selectable={true}
          editable={true}
          initialEvents={INITIAL_EVENTS}
          locales={allLocales}
          locale="vie"
          eventsSet={handleEvents}
          select={handleDateSelect}
          eventClick={handleEventClick}
        />
      </div>
    </div>
  );
}

export default ScheduleCalendar;
