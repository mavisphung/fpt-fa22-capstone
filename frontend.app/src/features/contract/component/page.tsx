import {
  faBedPulse,
  faCalendarDay,
  faCircleInfo,
  faCircleMinus,
  faSearch,
  faUserShield,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { listContract } from 'api/contract_api';
import { CustomDatePicker } from 'components/common/DatetimePicker';
import { ITreamtentContract } from 'models/contract';
import { ContractStatus } from 'models/enum';
import { IPatient } from 'models/patient';
import { ChangeEvent, SyntheticEvent, useEffect, useState } from 'react';
import { options, optionsTime } from 'utils/utils';
import { ContractFilterState } from '../reducer';
import '../style/style.scss';
import '../../../../node_modules/rc-pagination/assets/index.css';
import { ContractDetailInfo, ContractInfo } from './contract_detail';
import Pagination from 'rc-pagination';
import { useAppDispatch } from 'app/hooks';
import { useSelector } from 'react-redux';
import { contractAction, contractFilterSelector, contractPagingSelector } from '../contractSlice';
import { AppointmentStatusMap } from 'constants/Enum';
import { useHistory, useLocation } from 'react-router-dom';

let initialState: ContractFilterState = {
  status: ContractStatus.PENDING,
  startedAt__gte: '2022-12-12',
  startedAt__lte: '2022-12-12',
  keyword: '',
};

const dateOptions = options;
const timeOptions = optionsTime;

export const ContractDropdown = (props: { setOptions: (options: ContractStatus) => void }) => {
  const [selectedState, setSelectedStatus] = useState<ContractStatus>(ContractStatus.PENDING);
  const allowedValue = Object.entries(ContractStatus);
  let status = new Map(allowedValue);
  const onAddStatus = (e: SyntheticEvent<HTMLInputElement>) => {
    let newStatus = e.currentTarget.value;
    let radio = document.getElementById(
      selectedState.toLocaleLowerCase().replaceAll('_', ' ')
    ) as HTMLInputElement;
    console.log(
      'id: ',
      radio,
      'element:',
      radio,
      'selected: ',
      newStatus,
      'map:',
      status.get(newStatus)
    );
    radio.checked = false;
    setSelectedStatus(newStatus as ContractStatus);
    props.setOptions(newStatus as ContractStatus);
  };
  return (
    <div className="dropdown">
      <div className="dropdown__result">
        {<span className="selectedResult">{status.get(selectedState)}</span>}
      </div>
      <div className="dropdown__options">
        <div className="dropdown__options__item">
          {allowedValue.map((v) => {
            return (
              <div className="dropdown__options__item__wrapper">
                <input
                  type={'radio'}
                  value={v[0]}
                  onChange={(e) => onAddStatus(e)}
                  id={v[1].toLowerCase().replace('_', ' ')}
                />{' '}
                {v[1]}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export const SearchBox = (props: {
  keyword: string;
  onKeywordChange: (keyword: string) => void;
}) => {
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log('search box:', e.target.value);
    props.onKeywordChange(e.target.value);
  };
  return (
    <span className="input_wrapper">
      <input
        type={'text'}
        onChange={(e) => {
          handleInputChange(e);
        }}
      />
    </span>
  );
};

export const ContractFilter = (props: { reload: (contracts: ITreamtentContract[]) => void }) => {
  const state = useSelector(contractFilterSelector);
  const dispatch = useAppDispatch();
  async function init() {
    console.log('call result filter ', state);
    let result = await (await listContract(state)).data.data;
    props.reload(result);
  }

  useEffect(() => {
    init();
  }, [state]);

  const handleChangeDate = (date: string, comparator: string) => {
    let newDate = new Date(date);
    let currentState = Object.assign({}, state);
    if (comparator === 'lte') {
      currentState.startedAt__lte = newDate.toISOString();
    }
    if (comparator === 'gte') {
      currentState.startedAt__gte = newDate.toISOString();
    }
    dispatch(contractAction.changeFilter(currentState));
  };
  const handleChangeKeyword = (keyword: string) => {
    let previousState = Object.assign({}, state);
    previousState.keyword = keyword;
    console.log(keyword);
  };

  const handleChangeStatusOptions = (option: ContractStatus) => {
    let currentState = Object.assign({}, state);
    currentState.status = option;
    dispatch(contractAction.changeFilter(currentState));
  };

  return (
    <div className="filter">
      <div className="filter__date">
        <div><p className='filter_label'>Ngày bắt đầu từ:</p></div>
        <CustomDatePicker
          comparator="gte"
          changeDate={handleChangeDate}
          selectedDate={state.startedAt__gte.toLocaleString()}
        />
      </div>
      <div className="filter__date">
        <div><p className='filter_label'>Ngày bắt đầu tới:</p></div>
        <CustomDatePicker
          comparator="lte"
          changeDate={handleChangeDate}
          selectedDate={state.startedAt__lte.toLocaleString()}
        />
      </div>
      <div className="filter__status-keyword">
        <div className="filter__status-keyword__status">
          <div><p className='filter_label'>Trạng thái:</p></div>
          <ContractDropdown setOptions={handleChangeStatusOptions}></ContractDropdown>
        </div>
        <div className="filter__status-keyword__keyword">
          <div><p className='filter_label'>Tên bệnh nhân:</p></div>
          <div className='keyword_container'>
            <SearchBox keyword={state.keyword} onKeywordChange={handleChangeKeyword} />
            <span>
              <FontAwesomeIcon icon={faSearch} size="1x" fixedWidth />
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ContractItem = (props: { contract: ITreamtentContract }) => {
  let contract = props.contract;
  let supervisor = props.contract.supervisor;
  let patient = props.contract.patient;
  let supervisorName = supervisor.lastName.concat(' ', supervisor.firstName);
  let patientName = patient.lastName.concat(' ', patient.firstName);
  return (
    <div className="contract_item">
      <div className="contract_item__summary">
        <div className="contract_item__summary__detail">
          <h5>
            <FontAwesomeIcon icon={faBedPulse} size="xs" fixedWidth />{' '}
            {props.contract.patient.lastName.concat(' ', props.contract.patient.lastName)}
          </h5>
          <div className="contract_item__summary__detail__label">
            <span className="contract_item__summary__detail__label__content">
              {AppointmentStatusMap.get(contract.status)}
            </span>
          </div>
          <div className="contract_item__summary__detail__text">
            <div className="col">
              <span className="contract_supervisor">
                <FontAwesomeIcon icon={faUserShield} size="1x" fixedWidth /> Giám hộ
              </span>
              <span className="contract_supervisor">{supervisorName}</span>
            </div>
            <div className="col">
              <span className="contract_supervisor">
                <FontAwesomeIcon icon={faCalendarDay} size="1x" fixedWidth /> Ngày bắt đầu
              </span>
              <span className="contract_supervisor">
                {new Date(contract.startedAt).toLocaleDateString('vi-VI', dateOptions)}
              </span>
            </div>
          </div>
        </div>
        <div className="contract_item__summary__action">
          <div
            className="contract_item__summary__action__button contract_item__summary__action__button--info"
            role="button"
          >
            <span className="contract_item__summary__action__button__icon">
              <FontAwesomeIcon icon={faCircleInfo} size="1x" fixedWidth />
            </span>
            <span className="contract_item__summary__action__button__text">Xem Chi tiết</span>
          </div>
          <div
            className="contract_item__summary__action__button contract_item__summary__action__button--cancel"
            role="button"
          >
            <span className="contract_item__summary__action__button__icon">
              <FontAwesomeIcon icon={faCircleMinus} size="1x" fixedWidth />
            </span>
            <span className="contract_item__summary__action__button__text">Hủy hợp đồng</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ContractFooter = () => {
  const dispatch = useAppDispatch();
  const page: number = useSelector(contractPagingSelector);
  const updatePage = (page: number, pageSize: number) => {
    dispatch(contractAction.changePage(page));
  };
  return (
    <div>
      <Pagination pageSize={10} onChange={updatePage} current={page} total={10} />
    </div>
  );
};

export const ContractPage = () => {
  const [showDetail, setShowDetail] = useState<boolean>(false);
  const [contracts, setContracts] = useState<ITreamtentContract[]>([]);
  const [selectedContracts, setSelectedContracts] = useState<ITreamtentContract>(contracts[0]);
  const history = useHistory()
  const location = useLocation<any>()
  const popUpDetail = (contract: ITreamtentContract) => {
    let state = location.state;
    history.push('/doctor/contract/detail', {
      ...state,
      contract: contract
    })
    // setShowDetail(true);
    // setSelectedContracts(contract);
  };

  const initPatient: IPatient = {
    avatar: '/logo_app.jpg',
    firstName: 'John',
    lastName: 'Doe',
    address: '23 Khieu Nang',
    gender: 'male',
    id: 1,
  };

  const doctor = {
    firstName: localStorage.getItem('firstName_data'),
    lastName: localStorage.getItem('lastName_data'),
    avatar: localStorage.getItem('avatar_data'),
  };

  const handleReload = (contractList: ITreamtentContract[]) => {
    setContracts(contractList);
  };

  return showDetail ? (
    <ContractInfo
      // patient={initPatient}
      // prescription={[]}
      // instructions={[]}
      contract={selectedContracts}
    />
  ) : (
    <div className="contract">
      <div className="contract__header">
        <ContractFilter reload={handleReload}></ContractFilter>
      </div>
      <div className="contract__body">
        {contracts.map((contract) => {
          return (
            <div
              onClick={(e) => {
                popUpDetail(contract);
              }}
            >
              <ContractItem contract={contract} />
            </div>
          );
        })}
      </div>
      <div className="contract__footer">
        <ContractFooter></ContractFooter>
      </div>
    </div>
  );
};
