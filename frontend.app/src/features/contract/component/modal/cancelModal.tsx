import { ChangeEvent, useState } from "react";
import '../../style/session_detail.scss'
export const CancelContractModal = (props: {onSubmit: (reason: any) => void, onClose: () => void }) => {
    const [cancelReason, setCancelReason] = useState<any>()
    const asyncHandleCancelAction = async () => {
        props.onSubmit(cancelReason)
    }
    const handleCancelReasonChange = (e: ChangeEvent<HTMLInputElement>) => {
        console.log('cancel reason ', e.currentTarget.value);
        setCancelReason(e.currentTarget.value)
    }
    return (
        <div className="modal_wrapper">
            <div className="cancel_session_modal">
                <div className="cancel_session_modal_header">
                    <h6 className="cancel_session_modal_header_title">Xác nhận hủy hợp đồng</h6>
                </div>
                <div className="horizontal_divider"></div>
                <div className="cancel_session_modal_content">
                    <div><p>Lí do Hủy</p></div>
                    <input className="cancelReason_input" onChange={e => handleCancelReasonChange(e)} />
                </div>
                <div className="horizontal_divider"></div>
                <div className="cancel_session_modal_footer">
                    <button className="cancel_session_modal_footer_confirm" onClick={e => asyncHandleCancelAction()}>Hủy</button>
                    <button className="cancel_session_modal_footer_close" onClick={e => props.onClose()}>Đóng</button>
                </div>
            </div>
        </div>
    )
}