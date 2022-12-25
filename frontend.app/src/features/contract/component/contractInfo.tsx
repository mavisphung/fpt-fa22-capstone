import {faCakeCandles, faCalendarDay, faVenusMars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IPatient } from "models/patient";
import { dob, shortDate } from "constants/ConstValue";
import { ContractStatusMap, Gender } from "constants/Enum";
import { ITreamtentContract, ITreatmentSession } from "models/contract";
import '../style/contract_detail.scss';
import { useEffect, useState } from "react";
import { listContractSession } from "api/sessionApi";
import { ContractStatus } from "models/enum";
import { listPrescription } from "api/prescriptionApi";
import { HealthRecord, IPrescription2, IMedicalInstruction } from 'models/health_record';
import { useHistory, useLocation } from "react-router-dom";
import { MedicalInstructionDetailModal, PrescriptionDetailModal, PrescriptionCreatorprescription, MedicalInstructionDetailCreatorModal } from "./modal";
import { SessionForm } from "./form/session_form";
import { SessionDetailViewOnly } from "./modal/session_detail";
import { HealthRecordSharedDoccument } from "./healthRecord/healthRecord";
import { ApprovalModal } from "./modal/approve_modal";
import { cancelContract, reloadContract } from "api/contract_api";
import { CancelContractModal } from "./modal/cancelModal";
import moment from "moment";
export const PaitentInfoTab = (props: { patient: IPatient, supervisor: ITreamtentContract }) => {
    return (
        <div className="tab">
            <div className="contract_short_info">
                <span className="icon"><FontAwesomeIcon icon={faCakeCandles} /> Ngày sinh</span>
                <span className="text">{(props.patient.dob as Date).toLocaleDateString('vi-VI', dob)}</span>
            </div>
            <div className="contract_short_info">
                <span className="icon"><FontAwesomeIcon icon={faVenusMars} /> Giới tính</span>
                <span className="text">{props.patient.gender}</span>
            </div>
            <div className="contract_short_info">
                <span className="icon">Giám hộ</span>
                <span className="text">{props.supervisor.supervisor.lastName.concat(' ', props.supervisor.supervisor.firstName)}</span>
            </div>
            <div className="contract_short_info">
                <span className="icon">Địa chỉ:</span>
                <span className="text">{props.patient.address}</span>
            </div>
            <div className="contract_short_info">
                <span className="icon"></span>
                <span className="text"></span>
            </div>
        </div>
    )
}

