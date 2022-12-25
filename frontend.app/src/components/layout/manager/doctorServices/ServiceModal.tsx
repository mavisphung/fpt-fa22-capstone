import { ServiceCategory } from 'constants/Enum';
import { urlApi } from 'constants/UrlApi';
import Multiselect from 'multiselect-react-dropdown';
import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import classes from './ServiceModal.module.scss';

export const ServiceModal: React.FC<any> = (props) => {
  const [selectedType, setSelectedType] = useState(['Trực tuyến']);

  const nameServiceRef = React.useRef<HTMLInputElement>(null);
  const descriptionRef = React.useRef<HTMLInputElement>(null);
  const priceRef = React.useRef<HTMLInputElement>(null);
  const handleAddService = (event: any) => {
    event.preventDefault();

    const currentToken = localStorage.getItem('access_token');

    var myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');
    myHeaders.append('Authorization', 'Bearer ' + currentToken);

    var raw = JSON.stringify({
      name: nameServiceRef.current?.value,
      description: descriptionRef.current?.value,
      price: priceRef.current?.value,
      category: ServiceCategory.get(selectedType[0]),
    });

    var requestOptions: RequestInit = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow',
    };

    fetch(urlApi + 'manager/service/', requestOptions)
      .then((response) => {
        if (response.status === 201) {
          return response.json();
        } else {
          props.onHide();
          props.showNotificationToast(false, 'Không thành công', 'Vui lòng thử lại!');
        }
      })
      .then((result) => {
        props.onCloseModal(result.data);
        props.showNotificationToast(true, 'Thành công', 'Thêm dịch vụ thành công!');
      })
      .catch((error) => console.log('error', error));
  };
  return (
    <Modal
      show={props.show}
      onHide={props.onHide}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">{props.titleString}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className={classes.bodyPrescriptionModal}>
          <form onSubmit={handleAddService}>
            <table>
              <tbody>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Tên dịch vụ</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="text"
                      placeholder="Vui lòng nhập tên dịch vụ"
                      required
                      ref={nameServiceRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Mô tả chi tiết</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="text"
                      placeholder="Vui lòng mô tả chi tiết dịch vụ"
                      required
                      ref={descriptionRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Giá (vnđ)</span>
                  </td>
                  <td>
                    <input
                      className={classes.inputDiv}
                      type="number"
                      placeholder="Vui lòng nhập giá dịch vụ"
                      required
                      ref={priceRef}
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <span className={classes.titleLabel}>Hình thức khám</span>
                  </td>
                  <td>
                    <Multiselect
                      isObject={false}
                      onKeyPressFn={function noRefCheck() {}}
                      onRemove={setSelectedType}
                      onSearch={function noRefCheck() {}}
                      onSelect={setSelectedType}
                      options={Array.from(ServiceCategory.keys())}
                      placeholder="Chọn hình thức khám"
                      singleSelect={true}
                      selectedValues={selectedType}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
            <div className={classes.buttonSubmit}>
              <button className={classes.btnSave}>Lưu</button>
            </div>
          </form>
        </div>
      </Modal.Body>
    </Modal>
  );
};
