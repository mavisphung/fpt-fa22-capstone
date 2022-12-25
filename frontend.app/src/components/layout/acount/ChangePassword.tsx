import React from 'react';
import classes from './ChangePassword.module.scss';
import { requestOption } from 'constants/HeadersRequest';
import { urlApi } from 'constants/UrlApi';

export const ChangePassword: React.FC<any> = (props) => {
  const currentPassRef = React.useRef<HTMLInputElement>(null);
  const newPassRef = React.useRef<HTMLInputElement>(null);
  const reNewPassRef = React.useRef<HTMLInputElement>(null);

  const handleChangePassword = (event: any) => {
    event.preventDefault();
    const enteredCurrentPass = currentPassRef.current?.value;
    const enteredNewPass = newPassRef.current?.value;
    const enteredReNewPass = reNewPassRef.current?.value;

    const currentToken = localStorage.getItem('access_token');

    var jsonHeaders = new Headers();
    jsonHeaders.append('Content-Type', 'application/json');
    jsonHeaders.append('Authorization', 'Bearer ' + currentToken);

    var raw = JSON.stringify({
      currentPassword: enteredCurrentPass,
      newPassword: enteredNewPass,
      reNewPassword: enteredReNewPass,
    });

    requestOption.method = 'PUT';
    requestOption.headers = jsonHeaders;
    requestOption.body = raw;

    fetch(urlApi + 'user/me/change-password/', requestOption)
      .then((response) =>
        props.showNotificationToast(true, 'Thành công', 'Cập nhật mật khẩu thành công!')
      )
      .catch((error) => props.showNotificationToast(false, 'Không thành công', error));
  };

  return (
    <div className={classes.backgroundBodyPass}>
      <div className={classes.containerPass}>
        <form onSubmit={handleChangePassword}>
          <div className={classes.userDetailsPass}>
            <div className={classes.inputBoxPass}>
              <span className={classes.titleLabelPass}>Mật khẩu hiện tại</span>
              <input
                className={classes.inputDivPass}
                type="password"
                placeholder="Vui lòng nhập mật khẩu hiện tại"
                required
                ref={currentPassRef}
              />
            </div>
            <div className={classes.inputBoxPass}>
              <span className={classes.titleLabelPass}>Mật khẩu mới</span>
              <input
                className={classes.inputDivPass}
                type="password"
                placeholder="Vui lòng nhập mật khẩu mới"
                required
                ref={newPassRef}
              />
            </div>
            <div className={classes.inputBoxPass}>
              <span className={classes.titleLabelPass}>Xác nhận mật khẩu mới</span>
              <input
                className={classes.inputDivPass}
                type="password"
                placeholder="Xác nhận mật khẩu mới"
                required
                ref={reNewPassRef}
              />
            </div>
          </div>
          <div className={classes.buttonSubmitPass}>
            <button className={classes.btnSavePass}>Cập nhật</button>
          </div>
        </form>
      </div>
    </div>
  );
};