export const TreatmentSessionScheduleTab = (props: { sessions: ITreatmentSession }) => {

    return (
        <div className="tab_displayer__content">
            <div className="new_section">
                <button className="newSessionBtn">Thêm buổi đánh giá</button>
            </div>
            <div className="session">
                <div className="session__datetime">
                    <div className="wrapper_centerVer">
                        <h5>{new Date(props.sessions.date).toLocaleDateString('vi-VI', shortDate)}</h5>
                        <h6>{`${props.sessions?.start} - ${props.sessions?.end}`}</h6>
                    </div>
                </div>
                <div className="divider--small"></div>
                <div className="session__note_assetment">
                    <div className="assetment_container">
                        <div className="wrapper_centerVer wrapper_centerHorizontal">
                            <h5 className="title">Đánh giá</h5>
                            <h6 className="content">Chưa có đánh giá từ bác sĩ</h6>
                        </div>
                    </div>
                </div>
                <div className="divider--small"></div>
                <div className="session__note_assetment">
                    <div className="note_container">
                        <div className="wrapper_centerVer wrapper_centerHorizontal">
                            <h5 className="title">Chú thích</h5>
                            <h6 className="content">Chưa có chú thích</h6>
                        </div>
                    </div>
                </div>
                <div className="divider--small"></div>
                <div className="session__note_assetment session__note_assetment--small">
                    <div className="note_container">
                        <div className="wrapper_centerVer wrapper_centerHorizontal">
                            <button>Hủy bỏ</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}


export const MedicalInstruction = (props: { instruction: IMedicalInstruction[], contract: ITreamtentContract, onModal: (instruction: any) => void, onNewModal: () => void }) => {
    console.log(`instruction: ${props.instruction}`)
    const history = useHistory()
    return <div className="tab_displayer__content">
        <div className="tab_title">
            <h5>Y lệnh</h5>
        </div>
        <div className="new_section">
            <button className="newSessionBtn" onClick={e => props.onNewModal()} disabled={
                props.contract.status.toLocaleLowerCase() !== ContractStatus.IN_PROGRESS.replaceAll(' ', '_').toLocaleLowerCase()
            }>Thêm y lệnh</button>
        </div>
        <div className="instruction">
            {
                props.instruction && props.instruction.length > 0 ?
                    props.instruction.map(p => {
                        console.log('note', p)
                        let requirements = p.requirments.replaceAll("\"", "")
                        let isUrl = requirements.startsWith("http") || requirements.startsWith("https")
                        return <div className="instruction_item" onClick={e => { props.onModal(p) }}>
                            <div className="instruction_item_date">
                                <h6>{p.category}</h6>
                                <h6>Ngày tạo: {new Date(p.createdAt).toLocaleDateString('vi-Vi', dob)}</h6>
                            </div>
                            <div className="divider--small"></div>
                            <div className="instruction_item_note">
                                <h6>Yêu cầu y lệnh</h6>
                                {/* {p.requirements !== undefined ? p.requirements.map(r => <p>r</p>):<p>Không có yêu c</p>} */}
                                <p>{p.requirments !== undefined ? (isUrl? requirements : p.requirments) : 'Không có yêu cầu'}</p>
                            </div>
                            <div className="divider--small"></div>
                            <div className="actions">
                                {
                                    p.submissions === '' ? <p>Chưa có kết quả</p> : <p className="btnDetail" onClick={e => {

                                    }}>Xem chi tiết</p>
                                }
                            </div>
                        </div>
                    }) : <p>Chưa có y lệnh ghi nhận</p>
            }
        </div>
    </div>

}

export const TreatmentHealthRecord = (props: { record: HealthRecord, contract: ITreamtentContract, prescriptions: IPrescription2[], onModal: (selectedPrescription: any) => void, onCreateModal: () => void }) => {
    console.log('131', props.contract, props.contract.status !== 'IN_PROGRESS')
    const history = useHistory()
    return (
        <div className="tab_displayer__content">
            <div className="tab_title">
                <h5>Đơn thuốc đã kê</h5>
            </div>
            <div className="new_section">
                <button className="newSessionBtn" onClick={e => { props.onCreateModal() }} disabled={props.contract.status.toLocaleLowerCase() !== ContractStatus.IN_PROGRESS.replaceAll(' ', '_').toLocaleLowerCase()}>Thêm đơn thuốc</button>
            </div>
            <div className="prescriptions">
                {
                   props.prescriptions && props.prescriptions.length > 0 && props.prescriptions.map(p => {
                        return <div className="prescriptions_item">
                            <div className="prescriptions_item_date">
                                <h6>Ngày bắt đầu: {new Date(p.toDate).toLocaleDateString('vi-Vi', dob)}</h6>
                                <h6>Ngày kết thúc: {moment(p.toDate).isValid()? moment(p.toDate).format('dd/MM/yyyy') :""}</h6>
                            </div>
                            <div className="divider-small"></div>
                            <div className="prescriptions_item_note">
                                <h6>Chú thích</h6>
                                <p>{(p.note !== undefined && p!.note.length > 0) ? p.note[0] : 'Không có chú thích'}</p>
                            </div>
                            <div className="divider--small"></div>
                            <div className="actions">
                                <p className="btnDetail" onClick={e => {
                                    props.onModal(p)
                                }}>Xem chi tiết</p>
                            </div>
                        </div>
                    })
                }
            </div>
        </div>
    )
}

var initItem: ITreatmentSession = {
    date: '2022-12-09',
    status: 'active',
    assessment: [],
    note: [],
    cancelReason: '',
    checkInCode: '',
    end: '19:00',
    start: '18:30',
    id: 1,
    isDoctorCancelled: false,
    isSupervisorCancelled: false,
    isSystemCancelled: false,
}


export const ContractInfo = (props: { contract: ITreamtentContract }) => {
    const [contract, setContract] = useState(props.contract)
    const [patient, setPatient] = useState(contract.patient)
    const [sessions, setSession] = useState<ITreatmentSession[]>([])
    const [prescription, setPrescription] = useState<IPrescription2[]>([])
    const [selectedInstruction, setSelectedInstruction] = useState<any>()
    const [selectedSession, setSelectedSession] = useState<any>()
    const [selectedPrescription, setSelectedPrescription] = useState<any>()
    const [onCreatePrescription, setOnCreatedPrescrtion] = useState<boolean>(false)
    const [onCreateInstruction, setOnCreatedInstruction] = useState<boolean>(false)
    const [onApproval, setOnApproval] = useState<boolean>(false)
    const [onCancelContract, setOnCancelContract] = useState<boolean>(false)
    const [tab, setTab] = useState('medicalRecord')
    const [rerender, setRerender] = useState(0);
    let endDate = contract.endedAt === undefined || contract.endedAt === null ? 'Chưa có thông tin'
        : new Date(contract.endedAt).toLocaleDateString('vi-VI', dob)
    useEffect(() => {
        console.log('id ', contract.healthRecord)
        async function init() {
            let sessions
            try {
                sessions = await (await listContractSession(contract.id)).data.data;
            } catch (e) {
                console.log('error', e)
            }
            let prescriptions = await (await listPrescription(contract.healthRecord[0].recordId)).data.data
            if (sessions && sessions.length !== undefined) {
                setSession(sessions)
            }
            if (prescriptions) {
                setPrescription(prescriptions)
            }
            console.log('prescriptions', prescriptions)
            console.log('sessions', sessions)
        }
        init()
    }, [contract])

    useEffect(() => {
        if (rerender === 0){
            return;
        }
        async function init() {
            let sessions
            try {
                sessions = await (await listContractSession(contract.id)).data.data;
            } catch (e) {
                console.log('error', e)
            }
            let prescriptions = await (await listPrescription(contract.healthRecord[0].recordId)).data.data
            if (sessions && sessions.length !== undefined) {
                setSession(sessions)
            }
            if (prescriptions) {
                setPrescription(prescriptions)
            }
           try {
               let contract:ITreamtentContract =  await (await reloadContract(props.contract.id)).data.data
               console.log('contract rerender', contract);
               setContract(contract);
           } catch (error) {
                console.log('error', error);
           }
        }
        init()
    }, [rerender])

    const handleOnTabClick = (item: string) => {
        setTab(item);
    }

    const handleOnInstructionClick = (instruction: any) => {
        setSelectedInstruction(instruction);
    }

    const closeInstructionMode = () => {
        setSelectedInstruction(undefined);
    }

    const handlePrescriptionClick = (instruction: any) => {
        setSelectedPrescription(instruction);
    }

    const closePrescriptionModal = () => {
        setSelectedPrescription(undefined);
    }

    const handleAddNewPrescriptionToggle = () => {
        setOnCreatedPrescrtion(!onCreatePrescription);
    }

    const handleSessionClick = (session : any) => {
        setSelectedSession(session);
    }
    const handleSessionClose = () => {
        setSelectedSession(undefined);
    }

    const handleOnApproval = () => {
        setOnApproval(true);
    }

    const handleCloseApproval = () => {
        setOnApproval(false);
    }

    const handleOpenCreateInstruction =  () => {
        setOnCreatedInstruction(true);
    }

    const handleCloseCreateInstruction =  () => {
        setOnCreatedInstruction(false);
    }

    const handleCancelContract =  async (reason: any) => {
        cancelContract(contract.id, reason).then(res => {
            setRerender(rerender + 1);
        }).catch(e => {
            console.log(e);
        })
    }

    return (
        <div className="page_detail">
            <div className="main">
                <div className="patient">
                    <div className="avatar_side">
                        <div className="avatar">
                            <img src={contract.patient.avatar} className='circle_img'></img>
                            <div className="fullname">
                                <p>{contract.patient.lastName.concat(' ', contract.patient.firstName)}</p>
                            </div>
                        </div>
                        <div className="contract_detail_long">
                            <p className="align_center">{contract.patient.address}</p>
                        </div>
                        <div className="contract_actions">
                            {
                                contract.status.toLowerCase() === ContractStatus.PENDING.toLowerCase() ?
                                    <>
                                        <button className="acceptButton" onClick={e => handleOnApproval()}>Chấp thuận</button>
                                        <button className="rejectButton" onClick={e => {setOnCancelContract(true)}}>Từ chối</button>
                                    </> : <></>
                            }
                            {
                                contract.status === ContractStatus.IN_PROGRESS ? <button className="fullContainerWidth"  onClick={e => {setOnCancelContract(true)}}>Hủy hợp đồng</button> : <></>
                            }
                            {
                                contract.status.toLowerCase() === ContractStatus.APPROVED.toLowerCase() ? <button className="fullContainerWidth" onClick={e => {setOnCancelContract(true)}}>Hủy hợp đồng</button> : <></>
                            }

                        </div>
                    </div>
                    <div className="divider">
                    </div>
                    <div className="patient_summary">
                        <div className="contract_detail_short">
                            <span className="icon">Giới tính:</span>
                            <span className="text">{contract.patient.gender !== undefined ? Gender.get(contract.patient.gender) : 'Chưa có thông tin'}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Ngày sinh:</span>
                            <span className="text">{contract.patient.dob !== undefined ? (new Date(contract.patient.dob)).toLocaleDateString('vi-VI', dob) : 'Không có thông tin'}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Giám hộ:</span>
                            <span className="text">{contract.supervisor.lastName.concat(' ', contract.supervisor.firstName)}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Dịch vụ:</span>
                            <span className="text">{contract.service.name}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Trạng thái hợp đồng:</span>
                            <span className="text">{ContractStatusMap.get(contract.status.toUpperCase())}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Ngày bắt đầu hợp đồng:</span>
                            <span className="text">{(new Date(contract.startedAt).toLocaleDateString('vi-VI', dob))}</span>
                        </div>
                        <div className="contract_detail_short">
                            <span className="icon">Ngày kết thúc hợp đồng:</span>
                            <span className="text">{moment(contract.endedAt).isValid() ?moment(contract.endedAt).format('LLLL'):""}</span>
                        </div>
                    </div>
                </div>
                <div className="tab">
                    <div className="tab_selection">
                        <div className={`tab_item ${tab == 'medicalRecord' ? 'tab_item--active' : ''}`} onClick={e => handleOnTabClick('medicalRecord')}>
                            <p>Đơn thuốc</p>
                        </div>
                        <div className={`tab_item ${tab == 'session' ? 'tab_item--active' : ''}`} onClick={e => handleOnTabClick('session')}>
                            <p>Y lệnh</p>
                        </div>
                        <div className={`tab_item ${tab == 'personal_medical_history' ? 'tab_item--active' : ''}`} onClick={e => handleOnTabClick('personal_medical_history')}>
                            <p>Bệnh lý yêu cầu</p>
                        </div>
                    </div>
                    <div className="tab_displayer">
                        {
                            tab === 'medicalRecord' ? prescription && <TreatmentHealthRecord contract={contract} record={contract.healthRecord[0]} prescriptions={prescription} onModal={handlePrescriptionClick} onCreateModal={handleAddNewPrescriptionToggle}></TreatmentHealthRecord>:<></>
                        }
                        {
                             tab === 'session' ? <MedicalInstruction instruction={contract.healthRecord[0].detail.instructions} onModal={handleOnInstructionClick} onNewModal={handleOpenCreateInstruction} contract={contract}></MedicalInstruction>:<></>
                        }
                        {
                             tab === 'personal_medical_history' ? <HealthRecordSharedDoccument healthRecord={contract.healthRecord[0]}/>:<></>
                        }
                    </div>
                </div>
            </div>
            <div className="side">
                <div className="session_list">
                    <div className="session_list_header">
                        <div className="session_list_header_item">
                            <h6>Lịch theo dõi đánh giá/điều trị</h6>
                        </div>
                    </div>
                    <div className="session_list_content">
                        {sessions.map(s => <div className="session_list_content_item">
                            <div className="session_list_content_item_label">
                                <div className="wrapper">
                                    <FontAwesomeIcon icon={faCalendarDay} fixedWidth size="2x" />
                                </div>
                            </div>
                            <div className="divider--small"></div>
                            <div className="session_list_content_item_detail">
                                <div className="datetime">
                                    <p>
                                        Ngày: {new Date(s.date).toLocaleDateString('vi-VI', dob)}
                                    </p>
                                    <p>Thời gian: {s.start.slice(10).concat(' - ', s.end.slice(11))}</p>
                                </div>
                                <div className="action">
                                    <span className="btnSpan" onClick={e => handleSessionClick(s)}>Chi tiết</span>
                                </div>
                            </div>
                        </div>
                        )}
                    </div>
                </div>
                <SessionForm contract={contract}/>
            </div>
            {
                selectedInstruction ? <MedicalInstructionDetailModal  instruction={selectedInstruction} onClose={closeInstructionMode} rerender = {() => {setRerender(rerender + 1)}}></MedicalInstructionDetailModal> : <></>
            }
            {
                onCreateInstruction ? <MedicalInstructionDetailCreatorModal onClose={handleCloseCreateInstruction}/> : <></>
            }
            {
                selectedPrescription ? <PrescriptionDetailModal contract={contract} prescription={selectedPrescription.id} close={closePrescriptionModal}></PrescriptionDetailModal> : <></>
            }
            {
                onCreatePrescription ? <PrescriptionCreatorprescription onClose={handleAddNewPrescriptionToggle} healthRecord = {contract.healthRecord[0]}></PrescriptionCreatorprescription> : <></>
            }
            {
                selectedSession ? <SessionDetailViewOnly onClose={handleSessionClose} session = {selectedSession}/> : <></>
            }
            {
                onApproval? <ApprovalModal contract={contract} close={handleCloseApproval} rerender = {() => {setRerender(rerender + 1)}}/>:<></>
            }

            {
                onCancelContract? <CancelContractModal onSubmit={handleCancelContract} onClose={() => {setOnCancelContract(true)}}/>:<></>
            }   
        </div>
    )
}


export const ContractInfoWrapper = () => {
    const location = useLocation<any>();
    const [contract, setContract] = useState<ITreamtentContract>()
    useEffect(() => {
        setContract(location.state.contract)
    }, [location.state])
    return contract ? <ContractInfo contract={contract}></ContractInfo> : <></>
}