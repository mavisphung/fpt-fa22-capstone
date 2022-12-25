import React from 'react';
import { urlApi } from 'constants/UrlApi';
import { ShiftTimes } from 'models/shiftTime';
import { Spinner } from 'react-bootstrap';
import Delayed from 'components/common/Delay';

const WorkingTimes = React.lazy(() => import('./WorkingTimes'));

export const InitShiftsTime: React.FC<any> = (props) => {
  const initShiftsTimeMap = new Map<string, ShiftTimes>(
    Object.entries({
      '1': [
        { id: undefined, weekday: 1, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '2': [
        { id: undefined, weekday: 2, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '3': [
        { id: undefined, weekday: 3, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '4': [
        { id: undefined, weekday: 4, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '5': [
        { id: undefined, weekday: 5, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '6': [
        { id: undefined, weekday: 6, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
      '7': [
        { id: undefined, weekday: 7, startTime: '18:00:00', endTime: '20:30:00', isActive: false },
      ],
    })
  );
  const [shiftsTimeMap, setShiftsTimeProp] = React.useState(initShiftsTimeMap);
  const currentToken = localStorage.getItem('access_token');
  var jsonHeaders = new Headers();
  jsonHeaders.append('Content-Type', 'application/json');
  jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

  var requestOption: RequestInit = {
    method: 'GET',
    headers: jsonHeaders,
    redirect: 'follow',
  };

  React.useEffect(() => {
    fetch(urlApi + 'doctor/shifts/', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          return response.json().then(() => {
            props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
          });
        }
      })
      .then((result) => {
        const mapObj = new Map<string, ShiftTimes>(Object.entries(result.data));
        setShiftsTimeProp(mapObj);
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
          <WorkingTimes
            shiftsTimeProp={shiftsTimeMap}
            showNotificationToast={props.showNotificationToast}
          />
        </Delayed>
      </>
    </React.Suspense>
  );
};
