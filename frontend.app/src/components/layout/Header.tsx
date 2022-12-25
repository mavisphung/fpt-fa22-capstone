import React from 'react';
import classes from './Header.module.scss';
import { useSelector } from 'react-redux';
import { selectCurrentUser } from 'features/auth/authSlice';
import { useHistory } from 'react-router-dom';

export const Header: React.FC = () => {
  const currentUser = useSelector(selectCurrentUser);
  const fullName = currentUser?.lastName + ' ' + currentUser?.firstName;

  const history = useHistory();

  const navigatePage = (linkProps: string) => {
    history.push(linkProps);
  };

  return (
    <div className={classes.header}>
      <div className={classes.welcomeString}>
        <span>Chào mừng </span>
        <span className={classes.fullname}>bác sĩ {fullName}</span>
      </div>
      <div className={classes.imgUser} onClick={() => navigatePage('/doctor/settingAccount')}>
        <img src={currentUser?.avatar} alt="avatar" />
      </div>
    </div>
  );
};
