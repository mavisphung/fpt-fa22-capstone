import React, { useEffect, useRef, useState } from 'react';

import classes from './Profile.module.scss';
import { urlApi } from 'constants/UrlApi';
import { User } from 'models/user';
import { requestOption, imageHeader } from 'constants/HeadersRequest';
import { Tab, Tabs } from 'react-bootstrap';
import { ChangePassword } from './ChangePassword';
import { IonIcon } from 'react-ion-icon';
import { timeOutSeconds } from 'constants/ConstValue';

const Profile: React.FC<{ profileProps: User; showNotificationToast: any }> = (profileProps) => {
  const [keyTab, setKeyTab] = useState('detailProfile');
  const avatarDoctor = String(localStorage.getItem('avatar_data'));
  const [gender, setGender] = useState(profileProps.profileProps?.gender);
  const firstNameInputRef = useRef<HTMLInputElement>(null);
  const lastNameInputRef = useRef<HTMLInputElement>(null);
  const phoneInputRef = useRef<HTMLInputElement>(null);
  const addressInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<any>();
  const [preview, setPreview] = useState<any>();

  // create a preview as a side effect, whenever selected file is changed
  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);

    // free memory when ever this component is unmounted
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  const onSelectFile = (e: any) => {
    if (!e.target.files || e.target.files.length === 0) {
      setSelectedFile(undefined);
      return;
    }

    // I've kept this example simple by using the first image instead of multiple
    setSelectedFile(e.target.files[0]);
  };

  const onOptionChange = (e: any) => {
    setGender(e.target.value);
  };

  const handleEditProfile = (event: any) => {
    event.preventDefault();
    const enteredFirstName = firstNameInputRef.current?.value;
    const enteredLastName = lastNameInputRef.current?.value;
    const enteredPhonne = phoneInputRef.current?.value;
    const enteredAddress = addressInputRef.current?.value;

    const currentToken = localStorage.getItem('access_token');
    var jsonHeaders = new Headers();
    jsonHeaders.append('Content-Type', 'application/json');
    jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

    if (selectedFile !== undefined) {
      const arrFile = [
        {
          ext: selectedFile.name.split('.').pop(),
          size: Number(selectedFile.size / (1024 * 1024)),
        },
      ];

      var raw = JSON.stringify({
        images: arrFile,
      });

      requestOption.method = 'POST';
      requestOption.headers = jsonHeaders;
      requestOption.body = raw;

      fetch(urlApi + 'get-presigned-urls/', requestOption)
        .then((response) => response.json())
        .then((result) => result.data.urls)
        .then(async (urls) => {
          const url = urls[0];
          const fileRaw = selectedFile;
          requestOption.method = 'PUT';
          requestOption.headers = imageHeader;
          requestOption.body = fileRaw;
          await fetch(url, requestOption)
            .then((res) => res.url.slice(0, res.url.indexOf('?')))
            .then(async (avatarUrl) => {
              var raw = JSON.stringify({
                firstName: enteredFirstName,
                lastName: enteredLastName,
                phoneNumber: enteredPhonne,
                gender: gender,
                address: enteredAddress,
                avatar: avatarUrl,
              });
              requestOption.method = 'PUT';
              requestOption.headers = jsonHeaders;
              requestOption.body = raw;
              await fetch(urlApi + 'user/me/', requestOption).then((response) => {
                if (response.status === 201) {
                  localStorage.setItem('firstName_data', String(enteredFirstName));
                  localStorage.setItem('lastName_data', String(enteredLastName));
                  localStorage.setItem('avatar_data', avatarUrl);
                  profileProps.showNotificationToast(
                    true,
                    'Thành công',
                    'Cập nhật thông tin cá nhân thành công!'
                  );
                  setTimeout(() => {
                    window.location.reload();
                  }, timeOutSeconds);
                } else {
                  profileProps.showNotificationToast(
                    false,
                    'Không thành công',
                    'Vui lòng thử lại!'
                  );
                }
              });
            });
        })
        .catch((error) => console.log('error', error));
    } else {
      var raw = JSON.stringify({
        firstName: enteredFirstName,
        lastName: enteredLastName,
        phoneNumber: enteredPhonne,
        gender: gender,
        address: enteredAddress,
        avatar: localStorage.getItem('avatar_data'),
      });
      requestOption.method = 'PUT';
      requestOption.headers = jsonHeaders;
      requestOption.body = raw;
      fetch(urlApi + 'user/me/', requestOption).then((response) => {
        if (response.status === 201) {
          localStorage.setItem('firstName_data', String(enteredFirstName));
          localStorage.setItem('lastName_data', String(enteredLastName));
          profileProps.showNotificationToast(
            true,
            'Thành công',
            'Cập nhật thông tin cá nhân thành công!'
          );
          setTimeout(() => {
            window.location.reload();
          }, timeOutSeconds);
        } else {
          profileProps.showNotificationToast(false, 'Không thành công', 'Vui lòng thử lại!');
        }
      });
    }
  };

  return (
    <section className={classes.backgroundBody}>
      <div className={classes.avatarDoctor}>
        <label htmlFor="uploadAvatar" className={classes.inputLabel}>
          <input
            type="file"
            accept="image/png, image/jpeg"
            onChange={onSelectFile}
            id="uploadAvatar"
            hidden
          />
          {selectedFile ? <img src={preview} /> : <img src={avatarDoctor} alt="avatarDoctor" />}
          <IonIcon name="camera"></IonIcon>
        </label>
      </div>
      <div className={classes.container}>
        <Tabs
          activeKey={keyTab}
          onSelect={(k: any) => setKeyTab(k)}
          id="justify-tab-example"
          className="mb-3"
          justify
        >
          <Tab eventKey="detailProfile" title="Thông tin cá nhân">
            <form onSubmit={handleEditProfile}>
              <div className={classes.userDetails}>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Họ</span>
                  <input
                    className={classes.inputDiv}
                    type="text"
                    required
                    ref={lastNameInputRef}
                    defaultValue={profileProps.profileProps?.lastName}
                  />
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Tên</span>
                  <input
                    className={classes.inputDiv}
                    type="text"
                    required
                    ref={firstNameInputRef}
                    defaultValue={profileProps.profileProps?.firstName}
                  />
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Số điện thoại</span>
                  <input
                    className={classes.inputDiv}
                    type="text"
                    required
                    ref={phoneInputRef}
                    defaultValue={profileProps.profileProps?.phoneNumber}
                  />
                </div>
                <div className={classes.inputBox}>
                  <span className={classes.titleLabel}>Địa chỉ</span>
                  <input
                    className={classes.inputDiv}
                    type="text"
                    required
                    ref={addressInputRef}
                    defaultValue={profileProps.profileProps?.address}
                  />
                </div>
              </div>
              <div className={classes.genderDetails}>
                <span className={classes.genderTitle}>Giới tính</span>
                <div className={classes.category}>
                  <label htmlFor="dot-1">
                    <input
                      type="radio"
                      value="MALE"
                      name="gender"
                      id="dot-1"
                      checked={gender === 'MALE'}
                      onChange={onOptionChange}
                    />
                    <span className={classes.gender}>Nam</span>
                  </label>
                  <label htmlFor="dot-2">
                    <input
                      type="radio"
                      value="FEMALE"
                      name="gender"
                      id="dot-2"
                      checked={gender === 'FEMALE'}
                      onChange={onOptionChange}
                    />
                    <span className={classes.gender}>Nữ</span>
                  </label>
                  <label htmlFor="dot-3">
                    <input
                      type="radio"
                      value="OTHER"
                      name="gender"
                      id="dot-3"
                      checked={gender === 'OTHER'}
                      onChange={onOptionChange}
                    />
                    <span className={classes.gender}>Khác</span>
                  </label>
                </div>
              </div>
              <div className={classes.buttonSubmit}>
                <button className={classes.btnSave}>Lưu</button>
              </div>
            </form>
          </Tab>
          <Tab eventKey="changePassword" title="Đổi mật khẩu">
            <ChangePassword showNotificationToast={profileProps.showNotificationToast} />
          </Tab>
        </Tabs>
      </div>
    </section>
  );
};

export default Profile;
