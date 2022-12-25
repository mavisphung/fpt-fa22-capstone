import { IAppointment} from "models/appointment";
import {IPatient} from 'models/patient'
import './appointment_detail.scss'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCakeCandles, faCalendarAlt, faDollyBox, faFileWaveform, faHandshakeAlt, faMarsAndVenus, faMessage, faPhone, faPhoneAlt, faVideoCamera } from '@fortawesome/free-solid-svg-icons'
export interface AppointmentDetailProps {
    patient?: IPatient;
    appointment: IAppointment;
}

export const AppointmentDetail = (props: AppointmentDetailProps) => {
    return (
        <div className="modal_container">
            <div className="modal">
                <div className="modal__card">
                    <div className="modal__card__header">
                        <img src="https://images.unsplash.com/photo-1549068106-b024baf5062d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80"
                            className="modal__card__header__avatar"></img>
                        <div className="modal__card__header__name">
                            <h2>{props.patient?.firstName + ' ' + props.patient?.lastName}</h2>
                        </div>
                    </div>
                    <div className="modal__card__text">
                        <div className="modal__card__text__line">
                            <div className="modal__card__text__line__label">
                                <FontAwesomeIcon icon={faCakeCandles} size='lg' fixedWidth />
                                <h3>Ngày sinh:</h3>
                            </div>
                            <div className="modal__card__text__line__content">
                                <p>{props.patient?.dob !== null ? props.patient!.dob?.toLocaleString():''}</p>
                            </div>
                        </div>
                        <div className="modal__card__text__line">
                            <div className="modal__card__text__line__label">
                                <FontAwesomeIcon icon={faMarsAndVenus} size='lg' fixedWidth />
                                <h3>Giới tính:</h3>
                            </div>
                            <div className="modal__card__text__line__content">
                                <p>{'MALE'}</p>
                            </div>
                        </div>
                    </div>
                    <div className="modal__card__control">
                        <button id='remote_call' className="modal__card__control__action">
                            <FontAwesomeIcon icon={faPhone} />
                        </button>
                        <button id='' className="modal__card__control__action">
                            <FontAwesomeIcon icon={faMessage} />
                        </button>
                    </div>
                </div>
                <div className="modal__appointment">
                    <div className="modal__appointment__header">
                        <h2>Thông tin cuộc hẹn</h2>
                    </div>
                    <div className="modal__appointment__content">
                        <div className="modal__appointment__content__line">
                            <div className="modal__appointment__content__line__label">
                                <FontAwesomeIcon icon={faCalendarAlt} size='lg' fixedWidth />
                                <h3>Ngày hẹn</h3>
                            </div>
                            <div className="modal__appointment__content__line__content">
                                <p>{new Date(''+props.appointment.bookedAt.toLocaleString()).toLocaleDateString('en-GB', { timeZone: 'UTC' }).slice(0,10)}</p>
                            </div>
                        </div>
                        <div className="modal__appointment__content__line">
                            <div className="modal__appointment__content__line__label">
                                <FontAwesomeIcon icon={faHandshakeAlt} size='lg' fixedWidth />
                                <h3>Hình thức gặp mặt</h3>
                            </div>
                            <div className="modal__appointment__content__line__content">
                                <p>Gặp mặt trực tiếp</p>
                            </div>
                        </div>
                        <div className="modal__appointment__content__line">
                            <div className="modal__appointment__content__line__label">
                                <FontAwesomeIcon icon={faFileWaveform} size='lg' fixedWidth />
                                <h3>Trạng thái</h3>
                            </div>
                            <div className="modal__appointment__content__line__content">
                                <p>Đã hoàn tất</p>
                            </div>
                        </div>
                        <div className="modal__appointment__content__line">
                            <div className="modal__appointment__content__line__label">
                                <FontAwesomeIcon icon={faFileWaveform} size='lg' fixedWidth />
                                <h3>Triệu chứng từ người bệnh</h3>
                            </div>
                            <div className="modal__appointment__content__line__content">
                                <p>Bắt chân sưng phù, căng cứng liên tục, đi lại khó khăn</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}