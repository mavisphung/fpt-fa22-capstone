import React from 'react';
import { urlApi } from 'constants/UrlApi';
// import { Profile } from './Profile';
import { User } from 'models/user';
import { Spinner } from 'react-bootstrap';
import Delayed from 'components/common/Delay';

const Profile = React.lazy(() => import('./Profile'));

export const InitProfile: React.FC<any> = (props) => {
  // const currentUser = store.getState().auth.currentUser;
  // const currentUser = useSelector(selectCurrentUser);

  const initProfileObj: User = {
    firstName: '',
    lastName: '',
    phoneNumber: '',
    address: '',
    gender: '',
  };

  const [profileObj, setProfileProps] = React.useState(initProfileObj);

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
    fetch(urlApi + 'user/me/', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          return response.json().then((data) => {
            alert('Not found id doctor');
          });
        }
      })
      .then((result) =>
        setProfileProps({
          firstName: result.data.firstName,
          lastName: result.data.lastName,
          phoneNumber: result.data.phoneNumber,
          address: result.data.address,
          gender: result.data.gender,
        })
      )
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
        {profileObj.gender !== '' && (
          <Delayed>
            <Profile
              profileProps={profileObj}
              showNotificationToast={props.showNotificationToast}
            />
          </Delayed>
        )}
      </>
    </React.Suspense>
  );
};
