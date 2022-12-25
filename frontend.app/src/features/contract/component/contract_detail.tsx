import {
  faBackward,
  faBedPulse,
  faBookMedical,
  faCalendarCheck,
  faCalendarDay,
  faFileMedical,
  faHome,
  faMarsAndVenus,
  faMessage,
  faPills,
  faUserShield,
  faVial,
  faVialCircleCheck,
  faVialVirus,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { CustomDatePicker } from 'components/common/DatetimePicker';
import { ITreamtentContract } from 'models/contract';
import { ContractStatus } from 'models/enum';
import { IMedicalInstruction, IPrescription } from 'models/health_record';
import { IPatient } from 'models/patient';
import { useState } from 'react';
import { options } from '../../../utils/utils';
import '../style/contract_detail.scss';
import '../style/detail2.scss';
import { ContractSchedule } from './contract_schedule';


const statusMap = new Map(
  [
    [ContractStatus.APPROVED.toLocaleLowerCase(), 'Đã chấp thuận'],
    [ContractStatus.CANCELLED.toLocaleLowerCase(), 'Đã hủy'],
    [ContractStatus.PENDING.toLocaleLowerCase(), 'Đang chờ'],
    [ContractStatus.IN_PROGRESS.toLocaleLowerCase(), 'Đang tiến hành'],
    [ContractStatus.POSTPONE.toLocaleLowerCase(), 'Tạm hoãn'],
  ]
)

export const ContractDetailInfo = (props: {
  patient: IPatient;
  prescription: IPrescription[];
  instructions: IMedicalInstruction[];
  contract: ITreamtentContract;
}) => {
  const [selectedSharedInstructions, setSelectedSharedInstructions] = useState<number[]>([]);
  const [selectedSharedPrescriptions, setSelectedSharedPrescriptions] = useState<number[]>([]);
  let patient = props.contract.patient;
  let supervisor = props.contract.supervisor;
  let healthRecord = props.contract.healthRecord;
  let fullname = patient.lastName.concat(' ', patient.firstName);
  let supFullname = supervisor.lastName.concat(' ', supervisor.firstName);
  let dob = new Date(healthRecord[0].patient.dob as string).toLocaleDateString('vi-VI', options);
  let startAt = new Date(props.contract.startedAt).toLocaleDateString('vi-VI', options);
  let endAt = new Date(props.contract.endedAt).toLocaleDateString('vi-VI', options);
  let details = props.contract.healthRecord.map((r) => {
    return r ? r.detail : undefined;
  });
  let monitoredPathologies = details.flatMap((d) => {
    return d ? d.monitoredPathology : undefined;
  });
  let diseaseHistory = monitoredPathologies.map((d) => {
    return d ? d.code.concat(' - ', d.diseaseName) : undefined;
  });
  const [selectedEndDate, setSelectedEndDate] = useState<string>(
    props.contract.status.toLowerCase() === ContractStatus.PENDING.toLowerCase() ? new Date().toISOString() : props.contract.endedAt.toString()
  );

  const handleSharedInstruction = (id: number) => {
    setSelectedSharedInstructions([...selectedSharedInstructions, id]);
  };

  const handleSharedPresctiptions = (id: number) => {
    setSelectedSharedPrescriptions([...selectedSharedPrescriptions, id]);
  };

  const handleChangeDate = (date: string, comparator: string) => {
    setSelectedEndDate(date);
  };

  return (
    <>
      {/* <div className="navigator">
                <FontAwesomeIcon icon={faBackward}></FontAwesomeIcon>
            </div> */}
    </>
  );
};

export const ContractInfo = (props: {
  contract: ITreamtentContract,
}) => {

  let patient = props.contract.patient;
  let supervisor = props.contract.supervisor;
  let healthRecord = props.contract.healthRecord;
  let fullname = patient.lastName.concat(' ', patient.firstName);
  let supFullname = supervisor.lastName.concat(' ', supervisor.firstName);
  let dob = new Date(healthRecord[0].patient.dob as string).toLocaleDateString('vi-VI', options);
  return (
    <div className='page'>
      <div className='label_status'>
        <span className='label'>Trạng thái hợp đồng</span>
        <span className='status'>{statusMap.get(props.contract.status.toLocaleLowerCase())}</span>
      </div>
      <div className='info_summary_action'>
        <div className='summary'>
          <div className='avatar'>
            <img src={patient.avatar} className='circle'></img>
          </div>
          <div className='fullname'>
            <span className='wrapper'>
              {fullname} <FontAwesomeIcon icon={faMessage} fixedWidth></FontAwesomeIcon>
            </span>
          </div>
        </div>
        <div className='actions'>
          {
            props.contract.status.toLowerCase() === ContractStatus.PENDING.toLowerCase() ? <div className='btn-group-center'>
              <button className='action_button'>Chấp thuận</button>
              <button className='action_button'>Hủy bỏ</button>
            </div> : <>

            </>
          }
        </div>
      </div>
      <div className='personal_detail tab'>
        <div className="contract_short_info">
          <span className="icon">
            <FontAwesomeIcon size="1x" fixedWidth icon={faMarsAndVenus} /> Giới tính:
          </span>
          <span className="text">{healthRecord[0].patient.gender}</span>
        </div>
        <div className="contract_short_info">
          <span className="icon">
            <FontAwesomeIcon size="1x" fixedWidth icon={faCalendarDay} /> Ngày sinh:
          </span>
          <span className="text">{dob}</span>
        </div>
        <div className="contract_short_info">
          <span className="icon">
            <FontAwesomeIcon size="1x" fixedWidth icon={faUserShield} /> Giám hộ:
          </span>
          <span className="text">{supFullname}</span>
        </div>
        <div className="contract_short_info">
          <span className="icon">
            <FontAwesomeIcon size="1x" fixedWidth icon={faHome} /> Địa chỉ:
          </span>
          <span className="text">{patient.address}</span>
        </div>
      </div>
      <div className='schedule tab'>
        <div className='action_bar'>
          <button className='action_button action_button--approve'>
            Thêm buổi điều trị
          </button>
        </div>
        <div className='schedule_content'>
          <div className='session'>
            <div className='session__datetime'>
              <div className='session__date'>
                <h5>{'20 Th11 2022'}</h5>
              </div>
              <div className='session__time'>
                <p>{'8h30 - 10h30'}</p>
              </div>
            </div>
            <div className='break'></div>
            <div className='session__content'>
              <div className='session_assetment'>
                <p className='session_assetment__title'>Đánh giá của buổi hẹn</p>
                <p className='content'>Mức độ viêm có xu hướng giảm dần tại vùng đầu gối kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk</p>
              </div>
              <div className='session_note'>
                <div className='btn-group'>
                  <button>Bắt đầu</button>
                  <button>Hủy bỏ</button>
                </div>
              </div>
            </div>
          </div>
          <div className='session'>
            <div className='session__datetime'>
              <div className='session__date'>
                <h5>{'20 Th11 2022'}</h5>
              </div>
              <div className='session__time'>
                <p>{'8h30 - 10h30'}</p>
              </div>
            </div>
            <div className='break'></div>
            <div className='session__content'>
              <div className='session_assetment'>
                <p className='session_assetment__title'>Đánh giá của buổi hẹn</p>
                <p className='content'>Phiên điều trị - theo dõi chưa bắt đầu</p>
              </div>
              <div className='session_note'>
                <div className='btn-group'>
                  <button>Bắt đầu</button>
                  <button>Hủy bỏ</button>
                </div>
              </div>
            </div>
          </div>
          <div className='session'>
            <div className='session__datetime'>
              <div className='session__date'>
                <h5>{'20 Th11 2022'}</h5>
              </div>
              <div className='session__time'>
                <p>{'8h30 - 10h30'}</p>
              </div>
            </div>
            <div className='break'></div>
            <div className='session__content'>
              <div className='session_assetment'>
                <p className='session_assetment__title'>Đánh giá của buổi hẹn</p>
                <p className='content'>Mức độ viêm có xu hướng giảm dần tại vùng đầu gối kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk</p>
              </div>
              <div className='session_note'>
                <div className='btn-group--disable'>
                  <button>Bắt đầu</button>
                  <button>Hủy bỏ</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className='medical_record tab'>
        <div className='prescripton'>

        </div>
        <div className='instruction'>

        </div>
      </div>
    </div>
  )
}
