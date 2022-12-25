import React, { useRef, useState } from 'react';
import Pagination from 'rc-pagination';
import 'rc-pagination/assets/index.css';
import { pageSizeNumber } from 'constants/ConstValue';
import { IonIcon } from 'react-ion-icon';
import classes from './MyTable.module.scss';
import { ServiceType } from 'constants/Enum';
import { useHistory } from 'react-router-dom';

const MyTable: React.FC<any> = (props) => {
  const searchValueRef = useRef<HTMLInputElement>(null);
  const [rendertime, setRenderState] = useState(0);
  const history = useHistory();

  const searchFunction = (event: any) => {
    event.preventDefault();
    updatePage(1);
  };

  const updatePage = async (p: number) => {
    await props.getDataFuntion(p, pageSizeNumber, searchValueRef.current?.value);
    setRenderState(rendertime + 1);
  };

  const deleteService = async (idService: number) => {
    await props.deleteFunction(idService);
    setRenderState(rendertime + 1);
  };

  const assignChkBox = async (idService: number) => {
    if (!props.currentServicesDoctor.includes(idService)) {
      await props.addServiceForDoctorFunction(idService, searchValueRef.current?.value);
    } else {
      await props.unassignServiceFunction(idService, searchValueRef.current?.value);
    }

    setRenderState(rendertime + 1);
  };

  const handleChangeChkBox = async (idService: number) => {
    await props.changeActivateServiceFuntion(idService, searchValueRef.current?.value);

    setRenderState(rendertime + 1);
  };

  const assignServiceDoctor = (idDoctor: number) => {
    localStorage.setItem('selected_account', String(idDoctor));
    history.push('/manager/assignServices');
  };

  const blockAccount = async (idDoctor: number, accountStatus: any) => {
    await props.blockAccFunction(idDoctor, accountStatus, searchValueRef.current?.value);
    setRenderState(rendertime + 1);
  };

  const tableRows = (rowData: any) => {
    const { key, index } = rowData;
    const tableCell = Object.keys(props.theadProp);
    if (props.dataListType === 'account') {
      const columnData = tableCell.map((keyD, i) => {
        if (keyD === 'avatar') {
          return (
            <td key={i} className={classes.img_td}>
              <div className={classes.imgBx}>
                <img src={key[keyD]} alt="doctorAvatar" />
              </div>
            </td>
          );
        } else if (keyD === 'isApproved') {
          if (key[keyD]) {
            return (
              <td key={i} style={{ color: 'green' }}>
                Hoạt động
              </td>
            );
          } else {
            return (
              <td key={i} style={{ color: 'grey' }}>
                Tạm ngừng
              </td>
            );
          }
        } else if (keyD === 'fullName') {
          return (
            <td key={i} title={key[keyD]}>
              {key['lastName']} {key['firstName']}
            </td>
          );
        } else {
          return (
            <td key={i} title={key[keyD]}>
              {key[keyD]}
            </td>
          );
        }
      });

      return (
        <tr key={index}>
          {columnData}
          {key['isApproved'] ? (
            <td>
              <button
                className={classes.deletePrescriptionButton}
                onClick={() => blockAccount(key['id'], key['isApproved'])}
              >
                Khóa
              </button>
              <button
                className={classes.assignServiceButton}
                onClick={() => assignServiceDoctor(key['id'])}
              >
                Chỉ định
              </button>
            </td>
          ) : (
            <td>
              <button
                className={classes.deletePrescriptionButton}
                onClick={() => blockAccount(key['id'], key['isApproved'])}
              >
                Mở khóa
              </button>
              {/* <button className={classes.assignServiceButton}>Chỉ định</button> */}
            </td>
          )}
        </tr>
      );
    } else {
      const columnData = tableCell.map((keyD, i) => {
        if (keyD === 'category') {
          return (
            <td key={i} title={ServiceType.get(key[keyD])}>
              {ServiceType.get(key[keyD])}
            </td>
          );
        } else {
          return (
            <td key={i} title={key[keyD]}>
              {key[keyD]}
            </td>
          );
        }
      });
      if (props.dataListType === 'servicesManager') {
        return (
          <tr key={index}>
            {columnData}
            <td>
              <button
                className={classes.deletePrescriptionButton}
                onClick={() => deleteService(key['id'])}
              >
                Xoá
              </button>
            </td>
          </tr>
        );
      } else if (props.dataListType === 'assignServices') {
        return (
          <tr key={index}>
            {columnData}
            <td>
              <input
                type="checkbox"
                id={key['id']}
                name={key['id']}
                value={key['id']}
                checked={props.currentServicesDoctor.includes(key['id'])}
                onChange={() => assignChkBox(key['id'])}
              />
            </td>
          </tr>
        );
      } else {
        return (
          <tr key={index}>
            {columnData}
            <td>
              <input
                type="checkbox"
                id={key['id']}
                name={key['id']}
                value={key['id']}
                checked={props.activeServicesArray.includes(key['id'])}
                onChange={() => handleChangeChkBox(key['id'])}
              />
            </td>
          </tr>
        );
      }
    }
  };

  const tableData = () => {
    return props.dataProp.map((key: any, index: any) => tableRows({ key, index }));
  };

  const headRow = () => {
    return Object.values(props.theadProp).map((title: any, index: number) => {
      if (title === '') {
        return (
          <td className={classes.img_th} key={index}>
            {title}
          </td>
        );
      } else {
        return <td key={index}>{title}</td>;
      }
    });
  };

  return (
    <>
      <div className={classes.details}>
        <div className={classes.details_requests}>
          <div className={classes.cardHeader}>
            <h3>{props.headerString}</h3>
            {props.dataListType !== 'servicesDoctor' && (
              <a className={classes.cardHeader_btn} onClick={props.addFunction}>
                <IonIcon color="secondary" name="add-outline"></IonIcon>Thêm {props.addString}
              </a>
            )}
          </div>
          <form onSubmit={searchFunction}>
            <div className={classes.searchArea}>
              <input
                type="text"
                className={classes.searchInput}
                placeholder={props.searchPlaceHolder}
                ref={searchValueRef}
              />
              <IonIcon name="search-outline"></IonIcon>
            </div>
          </form>
          <table>
            <thead>
              <tr>
                {headRow()}
                <td>Thao tác</td>
              </tr>
            </thead>
            <tbody>
              {props.dataProp.length > 0 ? (
                tableData()
              ) : (
                <tr>
                  <td></td>
                  <td>Danh sách trống.</td>
                  <td></td>
                  <td></td>
                </tr>
              )}
            </tbody>
          </table>
          {props.totalItemsProp !== 0 && (
            <Pagination
              pageSize={pageSizeNumber}
              onChange={updatePage}
              current={props.currentPageNumber}
              total={props.totalItemsProp}
            />
          )}
        </div>
      </div>
    </>
  );
};
export default MyTable;
