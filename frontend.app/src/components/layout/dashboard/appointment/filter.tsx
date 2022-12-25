import { useAppDispatch } from "app/hooks"
import { CustomDatePicker } from "components/common/DatetimePicker";
import { AppointmentStatusDropDown } from "components/common/dropdown";
import { appointmentAction, AppointmentFilterSelector } from "features/appointment/appointmentSlice";
import { AppointmentStatus } from "models/appointment";
import { useSelector } from "react-redux";
import './appointment_filter.scss'
export const AppointmentFilter = () => {
    const dispatch = useAppDispatch();
    const filter = useSelector(AppointmentFilterSelector);

    const handleChangeDate = (newDate:string, comparator:string)=>{
        let newFilter = Object.assign({},filter);
        if(comparator ==='gte'){
            newFilter.bookedAt__gte = newDate;
        }else{
            newFilter.bookedAt__lte = newDate;
        }
        dispatch(appointmentAction.loadFilter(newFilter));
    }

    const handleChangeStatus = (newStatus:string)=>{
        console.log('new status: ', newStatus);
        let status = newStatus as AppointmentStatus; 
        let newFilter = Object.assign({},filter);
        newFilter.status = status;
        dispatch(appointmentAction.loadFilter(newFilter));
    }

    return (
        <div id="filter">
            <AppointmentStatusDropDown option={AppointmentStatus.PENDING} handleChange = {handleChangeStatus}/>
            <CustomDatePicker changeDate ={handleChangeDate} selectedDate={filter.bookedAt__gte.toLocaleString()} comparator='gte'></CustomDatePicker>
            <CustomDatePicker changeDate = {handleChangeDate} comparator="lte" selectedDate ={filter.bookedAt__lte.toLocaleString()}></CustomDatePicker>
        </div>
    )
}