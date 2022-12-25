import React from 'react';
import classes from './RegisterPage.module.scss';
import Multiselect from 'multiselect-react-dropdown';
import { DoctorSpecialist } from 'models/specialists';
import { urlApi } from 'constants/UrlApi';
import { useHistory } from 'react-router-dom';

const RegisterPage: React.FC<any> = (specialistsProp) => {
  const history = useHistory();
  const [gender, setGender] = React.useState('MALE');
  const [selected, setSelected] = React.useState([]);

  const emailInputRef = React.useRef<HTMLInputElement>(null);
  const firstNameInputRef = React.useRef<HTMLInputElement>(null);
  const lastNameInputRef = React.useRef<HTMLInputElement>(null);
  const phoneInputRef = React.useRef<HTMLInputElement>(null);
  // const experienceInputRef = React.useRef<HTMLInputElement>(null);
  const addressInputRef = React.useRef<HTMLInputElement>(null);
  const dobInputRef = React.useRef<HTMLInputElement>(null);
  const onOptionChange = (e: any) => {
    setGender(e.target.value);
  };

  const handleRegisterClick = (event: any) => {
    event.preventDefault();
    const enteredEmail = emailInputRef.current?.value;
    const enteredFirstName = firstNameInputRef.current?.value;
    const enteredLastName = lastNameInputRef.current?.value;
    const enteredPhonne = phoneInputRef.current?.value;
    // const enteredExperience = Number(experienceInputRef.current?.value);
    const enteredAddress = addressInputRef.current?.value;
    const enteredDob = dobInputRef.current?.value;
    const selectedArr = [...selected];
    const idArr = selectedArr.map((singleSelect: DoctorSpecialist) => singleSelect.id);
    const currentToken = localStorage.getItem('access_token');

    var myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');
    myHeaders.append('Authorization', 'Bearer ' + currentToken);

    var raw = JSON.stringify({
      email: enteredEmail,
      firstName: enteredLastName,
      lastName: enteredFirstName,
      dob: enteredDob,
      avatar: 'https://cuu-be.s3.amazonaws.com/cuu-be/2022/10/23/68GE2G.png',
      phoneNumber: enteredPhonne,
      address: enteredAddress,
      gender: gender,
      // experienceYears: enteredExperience,
      specialists: idArr,
    });

    var requestOptions: RequestInit = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow',
    };

    fetch(urlApi + 'manager/doctor/register/', requestOptions)
      .then((response) => {
        if (response.status === 201) {
          specialistsProp.showNotificationProp(true, 'Thành công', 'Tạo tài khoản thành công!');
          setTimeout(() => {
            history.replace('/manager/home');
          }, 3000);
        } else {
          specialistsProp.showNotificationProp(
            false,
            'Không thành công',
            'Vui lòng nhập email khác và thử lại!'
          );
        }
      })
      .catch((error) => console.log('error', error));
  };

  return (
    <section className={classes.backgroundBody}>
      <div className={classes.container}>
        <div className={classes.title}>Tạo tài khoản</div>

        <form onSubmit={handleRegisterClick}>
          <div className={classes.userDetails}>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Họ</span>
              <input
                className={classes.inputDiv}
                type="text"
                placeholder="Vui lòng nhập họ"
                required
                ref={firstNameInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Tên</span>
              <input
                className={classes.inputDiv}
                type="text"
                placeholder="Vui lòng nhập tên"
                required
                ref={lastNameInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Email</span>
              <input
                className={classes.inputDiv}
                type="email"
                placeholder="Vui lòng nhập email"
                required
                ref={emailInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Số điện thoại</span>
              <input
                className={classes.inputDiv}
                type="text"
                placeholder="Vui lòng nhập số điện thoại"
                required
                ref={phoneInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Địa chỉ</span>
              <input
                className={classes.inputDiv}
                type="text"
                placeholder="Vui lòng nhập địa chỉ"
                required
                ref={addressInputRef}
              />
            </div>
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Ngày sinh</span>
              <input className={classes.inputDiv} type="date" required ref={dobInputRef} />
            </div>
            {/* <div className={classes.inputBox}>
                <span className={classes.titleLabel}>Số năm kinh nghiệm</span>
                <input
                  className={classes.inputDiv}
                  type="number"
                  placeholder="Vui lòng nhập số năm"
                  required
                  ref={experienceInputRef}
                />
              </div> */}
            <div className={classes.inputBox}>
              <span className={classes.titleLabel}>Chuyên khoa</span>
              <Multiselect
                isObject={true}
                onKeyPressFn={function noRefCheck() {}}
                onRemove={setSelected}
                onSearch={function noRefCheck() {}}
                onSelect={setSelected}
                options={specialistsProp.specialistsProp}
                displayValue="name"
                selectedValues={selected}
                placeholder="Chọn chuyên ngành"
                selectionLimit={4}
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
            <button className={classes.btnRegister}>Tạo tài khoản</button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default RegisterPage;
