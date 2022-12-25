import React, { useState } from 'react';
import { urlApi } from 'constants/UrlApi';
import { Spinner } from 'react-bootstrap';
import Delayed from 'components/common/Delay';
// import { InfoUser } from 'models/infoUser';
import { pageSizeNumber } from 'constants/ConstValue';
import { useHistory } from 'react-router-dom';

const DoctorsTable = React.lazy(() => import('../../../common/MyTable'));

export const InitDoctorsList: React.FC<any> = (props) => {
  const history = useHistory();
  const initDoctorsListArray = new Array<Object>();
  const [doctorsListArray, setDoctorsListProp] = useState(initDoctorsListArray);
  const [totalDoctorsNumber, setTotalDoctorsProp] = useState(0);
  const [currentPageNumber, setCurrentPage] = useState(1);
  const tableHead = {
    avatar: '',
    fullName: 'Họ và tên',
    email: 'Email',
    phoneNumber: 'Số điện thoại',
    isApproved: 'Trạng thái',
  };
  const currentToken = localStorage.getItem('access_token');

  var jsonHeaders = new Headers();
  jsonHeaders.append('Content-Type', 'application/json');
  jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

  var requestOption: RequestInit = {
    method: 'GET',
    headers: jsonHeaders,
    redirect: 'follow',
  };

  const handleAddAccount = (event: any) => {
    event.preventDefault();
    history.push('/manager/register');
  };

  const blockDoctorAccount = (idDoctor: number, accountStatus: any, inputedString: any) => {
    requestOption.method = 'PUT';
    requestOption.body = undefined;
    fetch(urlApi + 'manager/doctor/' + idDoctor + '/lock/', requestOption)
      .then((response) => {
        if (response.status === 202) {
          if (accountStatus) {
            props.showNotificationToast(true, 'Thành công', 'Đã khóa tài khoản bác sĩ!');
          } else {
            props.showNotificationToast(true, 'Thành công', 'Mở khóa tài khoản bác sĩ!');
          }
          fetchDoctors(currentPageNumber, pageSizeNumber, inputedString);
        } else {
          props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  const fetchDoctors = (pageNumber: number, limitNumber: number, inputedString: any) => {
    requestOption.method = 'GET';
    requestOption.body = undefined;
    fetch(
      urlApi +
        'api/manager/doctor/search/?page=' +
        pageNumber +
        '&limit=' +
        limitNumber +
        '&q=' +
        inputedString,
      requestOption
    )
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          setDoctorsListProp(initDoctorsListArray);
        }
      })
      .then((result) => {
        setDoctorsListProp(result.data);
        setTotalDoctorsProp(result.totalItems);
        setCurrentPage(pageNumber);
      })
      .catch((error) => console.log('error', error));
  };

  React.useEffect(() => fetchDoctors(1, pageSizeNumber, ''), []);

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
          <DoctorsTable
            theadProp={tableHead}
            dataProp={doctorsListArray}
            totalItemsProp={totalDoctorsNumber}
            showNotificationToast={props.showNotificationToast}
            getDataFuntion={fetchDoctors}
            currentPageNumber={currentPageNumber}
            addFunction={handleAddAccount}
            blockAccFunction={blockDoctorAccount}
            addString="tài khoản"
            headerString="Danh sách tài khoản bác sĩ"
            searchPlaceHolder="Tìm theo tên bác sĩ"
            dataListType="account"
          />
        </Delayed>
      </>
    </React.Suspense>
  );
};
