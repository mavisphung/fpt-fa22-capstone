import React from 'react';
import { urlApi } from 'constants/UrlApi';
import { Spinner } from 'react-bootstrap';
import { DoctorSpecialist } from 'models/specialists';
import Delayed from 'components/common/Delay';

const RegisterPage = React.lazy(() => import('./RegisterPage'));

export const GetSpecialists: React.FC<any> = (props) => {
  const initSpecialistsArray = new Array<DoctorSpecialist>();
  const [specialistsArray, setSpecialistsProp] = React.useState(initSpecialistsArray);

  React.useEffect(() => {
    var requestOption: RequestInit = {
      method: 'GET',
      redirect: 'follow',
    };
    fetch(urlApi + 'specialists/?page=1&limit=10', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          setSpecialistsProp(initSpecialistsArray);
        }
      })
      .then((result) => {
        setSpecialistsProp(result.data);
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
      <Delayed>
        <RegisterPage
          specialistsProp={specialistsArray}
          showNotificationProp={props.showNotificationToast}
        />
      </Delayed>
    </React.Suspense>
  );
};
