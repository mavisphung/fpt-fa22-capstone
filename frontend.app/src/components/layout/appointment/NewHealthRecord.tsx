import { timeOutSeconds } from 'constants/ConstValue';
import { urlApi } from 'constants/UrlApi';
import { Diseases } from 'models/diseases';
import { Prescription } from 'models/prescription';
import moment from 'moment';
import Multiselect from 'multiselect-react-dropdown';
import React from 'react';
import { IonIcon } from 'react-ion-icon';
import classes from './NewHealthRecord.module.scss';
import { PrescriptionModal } from './PrescriptionModal';

const NewHealthRecord: React.FC<any> = (props) => {
  const [showPrescription, setShowPrescription] = React.useState(false);
  const initPrescriptionArray = new Array<Prescription>();
  const [prescriptionArr, setPrescriptionArr] = React.useState(initPrescriptionArray);
  let prescriptionArray = [...prescriptionArr];
  const fromDateRef = React.useRef<HTMLInputElement>(null);
  const toDateRef = React.useRef<HTMLInputElement>(null);

  const initSelectedDisease = new Array<Diseases>();
  const [disease, setSelectedDisease] = React.useState(initSelectedDisease);
  let diseaseArray = [...disease];

  const inputNoteRef = React.useRef<HTMLInputElement>(null);

  function handleCloseModal(returnedData: any) {
    setPrescriptionArr([...prescriptionArr, returnedData]);
    setShowPrescription(false);
  }

  const handleRemovePrescription = (indexPrescription: number) => {
    prescriptionArray.splice(indexPrescription, 1);
    setPrescriptionArr(prescriptionArray);
  };

  const handleCreateHealthRecord = (event: any) => {
    event.preventDefault();
    let enteredNote = inputNoteRef.current?.value;
    const fromDateValue = fromDateRef.current?.value;
    const toDateValue = toDateRef.current?.value;

    if (enteredNote === '') {
      enteredNote = 'Không có lưu ý.';
    }

    if (disease.length === 0) {
      props.checkinProps.showNotificationToast(
        false,
        'Lưu không thành công',
        'Vui lòng chuẩn đoán bệnh!'
      );
    } else if (
      fromDateValue === '' ||
      fromDateValue === undefined ||
      toDateValue === '' ||
      toDateValue === undefined
    ) {
      props.checkinProps.showNotificationToast(
        false,
        'Lưu không thành công',
        'Vui lòng thiết lập thời gian cho đơn thuốc!'
      );
    } else if (
      moment(fromDateValue, 'YYYY-MM-DD').unix() < moment().unix() ||
      moment(fromDateValue, 'YYYY-MM-DD').unix() > moment(toDateValue, 'YYYY-MM-DD').unix()
    ) {
      props.checkinProps.showNotificationToast(
        false,
        'Lưu không thành công',
        'Vui lòng chọn thời gian đơn thuốc phù hợp!'
      );
    } else {
      const currentToken = localStorage.getItem('access_token');
      var myHeaders = new Headers();
      myHeaders.append('Content-Type', 'application/json');
      myHeaders.append('Authorization', 'Bearer ' + currentToken);

      let diseaseIdArr = new Array<number>();
      diseaseArray.map((diseaseObj: Diseases) => diseaseIdArr.push(Number(diseaseObj.id)));

      let prescriptionBody = new Array<object>();
      prescriptionArray.map((prescription: Prescription) =>
        prescriptionBody.push({
          medicine: prescription.id,
          quantity: prescription.quantity,
          unit: prescription.unit,
          guide: prescription.guide,
        })
      );

      // var raw = JSON.stringify({
      //   patient: props.checkinProps.detailAppointmentProps?.patient.id,
      //   detail: {
      //     idAppointment: props.checkinProps.idAppointment,
      //     diagnose: disease,
      //     note: enteredNote ?? 'Không có lưu ý.',
      //     prescription: prescriptionArray,
      //   },
      // });

      // var raw = JSON.stringify({
      //   patient: props.checkinProps.detailAppointmentProps?.patient.id,
      //   detail: {
      //     allergies: [],
      //     socialHistory: [],
      //     pathologies: [],
      //     diseases: disease,
      //   },
      //   prescriptions: [
      //     {
      //       doctor: localStorage.getItem('id_data'),
      //       detail: prescriptionBody,
      //       note: enteredNote ?? 'Không có lưu ý.',
      //     },
      //   ],
      // });

      var raw = JSON.stringify({
        patient: props.checkinProps.detailAppointmentProps?.patient.id,
        doctor: localStorage.getItem('id_data'),
        detail: {
          allergies: [],
          socialHistory: [],
          pathologies: [],
          diseases: diseaseIdArr,
          prescriptions: [
            {
              detail: prescriptionBody,
              note: enteredNote,
              fromDate: fromDateValue,
              toDate: toDateValue,
            },
          ],
          instructions: [],
        },
      });

      var requestOptions: RequestInit = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow',
      };

      fetch(urlApi + 'doctor/health-records/', requestOptions)
        .then((response) => {
          if (response.status === 201) {
            props.checkinProps.showNotificationToast(
              true,
              'Thành công',
              'Đã lưu sổ sức khỏe thành công!'
            );
            return response.json();
          } else {
            props.checkinProps.showNotificationToast(
              false,
              'Không thành công',
              'Vui lòng thử lại!'
            );
          }
        })
        .then((result) => {
          var checkoutRaw = JSON.stringify({
            healthRecord: result.data.record.id,
            receiver: result.data.supervisor.email,
          });
          requestOptions.method = 'PUT';
          requestOptions.body = checkoutRaw;

          fetch(
            urlApi + 'appointments/doctor/' + props.checkinProps.idAppointment + '/checkout/',
            requestOptions
          ).then(() =>
            setTimeout(() => {
              window.location.reload();
            }, timeOutSeconds - 1000)
          );
        })
        .catch((error) => console.log('error', error));
    }
  };

  return (
    <>
      <div className={classes.detail_area}>
        <div className={classes.healthRecords}>
          <div className={classes.record}>
            <div className={classes.childRecord}>
              <span className={classes.titleRecord}>Chẩn đoán</span>
              <Multiselect
                isObject={true}
                onKeyPressFn={function noRefCheck() {}}
                onRemove={setSelectedDisease}
                onSearch={(value: string) => props.checkinProps.getDiseasesFunction(value)}
                onSelect={setSelectedDisease}
                // options={props.checkinProps.diseasesProps.map(
                //   (disease: Diseases) => disease.code + ' - ' + disease.diseaseName
                // )}
                options={props.checkinProps.diseasesProps}
                displayValue="diseaseName"
                selectedValues={null}
                placeholder="Chọn loại bệnh"
                selectionLimit={3}
              />
            </div>

            <div className={classes.childRecord}>
              <span className={classes.titleNote}>Dặn dò</span>
              <input
                className={classes.inputDiv}
                type="text"
                placeholder="Dặn dò hoặc lưu ý dành cho bệnh nhân"
                ref={inputNoteRef}
              />
            </div>
          </div>
          <div className={classes.prescriptionArea}>
            <div className={classes.headerPrescription}>
              <h3>Đơn Thuốc</h3>
              <button
                className={classes.addPrescriptionButton}
                onClick={() => setShowPrescription(true)}
              >
                <IonIcon name="add-outline"></IonIcon> Thêm thuốc
              </button>
            </div>
            <table>
              <thead>
                <tr>
                  <th>STT</th>
                  <th>Tên thuốc</th>
                  <th>Số lượng</th>
                  <th>Cách dùng</th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {prescriptionArr.length === 0 ? (
                  <tr>
                    <td></td>
                    <td>Đơn thuốc chưa có thuốc.</td>
                    <td></td>
                    <td></td>
                  </tr>
                ) : (
                  prescriptionArr.map((prescription: Prescription, index: number) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{prescription?.name}</td>
                      <td>
                        {prescription?.quantity} {prescription?.unit}
                      </td>
                      <td>{prescription?.guide}</td>

                      <td>
                        <button
                          className={classes.deletePrescriptionButton}
                          onClick={() => handleRemovePrescription(index)}
                        >
                          Xoá
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          <div className={classes.record}>
            <div className={classes.childRecord}>
              <span className={classes.titleRecord}>Ngày bắt đầu dùng thuốc</span>
              <input className={classes.inputDateDiv} type="date" required ref={fromDateRef} />
            </div>
            <div className={classes.childRecord}>
              <span className={classes.titleRecord}>Ngày kết thúc đơn thuốc</span>
              <input className={classes.inputDateDiv} type="date" required ref={toDateRef} />
            </div>
          </div>
          <div className={classes.buttonSubmit} onClick={handleCreateHealthRecord}>
            <button className={classes.btnSave}>
              <IonIcon name="checkmark-circle-outline"></IonIcon>
              <span>Lưu và kết thúc</span>
            </button>
          </div>
        </div>
      </div>

      <PrescriptionModal
        show={showPrescription}
        onHide={() => setShowPrescription(false)}
        titleString="Thêm thuốc vào đơn thuốc"
        dialogClassName={classes.customPrescriptionModal}
        medicinesProps={props.checkinProps.medicinesProps}
        searchMedicinesFunction={props.checkinProps.getMedicinesFunction}
        onCloseModal={handleCloseModal}
      />
    </>
  );
};

export default NewHealthRecord;
