import {
  faCalendarDays,
  faCheckCircle,
  faClock,
  faClose,
  faHeartPulse,
  faInfoCircle,
  faTimesCircle,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { AppointmentStatus, IAppointment } from 'models/appointment';
import '../style/appointment_summary.scss';

const options: Intl.DateTimeFormatOptions = {
  weekday: 'narrow',
  year: 'numeric',
  month: 'numeric',
  day: 'numeric',
};
const optionsTime: Intl.DateTimeFormatOptions = { hour: '2-digit', minute: '2-digit' };
export const AppointmentSummaryCard = (props: {
  appointment: IAppointment;
  showDetail: (id: number) => void;
}) => {
  let map = new Map<AppointmentStatus, string>([
    [AppointmentStatus.CANCELLED, '--cancelled'],
    [AppointmentStatus.CHECKIN, '--checkin'],
    [AppointmentStatus.COMPLETED, '--completed'],
    [AppointmentStatus.PENDING, '--pending'],
  ]);
  let lang = new Map<AppointmentStatus, string>([
    [AppointmentStatus.CANCELLED, 'Đã Hủy'],
    [AppointmentStatus.CHECKIN, 'Đã Check in'],
    [AppointmentStatus.COMPLETED, 'Hoàn tất'],
    [AppointmentStatus.PENDING, 'Chờ'],
  ]);
  let date: Date = new Date(props.appointment.bookedAt);
  return (
    <div className="appointment_card">
      <div className="appointment_card__wrapper">
        <div className="appointment_card__wrapper__avatar">
          <div className="appointment_card__wrapper__avatar__label">
            <span
              className={`appointment_label appointment_label${map.get(props.appointment.status)}`}
            >
              {lang.get(props.appointment.status)}
            </span>
          </div>
          <img className="appointment_paitent_avatar" src={props.appointment.patient.avatar} />
          <h5>
            {props.appointment.patient.lastName.concat(' ', props.appointment.patient.firstName)}
          </h5>
        </div>
        <div className="appointment_card__wrapper__content">
          <div className="appointment_info">
            <span className="appointment_info__status">
              <FontAwesomeIcon icon={faHeartPulse} size="1x" fixedWidth /> Hình thức:{' '}
              {props.appointment.type}
            </span>
            <span className="appointment_info__date">
              <FontAwesomeIcon icon={faCalendarDays} size="1x" fixedWidth /> Ngày hẹn:{' '}
              {date.toLocaleDateString('vi-VN', options)}
            </span>
            <span className="appointment_info__time">
              <FontAwesomeIcon icon={faClock} size="1x" fixedWidth /> Giờ bắt đầu:{' '}
              {date.toLocaleTimeString('vi-VI', optionsTime)}
            </span>
          </div>
        </div>
        <div className="appointment_action">
          <div
            className="appointment_action__button appointment_action__button--checkin"
            role={'button'}
            onClick={(e) => {
              props.showDetail(props.appointment.id);
            }}
          >
            <span className="appointment_action__button__icon appointment_action__button__icon">
              <FontAwesomeIcon icon={faInfoCircle} size="1x" fixedWidth /> Chi tiết
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
