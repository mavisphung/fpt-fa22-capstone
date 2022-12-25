import { ServiceType } from 'constants/Enum';
import { urlApi } from 'constants/UrlApi';
import { DoctorService } from 'models/doctorService';
import { DoctorSpecialist } from 'models/specialists';
import Multiselect from 'multiselect-react-dropdown';
import React, { useState } from 'react';
import { Tab, Tabs } from 'react-bootstrap';
import { IonIcon } from 'react-ion-icon';
import './ServicePackages.scss';

const ServicePackages: React.FC<any> = (servicesProps) => {
  const [currentServices, setServicesArr] = useState(
    servicesProps.servicesProp.length !== 0
      ? servicesProps.servicesProp
      : [{ id: undefined, name: undefined, description: '', price: 0 }]
  );
  const [selectedType, setSelectedType] = useState([]);
  console.log(selectedType);
  const typeArr = ['Trực tuyến', 'Đến nhà bệnh nhân', 'Tại nhà bác sĩ'];

  const [key, setKey] = React.useState(0);
  const handleAddServices = (e: any) => {
    e.preventDefault();
    setServicesArr([
      ...currentServices,
      { id: undefined, name: undefined, description: '', price: 0 },
    ]);
    setKey(currentServices.length);
  };
  const handleServices = (event: any) => {
    event.preventDefault();
    let newServices = new Array<DoctorService>();

    currentServices.map((service: DoctorService) => {
      if (service.id === undefined) {
        newServices.push(service);
      }
    });
  };
  const handleRemoveService = (idSevice: number, indexService: number) => {
    let services = [...currentServices];

    if (idSevice !== undefined) {
      const currentToken = localStorage.getItem('access_token');
      const idDoctor = localStorage.getItem('id_data');

      var jsonHeaders = new Headers();
      jsonHeaders.append('Content-Type', 'application/json');
      jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

      var requestOptions: RequestInit = {
        method: 'DELETE',
        headers: jsonHeaders,
        redirect: 'follow',
      };

      fetch(urlApi + 'doctor/' + idDoctor + '/packages/' + idSevice + '/', requestOptions)
        .then((response) => {
          if (response.status === 200) {
            return response.json();
          } else {
            return response.json().then(() => {
              alert('Bạn không thể xóa dịch vụ này!');
            });
          }
        })
        .then((result) => {
          services.splice(indexService, 1);
          setServicesArr(services);
          setKey(0);
        })
        .catch((error) => console.log('error', error));
    } else {
      services.splice(indexService, 1);
      setServicesArr(services);
      setKey(indexService - 1);
    }
  };
  return (
    <section className="backgroundBody">
      <div className="container">
        <div className="cardHeader">
          <div className="title">Dịch vụ cung cấp</div>
          <a className="cardHeader_btn" onClick={handleAddServices}>
            <IonIcon color="secondary" name="add-outline"></IonIcon> Thêm dịch vụ
          </a>
        </div>

        <form onSubmit={handleServices}>
          <Tabs
            activeKey={key}
            onSelect={(k: any) => setKey(k)}
            id="justify-tab-example"
            className="mb-3"
          >
            {currentServices.map((service: any, index: any) => (
              <Tab
                eventKey={index}
                title={service.name ?? 'Gói mới'}
                key={index}
                unmountOnExit={true}
              >
                <div className="userDetails">
                  {/* <div className="inputBox">
                    <span className="titleLabel">Mã dịch vụ</span>
                    <input
                      className="inputDiv"
                      type="text"
                      defaultValue={service.id}
                      required
                      readOnly
                    />
                  </div> */}
                  <div className="inputBox">
                    <span className="titleLabel">Tên dịch vụ</span>
                    <input
                      className="inputDiv"
                      type="text"
                      placeholder="Vui lòng nhập tên dịch vụ"
                      defaultValue={service.name}
                      required
                    />
                  </div>
                  {/* <div className="inputBox">
                    <span className="titleLabel">Giá (vnđ)</span>
                    <input
                      className="inputDiv"
                      type="text"
                      placeholder="Vui lòng nhập giá dịch vụ"
                      required
                      defaultValue={service.price}
                    />
                  </div> */}
                  <div className="inputBox">
                    <span className="titleLabel">Mô tả chi tiết</span>
                    <input
                      className="inputDiv"
                      type="text"
                      placeholder="Vui lòng mô tả chi tiết dịch vụ"
                      required
                      defaultValue={service.description}
                    />
                  </div>
                  {/* <div className="inputBox">
                    <span className="titleLabel">Thuộc chuyên khoa</span>
                    <Multiselect
                      isObject={false}
                      onKeyPressFn={function noRefCheck() {}}
                      onRemove={function noRefCheck() {}}
                      onSearch={function noRefCheck() {}}
                      onSelect={function noRefCheck() {}}
                      options={servicesProps.specialistsProp.map(
                        (spec: DoctorSpecialist) => spec.name
                      )}
                      selectedValues={[]}
                      placeholder="Chọn chuyên khoa"
                      selectionLimit={1}
                      singleSelect={true}
                    />
                  </div> */}
                  <div className="inputBox">
                    <span className="titleLabel">Hình thức khám</span>
                    <Multiselect
                      isObject={false}
                      onKeyPressFn={function noRefCheck() {}}
                      onRemove={setSelectedType}
                      onSearch={function noRefCheck() {}}
                      onSelect={setSelectedType}
                      options={typeArr}
                      placeholder="Chọn hình thức"
                      singleSelect={true}
                      selectedValues={
                        null
                        // (service.category === ServiceType.ONLINE && ['Trực tuyến']) ||
                        // (service.category === ServiceType.AT_PATIENT_HOME && [
                        //   'Đến nhà bệnh nhân',
                        // ]) ||
                        // (service.category === ServiceType.AT_DOCTOR_HOME && ['Tại nhà bác sĩ'])
                      }
                    />
                  </div>
                </div>
                <div className="buttonSubmit">
                  {currentServices.length > 1 && (
                    <div
                      className="btnDelete"
                      onClick={() => handleRemoveService(service.id, index)}
                    >
                      Xóa
                    </div>
                  )}
                  <button className="btnSave">Lưu</button>
                </div>
              </Tab>
            ))}
          </Tabs>
        </form>
      </div>
    </section>
  );
};

export default ServicePackages;
