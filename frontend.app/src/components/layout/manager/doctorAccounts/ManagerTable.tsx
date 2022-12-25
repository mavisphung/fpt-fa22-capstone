// import { ServiceType } from 'constants/Enum';
import { DoctorService } from 'models/doctorService';
import React from 'react';
import { IonIcon } from 'react-ion-icon';
import { useHistory } from 'react-router-dom';
import classes from './ManagerTable.module.scss';

const ManagerTable: React.FC<any> = (props) => {
  const history = useHistory();

  const handleAddAccount = (event: any) => {
    event.preventDefault();
    history.push('/manager/register');
  };

  const handleAddService = (event: any) => {
    event.preventDefault();
    history.push('/');
  };

  return (
    <>
      <div className={classes.details}>
        {props.isAccount ? (
          <div className={classes.details_requests}>
            <div className={classes.cardHeader}>
              <h3>Danh sách tài khoản bác sĩ</h3>
              <a className={classes.cardHeader_btn} onClick={handleAddAccount}>
                <IonIcon color="secondary" name="add-outline"></IonIcon>Thêm tài khoản
              </a>
            </div>

            <table>
              <thead>
                <tr>
                  <td></td>
                  <td>Họ và Tên</td>
                  <td>Email</td>
                  <td>Số điện thoại</td>
                  <td>Trạng thái</td>
                </tr>
              </thead>
              <tbody>
                {props.doctorsLisProp.length > 0 ? (
                  props.doctorsLisProp.map((appointment: any, index: any) => (
                    <tr
                      key={index}
                      onClick={(e: any) => {
                        e.preventDefault();
                        //   viewDetailAppointment(appointment?.id);
                      }}
                    >
                      <td className={classes.img_td}>
                        <div className={classes.imgBx}>
                          <img src={appointment?.avatar} alt="doctorAvatar" />
                        </div>
                      </td>
                      <td>
                        {appointment?.firstName} {appointment?.lastName}
                      </td>
                      <td>{appointment?.email}</td>
                      <td>{appointment?.phoneNumber}</td>
                      <td>{appointment?.isApproved ? 'Đã kích hoạt' : 'Chưa kích hoạt'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td></td>
                    <td></td>
                    <td>Danh sách trống.</td>
                    <td></td>
                    <td></td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        ) : (
          <div className={classes.details_requests}>
            <div className={classes.cardHeader}>
              <h3>Danh sách dịch vụ</h3>
              <a className={classes.cardHeader_btn} onClick={handleAddService}>
                <IonIcon color="secondary" name="add-outline"></IonIcon>Thêm dịch vụ
              </a>
            </div>

            <table>
              <thead>
                <tr>
                  <td>Tên dịch vụ</td>
                  <td>Mô tả chi tiết</td>
                  <td>Hình thức khám</td>
                  <td>Giá (vnđ)</td>
                  <td>Thao tác</td>
                </tr>
              </thead>
              <tbody>
                {props.servicesProp.length > 0 ? (
                  props.servicesProp.map((service: DoctorService, index: any) => (
                    <tr
                      key={index}
                      onClick={(e: any) => {
                        e.preventDefault();
                        //   viewDetailAppointment(appointment?.id);
                      }}
                    >
                      <td title={service?.name}>{service?.name}</td>
                      <td title={service?.description}>{service?.description}</td>
                      <td>
                        {/* {(service.category === ServiceType.ONLINE && 'Trực tuyến') ||
                          (service.category === ServiceType.AT_PATIENT_HOME &&
                            'Đến nhà bệnh nhân') ||
                          (service.category === ServiceType.AT_DOCTOR_HOME && 'Tại nhà bác sĩ')} */}
                      </td>
                      <td title={String(service?.price)}>{service?.price}</td>
                      <td>
                        <button className={classes.deletePrescriptionButton}>Xoá</button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td></td>
                    <td></td>
                    <td>Danh sách trống.</td>
                    <td></td>
                    <td></td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
};

export default ManagerTable;
