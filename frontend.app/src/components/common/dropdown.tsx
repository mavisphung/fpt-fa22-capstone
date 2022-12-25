import React, { useState } from "react";
import classes from './dropdown.module.scss'
import { IonIcon } from "react-ion-icon";
import { AppointmentStatus } from "models/appointment";
import { AppointmentFilterSelector } from "features/appointment/appointmentSlice";
export const AppointmentStatusDropDown: React.FC<{ option: AppointmentStatus, handleChange: (status:string) => void }> = (props: {
    option: AppointmentStatus, handleChange: (status:string) => void
}) => {
    const [hover, setHover] = useState<boolean>(false)
    const [selected, setSelected] = useState('ALL');
    const selector = AppointmentFilterSelector
    const handleSelected = () => {
        setHover(!hover)
    }

    const handleChooseOption = (status: string) => {
        setSelected(status);
        props.handleChange(status);
    }

    return (
        <div className={classes.box} onClick={handleSelected}>
            <div className={classes.box__selection}>
                <div className={classes.box__selection__result}>
                    <p>{selected}</p>
                </div>
                <div className={classes.box__selection__icon}>
                    <div className={classes.box__selection__icon__wrapper}>
                        <IonIcon name="chevron-down" size="16" />
                    </div>
                </div>
            </div>
            {!hover ? <></> :
                < div className={classes.box__selector}>
                    {
                        Object.keys(AppointmentStatus).map((label) => {
                            return <div className={classes.box__selector__option} onClick={()=>handleChooseOption(label)}>
                                <p>{label}</p>
                            </div>
                        })
                    }
                </div>
            }
        </div >
    )
}