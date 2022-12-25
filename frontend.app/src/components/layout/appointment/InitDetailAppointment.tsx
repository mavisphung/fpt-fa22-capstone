import React from 'react';
import { urlApi } from 'constants/UrlApi';
import { Spinner } from 'react-bootstrap';
import { DetailAppointmentData } from 'models/detailAppointment';
import { Diseases } from 'models/diseases';
import Delayed from 'components/common/Delay';
// import { Instruction } from 'models/instruction';
import { Medicines } from 'models/medicines';

const DetailAppointment = React.lazy(() => import('./DetailAppointment'));

export const InitDetailAppointment: React.FC<any> = (props) => {
  const idAppointment = localStorage.getItem('selectedAppointment');
  const initDetailObj: DetailAppointmentData = {
    id: undefined,
    beginAt: undefined,
    bookedAt: undefined,
    booker: undefined,
    checkInCode: undefined,
    endAt: undefined,
    package: undefined,
    patient: undefined,
    status: undefined,
    type: undefined,
    cancelReason: undefined,
  };
  const [detailObj, setDetailAppointment] = React.useState(initDetailObj);

  const initDiseasesArray = new Array<Diseases>();
  const [diseasesArray, setDiseasesProp] = React.useState(initDiseasesArray);

  // const initInstructionArray = new Array<Instruction>();
  // const [instructionArray, setInstructionProp] = React.useState(initInstructionArray);

  const initMedicinesArray = new Array<Medicines>();
  const [medicinesArray, setMedicinesProp] = React.useState(initMedicinesArray);
  const currentToken = localStorage.getItem('access_token');
  var jsonHeaders = new Headers();
  jsonHeaders.append('Content-Type', 'application/json');
  jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

  var requestOption: RequestInit = {
    method: 'GET',
    headers: jsonHeaders,
    redirect: 'follow',
  };

  const getDiseases = (searchDiseasesString: string) => {
    fetch(urlApi + 'diseases/?page=1&limit=50&keyword=' + searchDiseasesString, requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          return response.json().then((data) => {
            alert('Not found diseases');
          });
        }
      })
      .then((result) => {
        setDiseasesProp(result.data);
      })
      .catch((error) => console.log('error', error));
  };

  const getMedicines = (searchMedicinesString: string) => {
    fetch(urlApi + 'medicines/?page=1&limit=50&keyword=' + searchMedicinesString, requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          return response.json().then((data) => {
            alert('Not found medicines');
          });
        }
      })
      .then((result) => {
        setMedicinesProp(result.data);
      })
      .catch((error) => console.log('error', error));
  };

  React.useEffect(() => {
    fetch(urlApi + 'appointments/' + idAppointment + '/', requestOption)
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        } else {
          alert('Not found the appointment');
        }
      })
      .then((result) => {
        setDetailAppointment(result.data);
      })
      .catch((error) => console.log('error', error));

    getDiseases('');

    getMedicines('');

    // fetch(urlApi + 'instructions-categories/?page=1&limit=10', requestOption)
    //   .then((response) => {
    //     if (response.status === 200) {
    //       return response.json();
    //     } else {
    //       return response.json().then((data) => {
    //         alert('Not found instruction');
    //       });
    //     }
    //   })
    //   .then((result) => {
    //     setInstructionProp(result.data);
    //   })
    //   .catch((error) => console.log('error', error));
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
      {detailObj.patient?.avatar !== undefined && (
        <Delayed>
          <DetailAppointment
            detailAppointmentProps={detailObj}
            diseasesProps={diseasesArray}
            getDiseasesFunction={getDiseases}
            // instructionsProps={instructionArray}
            medicinesProps={medicinesArray}
            getMedicinesFunction={getMedicines}
            idAppointment={idAppointment}
            showNotificationToast={props.showNotificationToast}
          />
        </Delayed>
      )}
    </React.Suspense>
  );
};
