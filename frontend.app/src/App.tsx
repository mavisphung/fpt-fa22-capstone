import { Switch, Route } from 'react-router-dom';
import { NotFound, DoctorRoute, ManagerRoute } from 'components/common';
import { HomePage } from 'components/layout/pages/HomePage';
import LoginPage from 'features/auth/pages/LoginPage';
import { InitProfile } from 'components/layout/acount/InitProfile';
import { InitShiftsTime } from 'components/layout/workingTimes/InitShiftsTime';
import { VideoPage } from 'features/video_message/video';
import { InitDetailAppointment } from 'components/layout/appointment/InitDetailAppointment';
import { InitServices } from 'components/layout/manager/doctorServices/InitServices';
// import ScheduleCalendar from 'components/layout/schedule/ScheduleCalendar';
import { InitDashboard } from 'components/layout/dashboard/InitDashboard';
import { MessageList } from 'features/communication/chat_section';
import { DoctorChatContainer } from 'features/communication/chat_layout';
import { Schedule } from 'features/manager/layout/schedule_layout';
import { InitDoctorsList } from 'components/layout/manager/doctorAccounts/InitDoctorsList';
import { GetSpecialists } from 'features/auth/pages/GetSpecialists';
import { Appointments } from 'components/layout/dashboard/appointment/Appointments';
import './utils/firebase';
import { useEffect, useState } from 'react';
import { getMyToken, onMessageListener, requestPermission } from './utils/firebase';
import { NotificationToast } from 'components/layout/NotificationToast';
import notificationIcon from './assets/images/notification_logo.png';
import { ContractPage } from 'features/contract/component/page';
import { AppointmentChatRoom, InitChatBox } from 'features/communication/appointment_chatRoom';
import { ContractInfo, ContractInfoWrapper } from 'features/contract/component/contractInfo';
import {
  InitPrescriptionReadonly,
  MedicalInstructionDetailModal,
  PrescriptionCreatorprescription,
  PrescriptionDetailModal,
} from 'features/contract/component/modal';

function App() {
  const typeLoggedIn = localStorage.getItem('type');
  const [showToast, setShowToast] = useState(false);
  const [notification, setNotification] = useState({ icon: '', title: '', body: '' });

  function showNotification(title: string, body: string) {
    setShowToast(true);

    setNotification({
      icon: notificationIcon,
      title: title,
      body: body,
    });
  }

  useEffect(() => {
    requestPermission();
    // getMyToken();
  }, []);

  onMessageListener()
    .then((payload: any) => {
      // console.log(payload);
      showNotification(payload.notification.title, payload.notification.body);
    })
    .catch((err) => console.log('failed: ', err));

  return (
    <>
      <NotificationToast
        show={showToast}
        onClose={() => setShowToast(false)}
        content={notification}
      />
      <Switch>
        <Route path="/login">
          <LoginPage />
        </Route>
        <DoctorRoute path="/" exact>
          {typeLoggedIn === 'DOCTOR' ? (
            <HomePage>
              <InitDashboard />
            </HomePage>
          ) : (
            <HomePage>
              <InitDoctorsList />
            </HomePage>
          )}
        </DoctorRoute>
        <DoctorRoute path="/doctor/home" exact>
          <HomePage>
            <InitDashboard />
          </HomePage>
        </DoctorRoute>

        <DoctorRoute path="/doctor/settingAccount">
          <HomePage>
            <InitProfile />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/appointments">
          <HomePage>
            <Appointments />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/workingTimes">
          <HomePage>
            <InitShiftsTime />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/services">
          <HomePage>
            <InitServices typeComponent="servicesDoctor" />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/detailAppointment">
          <HomePage>
            <InitDetailAppointment />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/video" exact>
          <VideoPage></VideoPage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/schedule">
          <HomePage>
            <Schedule />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/chat">
          <HomePage>
            <DoctorChatContainer doctorId={5} />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/appointment/chat/:id">
          <HomePage>
            {/* <DoctorChatContainer doctorId={5}></DoctorChatContainer> */}
            <InitChatBox id={180}></InitChatBox>
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/contracts">
          <HomePage>
            <ContractPage />
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/test">
          <HomePage></HomePage>
        </DoctorRoute>
        <ManagerRoute path="/manager/home">
          <HomePage>
            <InitDoctorsList />
          </HomePage>
        </ManagerRoute>
        <DoctorRoute path="/doctor/prescription">
          <HomePage>
            {/* <PrescriptionCreatorprescription/> */}
            <InitPrescriptionReadonly></InitPrescriptionReadonly>
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/contract/detail">
          <HomePage>
            {/* <PrescriptionCreatorprescription/> */}
            <ContractInfoWrapper></ContractInfoWrapper>
          </HomePage>
        </DoctorRoute>
        <DoctorRoute path="/doctor/contract/instruction">
          <HomePage>{/* <MedicalInstructionDetailModal/> */}</HomePage>
        </DoctorRoute>
        <ManagerRoute path="/manager/register">
          <HomePage>
            <GetSpecialists />
          </HomePage>
        </ManagerRoute>
        <ManagerRoute path="/manager/services">
          <HomePage>
            <InitServices typeComponent="servicesManager" />
          </HomePage>
        </ManagerRoute>
        <ManagerRoute path="/manager/assignServices">
          <HomePage>
            <InitServices typeComponent="assignServices" />
          </HomePage>
        </ManagerRoute>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  );
}

export default App;
