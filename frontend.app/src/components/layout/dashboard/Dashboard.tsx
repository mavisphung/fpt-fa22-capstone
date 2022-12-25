import { AppointmentType } from 'constants/Enum';
import { NotificationObj } from 'models/notificationObj';
import moment from 'moment';
import React from 'react';
import { IonIcon } from 'react-ion-icon';
import { useHistory } from 'react-router-dom';
import classes from './Dashboard.module.scss';

const Dashboard: React.FC<any> = (dashboardProps) => {
  const history = useHistory();

  const viewDetailAppointment = (idAppointment: number) => {
    localStorage.setItem('selectedAppointment', String(idAppointment));
    history.push('/doctor/detailAppointment');
  };

  return (
    <>
      <div className={classes.cardBox}>
        <div className={classes.cardBox_card}>
          <div className={classes.cardBox_card_iconBx}>
            <IonIcon color="success" name="people"></IonIcon>
          </div>
          <div>
            <div className={classes.numbers}>300</div>
            <div className={classes.cardName}>Bệnh nhân đã được chữa trị</div>
          </div>
        </div>
        <div className={classes.cardBox_card}>
          <div className={classes.cardBox_card_iconBx}>
            <IonIcon color="warning" name="star"></IonIcon>
          </div>
          <div>
            <div className={classes.numbers}>5.0/5.0</div>
            <div className={classes.cardName}>Điểm đánh giá (từ 100 người)</div>
          </div>
        </div>
      </div>
      <div className={classes.details}>
        <div className={classes.details_requests}>
          <div className={classes.cardHeader}>
            <h3>Yêu cầu hẹn khám</h3>
            <a className={classes.cardHeader_btn}>Xem thêm</a>
          </div>
          <table>
            <thead>
              <tr>
                <td></td>
                <td>Tên</td>
                <td>Loại dịch vụ</td>
                <td>Ngày hẹn</td>
                <td>Hình thức khám</td>
              </tr>
            </thead>
            <tbody>
              {dashboardProps.appointmentProp.length > 0 ? (
                dashboardProps.appointmentProp.map((appointment: any, index: any) => (
                  <tr
                    key={index}
                    onClick={(e: any) => {
                      e.preventDefault();
                      viewDetailAppointment(appointment?.id);
                    }}
                  >
                    <td>
                      <div className={classes.imgBx}>
                        <img src={appointment?.patient.avatar} alt="avatarPatient" />
                      </div>
                    </td>
                    <td>
                      {appointment?.patient.firstName} {appointment?.patient.firstName}
                    </td>
                    <td>{appointment?.package.name}</td>
                    <td>
                      {moment(appointment?.bookedAt, 'YYYY/MM/DD HH:mm:ss').format(
                        'HH:mm:ss DD/MM/YYYY'
                      )}
                    </td>
                    <td>
                      {appointment?.type === AppointmentType.OFFLINE ? 'Trực tiếp' : 'Trực tuyến'}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td></td>
                  <td></td>
                  <td>Lịch hẹn của bạn hiện đang trống.</td>
                  <td></td>
                  <td></td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className={classes.details_announcements}>
          <div className={classes.cardHeader}>
            <h3>Thông báo</h3>
          </div>
          <table>
            <tbody className={classes.body_announcements}>
              {dashboardProps.notificationProp.length > 0 ? (
                dashboardProps.notificationProp.map(
                  (notification: NotificationObj, index: number) => (
                    <tr key={index}>
                      <td>
                        <IonIcon name="calendar-outline"></IonIcon>
                      </td>
                      <td>
                        <span>
                          {notification.message} <br />
                        </span>
                        <div className={classes.time_announcement}>
                          {moment(notification.createdAt, 'YYYY/MM/DD HH:mm:ss').format(
                            'HH:mm:ss DD/MM/YYYY'
                          )}
                        </div>
                      </td>
                    </tr>
                  )
                )
              ) : (
                <tr>
                  <td>
                    <div className={classes.imgBx}>
                      <IonIcon name="time-outline"></IonIcon>
                    </div>
                  </td>
                  <td>
                    <span>Hiện chưa có thông báo.</span>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
