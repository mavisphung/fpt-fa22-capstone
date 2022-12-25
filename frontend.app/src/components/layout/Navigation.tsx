import React from 'react';
import './Navigation.scss';
import { IonIcon } from 'react-ion-icon';
import { useAppDispatch } from 'app/hooks';
import { authActions } from 'features/auth/authSlice';
import { useHistory, useLocation } from 'react-router-dom';
import { ConfirmPopup } from './ConfirmPopup';
import logoApp from '../../assets/images/new_logo.png';

export const Navigation: React.FC<any> = (props) => {
  const dispatch = useAppDispatch();
  const history = useHistory();
  const location = useLocation();
  const [isWideSideBar, setWidthSideBar] = React.useState(false);

  const [modalShow, setModalShow] = React.useState(false);

  const navigatePage = (linkProps: string) => {
    setWidthSideBar(false);
    history.push(linkProps);
  };

  const handleLogoutClick = () => {
    setWidthSideBar(false);
    setModalShow(false);
    dispatch(authActions.logout());
    localStorage.removeItem('access_token');
    localStorage.removeItem('id_data');
    localStorage.removeItem('firstName_data');
    localStorage.removeItem('lastName_data');
    localStorage.removeItem('avatar_data');
    localStorage.removeItem('selectedAppointment');
    localStorage.removeItem('type');
    localStorage.removeItem('id_user');
    // redirect to login page
    history.replace('/login');
  };

  return (
    <>
      <div className="nav_container">
        <div className={!isWideSideBar ? 'navigation' : 'navigation wide'}>
          <ul>
            <li className="li_item">
              <a>
                <div className="icon">
                  <img src={logoApp} alt="HiDoctor" />
                </div>
                <span className="title">HiDoctor</span>
              </a>
            </li>
            <li className="li_item" onClick={() => setWidthSideBar(!isWideSideBar)}>
              <a title="Phóng to thu nhỏ">
                <span className="icon">
                  <IonIcon name="menu-outline"></IonIcon>
                </span>
                <span className="title"></span>
              </a>
            </li>
            {props.liArr.map((singleLi: any, index: number) => (
              <li
                key={index}
                className={
                  location.pathname === singleLi.navProps ||
                  (index === 0 && location.pathname === '/')
                    ? 'li_item active'
                    : 'li_item'
                }
                onClick={() => navigatePage(singleLi.navProps)}
              >
                <a title={singleLi.liText}>
                  <span className="icon">
                    <IonIcon
                      name={
                        location.pathname === singleLi.navProps
                          ? singleLi.iconActive
                          : singleLi.iconName
                      }
                    ></IonIcon>
                  </span>
                  <span className="title">{singleLi.liText}</span>
                </a>
              </li>
            ))}
            <li className="li_item" onClick={() => setModalShow(true)}>
              <a title="Đăng xuất">
                <span className="icon">
                  <IonIcon name="log-out-outline"></IonIcon>
                </span>
                <span className="title">Đăng xuất</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
      <ConfirmPopup
        show={modalShow}
        onHide={() => setModalShow(false)}
        titleString="Đăng xuất"
        msgString="Bạn có muốn đăng xuất?"
        onYes={() => handleLogoutClick()}
        dialogClassName="customizeModal"
      />
    </>
  );
};
