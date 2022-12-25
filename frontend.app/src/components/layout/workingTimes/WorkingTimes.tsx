import { weekdayIdMap } from 'constants/Enum';
import { requestOption } from 'constants/HeadersRequest';
import { urlApi } from 'constants/UrlApi';
import { Shifts, ShiftTime, ShiftTimes } from 'models/shiftTime';
import React from 'react';
import { IonIcon } from 'react-ion-icon';
import ToggleSwitch from './ToggleSwitch';
import classes from './WorkingTimes.module.scss';

const WorkingTimes: React.FC<{ shiftsTimeProp: Shifts; showNotificationToast: any }> = (
  shiftsTimeProp
) => {
  const [timeShiftList, setTimeList] = React.useState(shiftsTimeProp.shiftsTimeProp);
  let shifts = new Map<string, ShiftTimes>(timeShiftList);
  const currentToken = localStorage.getItem('access_token');
  var jsonHeaders = new Headers();
  jsonHeaders.append('Content-Type', 'application/json');
  jsonHeaders.append('Authorization', 'Bearer ' + currentToken);
  requestOption.headers = jsonHeaders;

  const handleAddTimeShift = (id: string) => {
    setTimeList(
      shifts.set(id, [
        ...(shifts.get(id) ?? []),
        {
          id: undefined,
          weekday: Number(id),
          startTime: '18:00:00',
          endTime: '20:30:00',
          isActive: false,
        },
      ])
    );
  };

  const handleRemoveTimeShift = (id: string, index: number, shiftId: any) => {
    let shiftsOfWeekDay = shifts.get(id);
    if (shiftId === undefined) {
      shiftsOfWeekDay?.splice(index, 1);
      shiftsTimeProp.showNotificationToast(true, 'Thành công', 'Xóa ca làm việc thành công!');
      setTimeList(shifts);
    } else {
      requestOption.method = 'DELETE';

      requestOption.body = undefined;

      fetch(urlApi + 'doctor/shifts/' + shiftId + '/', requestOption)
        .then((response) => {
          if (response.status === 204) {
            shiftsOfWeekDay?.splice(index, 1);
            shiftsTimeProp.showNotificationToast(true, 'Thành công', 'Xóa ca làm việc thành công!');
            setTimeList(shifts);
          } else {
            shiftsTimeProp.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
          }
        })
        .catch((error) => console.log('error', error));
    }
  };

  const handleToggleChange = (id: string, index: number, prevState: boolean) => {
    let shiftsOfWeekDay = shifts.get(id);
    if (shiftsOfWeekDay !== undefined) {
      shiftsOfWeekDay[index].isActive = !prevState;
    }
    setTimeList(shifts);
  };

  const onChangeStartTime = (id: string, index: number, e: any) => {
    let shiftsOfWeekDay = shifts.get(id);
    if (shiftsOfWeekDay !== undefined) {
      shiftsOfWeekDay[index].startTime = e.target.value;
    }
    setTimeList(shifts);
  };

  const onChangeEndTime = (id: string, index: number, e: any) => {
    let shiftsOfWeekDay = shifts.get(id);
    if (shiftsOfWeekDay !== undefined) {
      shiftsOfWeekDay[index].endTime = e.target.value;
    }
    setTimeList(shifts);
  };

  const handleUpdateShifts = (event: any) => {
    event.preventDefault();

    let existedShifts = new Array<ShiftTime>();
    let newShifts = new Array<ShiftTime>();
    let shiftsBody = new Map<string, ShiftTimes>([
      ['shifts', existedShifts],
      ['newShifts', newShifts],
    ]);

    timeShiftList.forEach((shiftArr) => {
      shiftArr.map((shift) => {
        if (shift.id === undefined) {
          newShifts.push(shift);
          shiftsBody.set('newShifts', newShifts);
        } else {
          existedShifts.push(shift);
          shiftsBody.set('shifts', existedShifts);
        }
      });
    });

    var raw = JSON.stringify(Object.fromEntries(shiftsBody));
    requestOption.method = 'PUT';
    requestOption.body = raw;

    fetch(urlApi + 'doctor/shifts/', requestOption)
      .then((response) => {
        if (response.status === 202) {
          shiftsTimeProp.showNotificationToast(true, 'Thành công', 'Đã cập nhật ca làm việc!');
        } else {
          return response.json().then(() => {
            shiftsTimeProp.showNotificationToast(false, 'Không thành công', 'Đã có lỗi xảy ra!');
          });
        }
      })
      .catch((error) => console.log('error', error));
  };

  return (
    <>
      <div className={classes.wtMain}>
        <div className={classes.wtMain_workingTimesArea}>
          <div className={classes.cardTitle}>
            <h5>Thời gian bác sĩ làm việc với ứng dụng</h5>
          </div>
          <form className={classes.form_div} onSubmit={handleUpdateShifts}>
            {Array.from(timeShiftList.entries()).map(([id, shiftArr]) => (
              <table key={id}>
                <tbody>
                  {shiftArr.map((singleTimeShift: any, index: any) => (
                    <tr key={index}>
                      {index === 0 ? <td>{weekdayIdMap.get(id)}</td> : <td></td>}
                      <td>
                        <span>từ</span>
                      </td>
                      <td>
                        <input
                          type="time"
                          className={classes.inputTimes}
                          value={singleTimeShift.startTime}
                          onChange={(e: any) => onChangeStartTime(id, index, e)}
                        />
                      </td>
                      <td>
                        <span>đến</span>
                      </td>
                      <td>
                        <input
                          type="time"
                          className={classes.inputTimes}
                          value={singleTimeShift.endTime}
                          onChange={(e: any) => onChangeEndTime(id, index, e)}
                        />
                      </td>
                      <td>
                        <span>
                          <div>
                            <ToggleSwitch
                              id={'ca' + id + index}
                              name={'ca' + id + index}
                              checked={singleTimeShift.isActive}
                              onChange={() =>
                                handleToggleChange(id, index, singleTimeShift.isActive)
                              }
                            />
                          </div>
                        </span>
                      </td>

                      {shiftArr.length < 4 && shiftArr.length - 1 === index && (
                        <td>
                          <button
                            title="Thêm ca"
                            id={'ca' + id + index}
                            onClick={(event: any) => {
                              event.preventDefault();
                              handleAddTimeShift(id);
                            }}
                          >
                            <IonIcon color="secondary" name="add-circle"></IonIcon>
                          </button>
                        </td>
                      )}
                      {shiftArr.length > 1 && shiftArr.length - 1 !== index && (
                        <td>
                          <button
                            title="Xóa ca"
                            onClick={(event: any) => {
                              event.preventDefault();
                              handleRemoveTimeShift(id, index, singleTimeShift.id);
                            }}
                          >
                            <IonIcon color="danger" name="remove-circle"></IonIcon>
                          </button>
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            ))}
            <div className={classes.btnSaveTime}>
              <button>Lưu</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default WorkingTimes;
