import React from 'react';
import classes from './LoginPage.module.scss';
import imgAuthPage from '../../../assets/images/hi_doctor_logo.png';
// import logoGoogle from '../../../assets/images/gg_logo.png';
import '../../../constants/FontPage.scss';
import '../../../constants/Colors.css';
import { useAppDispatch } from 'app/hooks';
import { authActions } from '../authSlice';
import { useHistory } from 'react-router-dom';
import Multiselect from 'multiselect-react-dropdown';

const LoginPage: React.FC = () => {
  const history = useHistory();
  const dispatch = useAppDispatch();
  const emailInputRef = React.useRef<HTMLInputElement>(null);
  const passwordInputRef = React.useRef<HTMLInputElement>(null);
  const [selectedRole, setSelectedRole] = React.useState(['Bác sĩ']);

  const handleLoginClick = (event: any) => {
    event.preventDefault();
    const enteredEmail = emailInputRef.current?.value;
    const enteredPassword = passwordInputRef.current?.value;
    let userRole = 'DOCTOR';
    if (selectedRole[0] === 'Bác sĩ') {
      userRole = 'DOCTOR';
    } else {
      userRole = 'MANAGER';
    }

    dispatch(
      authActions.login({
        email: enteredEmail,
        password: enteredPassword,
        type: userRole,
      })
    );
  };

  const navigateRegister = (event: React.MouseEvent) => {
    event.preventDefault();
    history.push('/register');
  };

  return (
    <section className={classes.section_img}>
      <div className={classes.imgBx}>
        <img src={imgAuthPage} alt="HiDoctor" />
      </div>
      <div className={classes.contentBx}>
        <div className={classes.formBx}>
          <h2>Đăng nhập</h2>
          <form onSubmit={handleLoginClick}>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Email</span>
              <input
                className={classes.inputDiv}
                type="email"
                id="email"
                required
                ref={emailInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Mật Khẩu</span>
              <input
                className={classes.inputDiv}
                type="password"
                id="password"
                required
                ref={passwordInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Bạn là: </span>
              <Multiselect
                singleSelect={true}
                isObject={false}
                onKeyPressFn={function noRefCheck() {}}
                onRemove={setSelectedRole}
                onSearch={function noRefCheck() {}}
                onSelect={setSelectedRole}
                options={['Bác sĩ', 'Quản lí']}
                selectedValues={selectedRole}
                placeholder="Vai trò của bạn"
              />
            </div>
            <div className={classes.inputBox}>
              <button className={classes.btnSubmit}>Đăng nhập</button>
            </div>
            {/* <div className={classes.inputBx}>
              <p>
                Bạn chưa có tài khoản?{' '}
                <a className={classes.signUp} onClick={navigateRegister}>
                  Đăng kí
                </a>
              </p>
            </div> */}
          </form>
          {/* <h3>Hoặc bạn có thể</h3>
          <div className={classes.inputBx}>
            <button className={classes.btnGoogle}>
              <img src={logoGoogle} alt="logoGoogle" className={classes.logo_Google} />
              Đăng nhặp bằng Google
            </button>
          </div> */}
        </div>
      </div>
    </section>
  );
};

export default LoginPage;
