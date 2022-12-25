import React from 'react';
import { urlApi } from 'constants/UrlApi';
import { Spinner } from 'react-bootstrap';
import Delayed from 'components/common/Delay';
import { DetailAppointmentData } from 'models/detailAppointment';
import { NotificationObj } from 'models/notificationObj';

const Dashboard = React.lazy(() => import('./Dashboard'));

export const InitDashboard: React.FC<any> = (props) => {
  const initAppointmentArray = new Array<DetailAppointmentData>();
  const [appointmentArray, setAppointmentProp] = React.useState(initAppointmentArray);
  const initNotificationArray = new Array<NotificationObj>();
  const [notificationArray, setNotificationProp] = React.useState(initNotificationArray);

  React.useEffect(() => {
    const currentToken = localStorage.getItem('access_token');

    var jsonHeaders = new Headers();
    jsonHeaders.append('Content-Type', 'application/json');
    jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

    var requestOption: RequestInit = {
      method: 'GET',
      headers: jsonHeaders,
      redirect: 'follow',
    };
    fetch(urlApi + 'appointments/doctor/pending/?page=1&limit=5', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          setAppointmentProp(initAppointmentArray);
        }
      })
      .then((result) => {
        setAppointmentProp(result.data);
      })
      .catch((error) => console.log('error', error));

    fetch(urlApi + 'user/me/notifications/', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          setNotificationProp(initNotificationArray);
        }
      })
      .then((result) => {
        setNotificationProp(result.data);
      })
      .catch((error) => console.log('error', error));
  }, []);

  return (
    <React.Suspense
      fallback={
        <>
          <Spinner variant="primary" animation={'border'} />
          <h2 color="primary">Vui lòng đợi trong giây lát...</h2>
        </>
      }
    >
      <>
        <Delayed>
          <Dashboard appointmentProp={appointmentArray} notificationProp={notificationArray} />
        </Delayed>
      </>
    </React.Suspense>
  );
};
