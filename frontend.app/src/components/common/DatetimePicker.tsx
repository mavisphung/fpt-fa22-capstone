import { useAppDispatch } from "app/hooks"
import { appointmentAction } from "features/appointment/appointmentSlice"
import classes from '../common/dropdown.module.scss'
import ReactDatePicker, {registerLocale} from "react-datepicker";
import { forwardRef, useRef } from "react";
import React from "react";
import { IonIcon } from "react-ion-icon";
import vi from 'date-fns/locale/vi';
registerLocale('vi',vi);
export const CustomDatePicker = (props: {
    comparator: string,
    selectedDate: string,
    changeDate: (newDate:string, comparator:string) => void
}) => {
    const ExampleCustomInput = forwardRef<HTMLDivElement, React.HTMLProps<HTMLDivElement>>(({ value, onClick }, ref: React.Ref<HTMLDivElement>) => (
        <div className={classes.input_cotainer} onClick={onClick} ref={ref}>
            <div className={classes.input_cotainer__value}><p>{value}</p></div>
            <div className={classes.input_cotainer__icon}>
                <div className={classes.input_cotainer__icon__wrapper}>
                    <IonIcon name="calendar"></IonIcon>
                </div>
            </div>
        </div>
    ));
    const picker = useRef(null);
    const dispatch = useAppDispatch()
    const handleChangeDate = (date: Date) => {
        console.log('date to change', date);
        props.changeDate(date.toISOString(), props.comparator);
    }


    return (
        <div className={classes.wrapper}>
            <ReactDatePicker
                ref={picker}
                locale={'vi'}
                className={classes.wrapper__picker}
                showMonthDropdown
                showYearDropdown
                minDate={new Date('2000-12-12')}
                maxDate={new Date('2222-12-12')}
                selected={new Date(props.selectedDate)}
                onChange={handleChangeDate}
                customInput={<ExampleCustomInput />}
                dateFormat='dd/MM/yyyy' />
        </div>

    )
}

