import React, { useState } from 'react';
import { urlApi } from 'constants/UrlApi';
import { Spinner } from 'react-bootstrap';
import { DoctorService } from 'models/doctorService';
import Delayed from 'components/common/Delay';
import { pageSizeNumber, timeOutSeconds } from 'constants/ConstValue';
import { ServiceModal } from './ServiceModal';

const ServicesTable = React.lazy(() => import('../../../common/MyTable'));

export const InitServices: React.FC<any> = (props) => {
  const initServicesArray = new Array<DoctorService>();
  const [servicesArray, setServicesProp] = useState(initServicesArray);
  const [totalServicesNumber, setTotalServicesProp] = useState(0);
  const [currentPageNumber, setCurrentPage] = useState(1);
  const [totalAssignedServices, setTotalAssignedServicesProp] = useState(0);
  const [currentAssignedPageNumber, setCurrentAssignedPage] = useState(1);
  const initServicesDoctorArray = new Array<number>();
  const [servicesDoctorArray, setServicesDoctorProp] = useState(initServicesDoctorArray);
  const initCurrentServicesDoctorArray = new Array<number>();
  const [currentServicesDoctorArray, setCurrentServicesDoctorProp] = useState(
    initCurrentServicesDoctorArray
  );
  const initAssignedServices = new Array<Object>();
  const [assignedServicesArray, setAssignedServicesProp] = useState(initAssignedServices);

  const [showServiceModal, setShowServiceModal] = React.useState(false);

  const tableHead = {
    name: 'Tên dịch vụ',
    description: 'Mô tả chi tiết',
    category: 'Hình thức',
    price: 'Giá dịch vụ (vnđ)',
  };

  const currentToken = localStorage.getItem('access_token');
  const idDoctor = localStorage.getItem('selected_account');
  var jsonHeaders = new Headers();
  jsonHeaders.append('Content-Type', 'application/json');
  jsonHeaders.append('Authorization', 'Bearer ' + currentToken);
  var requestOption: RequestInit = {
    method: 'GET',
    headers: jsonHeaders,
    redirect: 'follow',
  };

  const openAddServiceModal = (event: any) => {
    event.preventDefault();
    setShowServiceModal(true);
  };

  const handleAddService = (returnedData: any) => {
    setServicesProp([...servicesArray, returnedData]);
    let totalServices = totalServicesNumber + 1;
    setTotalServicesProp(totalServices);
    setShowServiceModal(false);
  };

  const addServiceForDoctor = (returnedIdService: number, inputedString: any) => {
    var raw = JSON.stringify({
      services: [returnedIdService],
    });
    requestOption.method = 'POST';
    requestOption.body = raw;

    fetch(urlApi + 'doctor/' + idDoctor + '/services/', requestOption)
      .then((response) => {
        if (response.status === 201) {
          props.showNotificationToast(true, 'Thành công', 'Đã chỉ định dịch vụ!');
          fetchServices(currentPageNumber, pageSizeNumber, inputedString);
        } else {
          props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  const changeActivateService = (returnedIdService: number, inputedString: any) => {
    requestOption.method = 'DELETE';
    requestOption.body = undefined;
    fetch(urlApi + 'doctor/' + idDoctor + '/services/' + returnedIdService + '/', requestOption)
      .then((response) => {
        if (response.status === 204) {
          props.showNotificationToast(true, 'Thành công', 'Đã thay đổi lựa chọn!');
          fetchServicesDoctor(currentAssignedPageNumber, pageSizeNumber, inputedString);
        } else {
          props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  const fetchServices = (pageNumber: number, limitNumber: number, inputedString: any) => {
    requestOption.method = 'GET';
    requestOption.body = undefined;
    fetch(
      urlApi +
        'api/service/search/?page=' +
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
          setServicesProp(initServicesArray);
        }
      })
      .then((result) => {
        setServicesProp(result.data);
        setTotalServicesProp(result.totalItems);
        setCurrentPage(pageNumber);
      })
      .catch((error) => console.log('error', error));
    if (props.typeComponent !== 'servicesManager') {
      fetchServicesDoctor(1, 50, '');
    }
  };

  const fetchServicesDoctor = (pageNumber: number, limitNumber: number, inputedString: any) => {
    requestOption.method = 'GET';
    requestOption.body = undefined;
    fetch(
      urlApi +
        'doctor/' +
        idDoctor +
        '/services/?page=' +
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
          setServicesDoctorProp(initServicesDoctorArray);
        }
      })
      .then((result) => {
        let currentServicesArray = new Array<number>();
        let activeServicesArray = new Array<number>();
        let assignedServicesDoctor = new Array<Object>();
        result.data.map((dataObject: any) => {
          assignedServicesDoctor.push(dataObject.service);
          currentServicesArray.push(dataObject.service.id);
          if (dataObject.isActive) {
            activeServicesArray.push(dataObject.service.id);
          }
        });
        setAssignedServicesProp(assignedServicesDoctor);
        setCurrentServicesDoctorProp(currentServicesArray);
        setServicesDoctorProp(activeServicesArray);
        setTotalAssignedServicesProp(result.totalItems);
        setCurrentAssignedPage(result.currentPage);
      })
      .catch((error) => console.log('error', error));
  };

  React.useEffect(() => {
    if (props.typeComponent === 'servicesDoctor') {
      fetchServicesDoctor(1, pageSizeNumber, '');
    } else {
      fetchServices(1, pageSizeNumber, '');
    }
  }, []);

  const deleteService = (idService: number) => {
    requestOption.method = 'DELETE';
    requestOption.body = undefined;
    fetch(urlApi + 'manager/service/' + idService + '/', requestOption)
      .then((response) => {
        if (response.status === 204) {
          props.showNotificationToast(true, 'Thành công', 'Xóa dịch vụ thành công!');
          fetchServices(1, pageSizeNumber, '');
        } else {
          props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  const unassignService = (returnedIdService: number, inputedString: any) => {
    requestOption.method = 'DELETE';
    requestOption.body = undefined;
    fetch(
      urlApi + '/manager/doctor/' + idDoctor + '/services/' + returnedIdService + '/',
      requestOption
    )
      .then((response) => {
        if (response.status === 204) {
          props.showNotificationToast(true, 'Thành công', 'Bỏ chỉ định dịch vụ!');
          fetchServicesDoctor(currentPageNumber, pageSizeNumber, inputedString);
        } else {
          props.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
        }
      })
      .catch((error) => console.log('error', error));
  };

  return (
    <>
      <React.Suspense
        fallback={
          <>
            <Spinner variant="primary" animation={'border'} />
            <h2 color="primary">Vui lòng đợi trong giây lát...</h2>
          </>
        }
      >
        <>
          {props.typeComponent === 'servicesDoctor' ? (
            <Delayed>
              <ServicesTable
                theadProp={tableHead}
                dataProp={assignedServicesArray}
                totalItemsProp={totalAssignedServices}
                showNotificationToast={props.showNotificationToast}
                getDataFuntion={fetchServicesDoctor}
                currentPageNumber={currentAssignedPageNumber}
                addFunction={openAddServiceModal}
                deleteFunction={deleteService}
                addString="dịch vụ"
                headerString="Dịch vụ của bác sĩ"
                searchPlaceHolder="Tìm theo tên dịch vụ"
                dataListType={props.typeComponent}
                currentServicesDoctor={currentServicesDoctorArray}
                activeServicesArray={servicesDoctorArray}
                changeActivateServiceFuntion={changeActivateService}
                addServiceForDoctorFunction={addServiceForDoctor}
              />
            </Delayed>
          ) : (
            <Delayed>
              <ServicesTable
                theadProp={tableHead}
                dataProp={servicesArray}
                totalItemsProp={totalServicesNumber}
                showNotificationToast={props.showNotificationToast}
                getDataFuntion={fetchServices}
                currentPageNumber={currentPageNumber}
                addFunction={openAddServiceModal}
                deleteFunction={deleteService}
                addString="dịch vụ"
                headerString="Danh sách dịch vụ"
                searchPlaceHolder="Tìm theo tên dịch vụ"
                dataListType={props.typeComponent}
                currentServicesDoctor={currentServicesDoctorArray}
                activeServicesArray={servicesDoctorArray}
                changeActivateServiceFuntion={changeActivateService}
                addServiceForDoctorFunction={addServiceForDoctor}
                unassignServiceFunction={unassignService}
              />
            </Delayed>
          )}
        </>
      </React.Suspense>
      <ServiceModal
        show={showServiceModal}
        onHide={() => setShowServiceModal(false)}
        titleString="Thêm dịch vụ"
        onCloseModal={handleAddService}
        showNotificationToast={props.showNotificationToast}
      />
    </>
  );
};
