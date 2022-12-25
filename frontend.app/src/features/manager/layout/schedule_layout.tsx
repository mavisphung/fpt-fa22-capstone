import {faBedPulse, faCheckCircle, faClock, faClose, faUserGroup } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import '../style/component.scss';

export interface ScheduleProps {
    month_of_year: number;
    day_of_week: number;

}

export const ScheduleCard = () => {
    return (
        <div className='card'>
            <div className='card__wrapper'>
                <div className='card__wrapper__label'>
                    <div className='card__wrapper__label__wrapper'>
                        <span>Đang chờ</span>
                    </div>
                </div>
                <div className='header'>
                    <h5><FontAwesomeIcon icon={faBedPulse} size={'1x'} fixedWidth /> Hoang Thanh Phong</h5>
                    <h6>Giám hộ Phong Hoang</h6>
                </div>
                <div className='body'>
                    <div className='body__row'>
                        <span className='icon'><FontAwesomeIcon icon={faClock} size='1x' fixedWidth></FontAwesomeIcon></span>
                        <div className='content'>
                            <span>9:30 - 11:30</span>
                        </div>
                    </div>
                    <div className='body__row'>
                        <span className='icon'><FontAwesomeIcon icon={faUserGroup} size='1x' fixedWidth></FontAwesomeIcon></span>
                        <div className='content content--fit_content'>
                            <span>Online</span>
                        </div>
                    </div>
                </div>
                <div className='footer'>
                    <div className='action'>
                        <div role='button' className='button'>
                            <span className='button__icon'><FontAwesomeIcon icon={faCheckCircle} size='1x' fixedWidth></FontAwesomeIcon></span>
                            <span className='button__text'>Checkin</span>
                        </div>
                        <div role='button' className='button'>
                            <span className='button__icon'><FontAwesomeIcon icon={faClose} size='1x' fixedWidth></FontAwesomeIcon></span>
                            <span className='button__text'>Cancel</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export const Schedule = () => {
    return (
        <ScheduleCard></ScheduleCard>
    )
}