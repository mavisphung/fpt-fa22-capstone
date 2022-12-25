import { timeOutSeconds } from 'constants/ConstValue';
import { AppointmentStatus, AppointmentStatusMap, ServiceType } from 'constants/Enum';
import { requestOption } from 'constants/HeadersRequest';
import { urlApi } from 'constants/UrlApi';
import { InitChatBox } from 'features/communication/appointment_chatRoom';
import moment from 'moment';
import React from 'react';

import { IonIcon } from 'react-ion-icon';
import { CancelModal } from './CancelModal';

import classes from './DetailAppointment.module.scss';
import NewHealthRecord from './NewHealthRecord';

import { QRModal } from './QRModal';

const DetailAppointment: React.FC<any> = (props) => {
  const [showQR, setShowQR] = React.useState(false);
  const [checkin, setCheckin] = React.useState(0);
  const [showReasonCancel, setShowReasonCancel] = React.useState(false);

  const currentToken = localStorage.getItem('access_token');
  var myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');
  myHeaders.append('Authorization', 'Bearer ' + currentToken);

  const continueAppointment = (event: any) => {
    event.preventDefault();
    setCheckin(1);
    // if (props.detailAppointmentProps?.category === AppointmentType.ONLINE) {
    //   setCheckin(1);
    // } else {
    //   setCheckin(2);
    // }
  };

  const joinRoom = (event: any) => {
    event.preventDefault();
    window.open(window.location.origin + '/doctor/video', 'Appointment ', 'height=800,width=850');
  };

  const onCancelAppointment = (reasonString: string) => {
    var raw = JSON.stringify({
      cancelReason: reasonString,
    });
    console.log(raw);
    requestOption.method = 'PUT';
    requestOption.headers = myHeaders;
    requestOption.body = raw;

    fetch(urlApi + 'appointments/' + props.detailAppointmentProps?.id + '/cancel/', requestOption)
      .then((response) => {
        if (response.status === 202) {
          setShowReasonCancel(false);
          props.showNotificationToast(true, 'Thành công', 'Đã hủy cuộc hẹn!');
          setTimeout(() => {
            window.location.reload();
          }, timeOutSeconds - 1000);
        } else {
          setShowReasonCancel(false);
          props.showNotificationToast(false, 'Không thành công', 'Chưa hủy cuộc hẹn!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  const continueCheckin = (event: any) => {
    event.preventDefault();
    if (
      moment().unix() < moment(props.detailAppointmentProps?.bookedAt, 'YYYY/MM/DD HH:mm:ss').unix()
    ) {
      props.showNotificationToast(false, 'Chưa đến giờ hẹn', 'Vui lòng quay lại sau!');
    } else {
      var raw = JSON.stringify({
        doctor: props.detailAppointmentProps?.doctor.id,
        patient: props.detailAppointmentProps?.patient.id,
        service: props.detailAppointmentProps?.package.id,
        action: 'checkin',
        checkInCode: props.detailAppointmentProps?.checkInCode,
      });

      requestOption.method = 'PUT';
      requestOption.headers = myHeaders;
      requestOption.body = raw;

      fetch(
        urlApi + 'appointments/doctor/' + props.detailAppointmentProps?.id + '/checkin/',
        requestOption
      )
        .then(() => {
          setCheckin(1);
        })
        .catch((error) => console.log('error', error));
    }
  };

  return (
    <>
      {checkin === 0 && (
        <div className={classes.details}>
          <div className={classes.backgroundBody}>
            <div className={classes.avatarDoctor}>
              <img src={props.detailAppointmentProps.patient.avatar} alt="avatarPatient" />
              <div className={classes.userDetails}>
                <div className={classes.inputBox}>
                  <span className={classes.nameLabel}>
                    {props.detailAppointmentProps?.patient.lastName}{' '}
                    {props.detailAppointmentProps?.patient.firstName}
                  </span>
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Ngày sinh</span>
                  <span className={classes.infoSpan}>
                    {moment(props.detailAppointmentProps?.patient.dob, 'YYYY/MM/DD').format(
                      'DD/MM/YYYY'
                    )}
                  </span>
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Địa chỉ</span>
                  <span className={classes.infoSpan}>
                    {props.detailAppointmentProps?.patient.address}
                  </span>
                </div>
              </div>
            </div>
            <div className={classes.detail_container}>
              <div className={classes.userDetails}>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Người giám hộ</span>
                  <span className={classes.infoSpan}>
                    {props.detailAppointmentProps?.booker.firstName}{' '}
                    {props.detailAppointmentProps?.booker.lastName}
                  </span>
                </div>
                <div title={props.detailAppointmentProps?.address} className={classes.inputBox}>
                  <span className={classes.titleLabel}>Ngày hẹn</span>
                  <span className={classes.infoSpan}>
                    {moment(props.detailAppointmentProps?.bookedAt, 'YYYY/MM/DD HH:mm:ss').format(
                      'HH:mm:ss DD/MM/YYYY'
                    )}
                  </span>
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Dịch vụ đã chọn</span>
                  <span className={classes.infoSpan}>
                    {props.detailAppointmentProps.package.name ?? 'Chưa xác định'}
                  </span>
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Triệu chứng của bệnh nhân</span>
                  <span className={classes.infoSpan}>
                    {props.detailAppointmentProps.diseaseDescription ?? 'Chưa xác định'}
                  </span>
                </div>
                {/* <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Dị ứng</span>
                  <span className={classes.infoSpan}>Không có</span>
                </div> */}

                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Hình thức</span>
                  <span className={classes.infoSpan}>
                    {ServiceType.get(props.detailAppointmentProps?.category)}
                  </span>
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Trạng thái</span>
                  <span className={classes.infoSpan}>
                    {AppointmentStatusMap.get(props.detailAppointmentProps?.status)}
                  </span>
                </div>
                {props.detailAppointmentProps?.status === AppointmentStatus.CANCELLED && (
                  <div className={classes.inputBox}>
                    <span className={classes.titleLabel}>Lý do hủy</span>
                    <span className={classes.infoSpan}>
                      {props.detailAppointmentProps?.cancelReason ?? 'Có việc đột xuất'}
                    </span>
                  </div>
                )}
              </div>
              <div className={classes.statusDiv}>
                {props.detailAppointmentProps?.status === AppointmentStatus.PENDING && (
                  <>
                    <button
                      className={classes.cancelButton}
                      onClick={() => setShowReasonCancel(true)}
                    >
                      <IonIcon color="light" name="close-circle-outline"></IonIcon>
                      <span>Hủy cuộc hẹn</span>
                    </button>
                    <button className={classes.checkinButton} onClick={continueCheckin}>
                      <IonIcon color="light" name="caret-forward-circle-outline"></IonIcon>
                      <span>Bắt đầu khám</span>
                    </button>
                  </>
                )}

                {props.detailAppointmentProps?.status === AppointmentStatus.IN_PROGRESS && (
                  <div>
                    {/* <button
                      className={classes.cancelButton}
                      onClick={() => setShowReasonCancel(true)}
                    >
                      <IonIcon color="danger" name="close-circle-outline"></IonIcon>
                      <span>Hủy cuộc hẹn</span>
                    </button> */}
                    {/* <button className={classes.rescheduleButton}>Dời lịch</button> */}
                    <button className={classes.continueButton} onClick={continueAppointment}>
                      <span>Tiếp tục khám</span>
                      <IonIcon color="info" name="chevron-forward-circle-outline"></IonIcon>
                    </button>
                  </div>
                )}
              </div>
            </div>
            {/* <div className={classes.file_area}>
              <div className={classes.cardHeader}>
                <h3>Tương tác với bệnh nhân</h3>
              </div>
              <table>
                <tbody>
                  <tr className={classes.file_tr}>
                    <td>
                      <IonIcon name="document-outline"></IonIcon>
                    </td>
                    <td>Tài liệu xét nghiệm</td>
                  </tr>
                </tbody>
              </table>
            </div> */}
          </div>
        </div>
      )}
      {checkin === 1 && (
        <InitChatBox
          id={props.detailAppointmentProps?.id}
          openVideoCallWindow={joinRoom}
          navigateNewHealthRecord={() => setCheckin(2)}
        />
      )}
      {checkin === 2 && <NewHealthRecord checkinProps={props} />}

      <QRModal
        show={showQR}
        onHide={() => setShowQR(false)}
        titleString="Vui lòng quét mã QR này để bắt đầu"
        dialogClassName={classes.sizeQRModal}
        actionProp={continueCheckin}
      />
      <CancelModal
        show={showReasonCancel}
        onHide={() => setShowReasonCancel(false)}
        titleString="Lý do hủy cuộc hẹn"
        dialogClassName={classes.sizeQRModal}
        onCloseModal={onCancelAppointment}
      />
    </>
  );
};

export default DetailAppointment;
