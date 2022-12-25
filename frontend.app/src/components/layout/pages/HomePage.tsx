import React from 'react';
import { Navigation } from 'components/layout/Navigation';
import classes from './HomePage.module.scss';
import { Header } from '../Header';
import { NotificationToast } from '../NotificationToast';
import errorIcon from '../../../assets/images/error_icon.png';
import successIcon from '../../../assets/images/success_icon.png';
import { IonIcon } from 'react-ion-icon';
import notificationIcon from '../../../assets/images/notification_logo.png';

interface liListObj {
  iconName: React.ComponentProps<typeof IonIcon>['name'] | undefined;
  iconActive: React.ComponentProps<typeof IonIcon>['name'] | undefined;
  navProps: string;
  liText: string;
}

interface liListArr extends Array<liListObj> {}

export const HomePage = (props: any) => {
  const [showToast, setShowToast] = React.useState(false);
  const [notification, setNotification] = React.useState({ icon: '', title: '', body: '' });
  const typeLoggedIn = localStorage.getItem('type');

  const liDoctor: liListArr = [
    { iconName: 'home-outline', iconActive: 'home', navProps: '/doctor/home', liText: 'Trang chủ' },
    {
      iconName: 'calendar-outline',
      iconActive: 'calendar',
      navProps: '/doctor/appointments',
      liText: 'Lịch hẹn khám',
    },
    {
      iconName: 'fitness-outline',
      iconActive: 'fitness',
      navProps: '/doctor/contracts',
      liText: 'Hợp đồng theo dõi',
    },
    // {
    //   iconName: 'chatbubble-ellipses-outline',
    //   iconActive: 'chatbubble-ellipses',
    //   navProps: '/doctor/chat',
    //   liText: 'Tin nhắn với bệnh nhân',
    // },
    {
      iconName: 'time-outline',
      iconActive: 'time',
      navProps: '/doctor/workingTimes',
      liText: 'Ca làm việc',
    },
    {
      iconName: 'bag-add-outline',
      iconActive: 'bag-add',
      navProps: '/doctor/services',
      liText: 'Dịch vụ của bác sĩ',
    },
    {
      iconName: 'settings-outline',
      iconActive: 'settings',
      navProps: '/doctor/settingAccount',
      liText: 'Cài đặt tài khoản',
    },
  ];

  const liManager: liListArr = [
    {
      iconName: 'home-outline',
      iconActive: 'home',
      navProps: '/manager/home',
      liText: 'Trang chủ',
    },
    {
      iconName: 'bag-add-outline',
      iconActive: 'bag-add',
      navProps: '/manager/services',
      liText: 'Dịch vụ',
    },
  ];

  function showNotification(success: any, title: string, body: string) {
    setShowToast(true);
    if (success === true) {
      setNotification({
        icon: successIcon,
        title: title,
        body: body,
      });
    } else if (success === false) {
      setNotification({
        icon: errorIcon,
        title: title,
        body: body,
      });
    } else {
      setNotification({
        icon: notificationIcon,
        title: title,
        body: body,
      });
    }
  }

  return (
    <React.Fragment>
      <Navigation liArr={typeLoggedIn === 'DOCTOR' ? liDoctor : liManager} />
      <div className={classes.main}>
        {typeLoggedIn === 'DOCTOR' && <Header />}
        {React.cloneElement(props.children, { showNotificationToast: showNotification })}
      </div>
      <NotificationToast
        show={showToast}
        onClose={() => setShowToast(false)}
        content={notification}
      />
    </React.Fragment>
  );
};
