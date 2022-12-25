import { faCalendarDay } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { ITreatmentSession } from 'models/contract';
import '../style/schedules.scss';

export const ContractScheduleItem = (props: { session: ITreatmentSession }) => {
    return <div className="timetable_item">
        <div className='dateTime'></div>
        <div></div>
    </div>
}



export const ContractSchedule = () => {
    let initItem: ITreatmentSession = {
        date: '2022-12-09',
        status: 'active',
        assessment: [],
        note: [],
        cancelReason: '',
        checkInCode: '',
        end: '',
        start: '',
        id: 1,
        isDoctorCancelled: false,
        isSupervisorCancelled: false,
        isSystemCancelled: false,
    }
    return (
        <div className="contract_schedule">
            <div className="contract_schedule__adjustment">

            </div>
            <div className="contract_schedule__table">
                <div className='row'>
                    <ContractScheduleItem session={initItem} />
                </div>
                <div className='row'>
                    <ContractScheduleItem session={initItem} />
                </div>
                <div className='row'>
                    <ContractScheduleItem session={initItem} />
                </div>
                <div className='row'>
                    <ContractScheduleItem session={initItem} />
                </div>
                <div className='row'>
                    <ContractScheduleItem session={initItem} />
                </div>
            </div>
        </div>
    )
}