import { dob } from "constants/ConstValue"
import { ITreatmentSession } from "models/contract"
import '../../style/session_detail.scss'
import { useState, ChangeEvent } from 'react'
import { cancelContractSession } from "api/sessionApi"

export const SuccessModal = (props: { category: string, title: string, messages: any, close: () => void }) => {
    return (
        <div className="modal_success_wrapper">
            <div className="modal_success_modal">
                <div className="modal_success_modal_header">
                    <h6 className="modal_success_modal_header_title">Xác nhận hủy phiên theo dõi - đánh giá - điều trị</h6>
                </div>
                <div className="horizontal_divider"></div>
                <div className="modal_success_modal_footer">
                    <button className="modal_success_modal_close" onClick={e => props.close()}>Đóng</button>
                </div>
            </div>
        </div>)
}

export const SessionCancelConfirmModal = (props: { session: ITreatmentSession, onClose: () => void }) => {
    const [cancelReason, setCancelReason] = useState<any>()
    const asyncHandleCancelAction = async () => {
        console.log(cancelReason);
        await cancelContractSession({ id: props.session.id, cancelReason: cancelReason }).then(res => {

        }).catch(e => {
            console.error(e);
        })
    }
    const handleCancelReasonChange = (e: ChangeEvent<HTMLInputElement>) => {
        console.log('cancel reason ', e.currentTarget.value);
        setCancelReason(e.currentTarget.value)
    }
    return (
        <div className="modal_wrapper">
            <div className="cancel_session_modal">
                <div className="cancel_session_modal_header">
                    <h6 className="cancel_session_modal_header_title">Xác nhận hủy phiên theo dõi - đánh giá - điều trị</h6>
                </div>
                <div className="horizontal_divider"></div>
                <div className="cancel_session_modal_content">
                    <div><p>Lí do Hủy</p></div>
                    <input className="cancelReason_input" onChange={e => handleCancelReasonChange(e)} />
                </div>
                <div className="horizontal_divider"></div>

                <div className="cancel_session_modal_footer">
                    <button className="cancel_session_modal_footer_confirm" onClick={e => asyncHandleCancelAction()}>Xác nhận</button>
                    <button className="cancel_session_modal_footer_close" onClick={e => props.onClose()}>Đóng</button>
                </div>
            </div>
        </div>
    )
}

export const SessionDetailViewOnly = (props: {
    session: ITreatmentSession,
    onClose: () => void
    onCancel?: (session: any) => void
}) => {
    const [openModal, setOpenModal] = useState(false);

    const handleOpenModaL = () => {
        setOpenModal(true);
    }

    const handleCloseModal = () => {
        setOpenModal(false);
    }
    return (
        <div className="session_modal_wrapper">
            <div className="session_modal">
                <div className="session_modal_header">
                    <h5 className="session_modal_header_title">Chi tiết buổi theo dõi - điều trị - đánh giá</h5>
                </div>
                <div className="horizontal_divider"></div>
                <div className="session_modal_content">
                    <div className="session_modal_content_datetime">
                        <div className="session_modal_content_datetime_item">
                            <h6 className="title">Ngày tiến hành</h6>
                            <p className="no_padding">{new Date(props.session.date).toLocaleDateString('vi-VI', dob)}</p>
                        </div>
                        <div className="session_modal_content_datetime_item">
                            <h6>Khung giờ thực hiện</h6>
                            <p className="no_padding">{props.session.start.slice(10)} - {props.session.end.slice(10)}</p>
                        </div>
                    </div>
                    <div className="session_modal_content_note">
                        <h6 className="title">Chú thích</h6>
                        <div className="session_modal_content_note_value">
                            <ul>
                                {

                                    props.session.note !== undefined && props.session.note.length > 0 ? props.session.note.map(n => {
                                        return <li className="no_padding">{n}</li>
                                    }) : <p className="no_padding">{'Không có chú thích'}</p>

                                }  
                            </ul>
                        </div>
                    </div>
                    <div className="session_model_content_assessment">
                        <h6>Đánh giá của bác sĩ</h6>
                        <div className="session_model_content_assessment_value">

                            {
                                props.session.assessment !== undefined && props.session.assessment.length > 0 ? props.session.assessment.map(a => {
                                    return <p className="no_padding">{"Đánh giá số 1"}</p>
                                }) : <p className="no_padding">{"Chưa có đánh giá"}</p>
                            }
                        </div>
                    </div>
                </div>
                <div className="horizontal_divider"></div>
                <div className="session_modal_footer">
                    {
                        props.session.status.toLocaleLowerCase() === 'PENDING'.toLowerCase() ? <button className="btnSessionClose" onClick={e => handleOpenModaL()}>Hủy</button> : <></>
                    }
                    <button className="btnSessionClose" onClick={e => props.onClose()}>Đóng</button>
                </div>
            </div>
            {
                openModal === true ? <SessionCancelConfirmModal session={props.session} onClose={handleCloseModal} /> : <></>
            }
        </div>
    )
}