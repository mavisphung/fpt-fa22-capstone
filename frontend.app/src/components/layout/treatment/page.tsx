import { faCakeCandles, faCalendarCheck, faCalendarDay, faFile, faFileMedical, faFileWaveform, faFolderMinus, faFolderPlus, faHome, faPerson, faPersonDotsFromLine, faPills, faPlus, faStethoscope, faUser, faVenusMars } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { IPatient } from "models/patient"
import { IMedicalInstruction, IPrescription, PatientMedicalHistory } from "models/health_record"
import { useState } from "react"
import "./page.scss"


// export const MedicalHistory = (props: PatientMedicalHistory) => {
//     return (
//         <>
//             <h2>Tiền sử bệnh nhân - người nhà bệnh nhân</h2>
//             <div className="row">
//                 <div className="row__column--half">
//                     <h4>Bệnh sử bệnh nhân</h4>
//                     <ul className="padding">
//                         {
//                             props.hpi.map((value) => {
//                                 return <li className="nobullet">{value.illness} {value.severity}</li>
//                             })
//                         }
//                     </ul>
//                 </div>
//                 <div className="row__column--half">
//                     <h4>Dị ứng</h4>
//                     <ul className="padding">
//                         {
//                             props.allergies.map((value) => {
//                                 return <li className="nobullet">{value}</li>
//                             })
//                         }
//                     </ul>
//                 </div>
//                 <div className="row__column--half">
//                     <h4>Tiền sử dùng thuốc</h4>
//                     <ul className="padding">
//                         {
//                             props.medicationHistory.map((value) => {
//                                 return <li className="nobullet">{value.medicine} - {value.status}</li>
//                             })
//                         }
//                     </ul>
//                 </div>
//                 <div className="row__column--half">
//                     <h4>Tiền sử gia đình</h4>
//                     <ul className="padding">
//                         {
//                             props.socialHistory.map((value) => {
//                                 return <li className="nobullet">{value}</li>
//                             })
//                         }
//                     </ul>
//                 </div>
//             </div>
//         </>
//     )
// }

// export const Prescription = (props: IPrescription) => {
//     const [expand, setExpand] = useState(false)
//     return (
//         <div className="prescription">
//             <div className="prescription__header">
//                 <p className="prescription__header__title">Đơn thuốc ngày: 22-10-2021</p>
//                 <div className="prescription__header__expand" onClick={() => setExpand(!expand)}>
//                     <FontAwesomeIcon icon={!expand ? faFolderPlus : faFolderMinus} />
//                 </div>
//             </div>
//             {expand &&
//                 <div className="prescription__detail--visible">
//                     <div className="prescription__detail__diagnose-container">
//                         <h5>Chẩn đoán</h5>
//                         <ul className="padding">
//                             <li className="nobullet">Viêm xoan mãn tính(Y11)</li>
//                             <li className="nobullet">Viêm loát bao tử(Y11)</li>
//                         </ul>
//                     </div>
//                     <div className="prescription__detail__medicine-container">
//                         <h5>Thuốc điều trị</h5>
//                         <ol className="padding">
//                             <li className="number-bullet">
//                                 <div className="prescription__detail__medicine__detail">
//                                     <p className="bold">Tên thuốc: Paracetamol 250mg</p>
//                                     <p>Liều dùng: Sáng 2 viên, Tối 2 viên</p>
//                                 </div>
//                             </li>
//                             <li className="number-bullet">
//                                 <div className="prescription__detail__medicine__detail">
//                                     <p className="bold">Tên thuốc: Paracetamol 250mg</p>
//                                     <p>Liều dùng: Sáng 2 viên, Tối 2 viên</p>
//                                 </div>
//                             </li>
//                         </ol>
//                     </div>
//                 </div>
//             }
//         </div>
//     )
// }

// export const MedicalInstruction = (props: { instruction: IMedicalInstruction[] }) => {
//     const [expand, setExpand] = useState(false)
//     return (
//         <div className="prescription">
//             <div className="prescription__header">
//                 <p className="prescription__header__title">Y lệnh từ bác sĩ</p>
//                 <div className="prescription__header__expand" onClick={() => setExpand(!expand)}>
//                     <FontAwesomeIcon icon={!expand ? faFolderPlus : faFolderMinus} />
//                 </div>
//             </div>
//             {expand &&
//                 <div className="prescription__detail--visible">
//                     <div className="prescription__detail__diagnose-container">
//                         <h5>Chẩn đoán</h5>
//                         <ul className="padding">
//                             <li className="nobullet">Viêm xoan mãn tính(Y11)</li>
//                             <li className="nobullet">Viêm loát bao tử(Y11)</li>
//                         </ul>
//                     </div>
//                 </div>
//             }
//         </div>
//     )
// }

// export const PatientSideBar = () => {
//     return (
//         <div className="leftbar">
//             <ul>
//                 <li>
//                     <div className="card">
//                         <div className="card__header">
//                             <img className="image" src="https://photo-baomoi.bmcdn.me/w700_r1/2022_09_29_83_43856916/d6b71eabdfe936b76ff8.jpg" />
//                             <h3>Hoang Thanh Phong</h3>
//                         </div>
//                         <h3>Tóm tắt bệnh nhân</h3>
//                         <div className="card__detail">
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faCakeCandles} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Ngày sinh</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>03-05-2022</p>
//                                 </div>
//                             </div>
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faVenusMars} size='1x'></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Giới tính</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Nam</p>
//                                 </div>
//                             </div>
//                         </div>
//                         <div className="card__detail">
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faFileWaveform} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Trạng thái</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Khỏe mạnh</p>
//                                 </div>
//                             </div>
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faFileWaveform} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Giám hộ</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Donald Regan</p>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </li>
//                 <li>
//                     <div className="card">
//                         <div className="card__header">
//                             <img className="image" src="https://photo-baomoi.bmcdn.me/w700_r1/2022_09_29_83_43856916/d6b71eabdfe936b76ff8.jpg" />
//                             <h3>Hoang Thanh Phong</h3>
//                         </div>
//                         <h3>Tóm tắt bệnh nhân</h3>
//                         <div className="card__detail">
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faCakeCandles} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Ngày sinh</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>03-05-2022</p>
//                                 </div>
//                             </div>
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faVenusMars} size='1x'></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Giới tính</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Nam</p>
//                                 </div>
//                             </div>
//                         </div>
//                         <div className="card__detail">
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faFileWaveform} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Trạng thái</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Khỏe mạnh</p>
//                                 </div>
//                             </div>
//                             <div className="card__detail__col">
//                                 <div className="card__detail__col__label">
//                                     <FontAwesomeIcon icon={faFileWaveform} size='1x' fixedWidth className="icon"></FontAwesomeIcon>
//                                     <p className="card__detail__col__label__text">Giám hộ</p>
//                                 </div>
//                                 <div className="card__detail__col__value">
//                                     <p>Donald Regan</p>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 </li>
//             </ul>
//         </div>
//     )
// }

// export const HealthRecordContentSideBar = () => {
//     return (
//         <div className="rightbar">
//             <div className="contract">
//                 <div></div>
//             </div>
//         </div>
//     )
// }


// export const HealthRecordListSideBar = () => {
//     let index = Array.from({ length: 20 }, (_, i) => i + 1)
//     return (
//         <div className="rightbar">
//             <div className="rightbar__tablecontent">
//                 <h2>Chỉ mục</h2>
//                 <div className="rightbar__tablecontent__list">
//                     <ul>
//                         <li><a href="#patient">1. Thông tin bệnh nhân</a></li>
//                         <li><a href="#history">2. Lịch sử điều trị</a></li>
//                         <li><a href="#instruction">3. Y lệnh</a></li>
//                         <li><a href="#prescription">4. Đơn thuốc</a></li>

//                     </ul>
//                 </div>
//             </div>
//             <div className="rightbar__healthrecord">
//                 <h2>Hồ sơ khám bệnh</h2>
//                 <ul className="rightbar__healthrecord__list">
//                     {index.map(() => {
//                         return <li className="rightbar__healthrecord__list__card">
//                             <div className="rightbar__healthrecord__list__card__icon">
//                                 <div className="rightbar__healthrecord__list__card__icon__wrapper">
//                                     <FontAwesomeIcon icon={faFile} size='2x' fixedWidth></FontAwesomeIcon>
//                                 </div>
//                             </div>
//                             <div className="rightbar__healthrecord__list__card__content">
//                                 <p className="title"><FontAwesomeIcon icon={faCalendarDay} fixedWidth/><span>Ngày bắt đầu</span></p>
//                                 <p className="value">22-12-2021</p>
//                                 <p className="title"><FontAwesomeIcon icon={faCalendarCheck} fixedWidth/><span>Ngày kết thúc</span></p>
//                                 <p className="value">22-12-2022</p>
//                             </div>
//                         </li>
//                     })}
//                 </ul>
//             </div>
//         </div>
//     )
// }




// export const HealthRecordDisplayer = (props: {
//     patient: IPatient,
//     history: PatientMedicalHistory
// }) => {
//     let patient = props.patient
//     return (
//         <div className="page__displayer">
//             <div id="patient" className="page__displayer__section">
//                 <h2>Thông tin tông quan</h2>
//                 <div className="page__displayer__section__personal">
//                     <ul className="page__displayer__section__list nopadding">
//                         <li className="nobullet">
//                             <div className="row">
//                                 <div className="row__column--half">
//                                     <p><FontAwesomeIcon icon={faUser} size='1x' fixedWidth /> Họ tên: <span className="bold-medium">{patient.lastName.concat(' ', patient.firstName)}</span></p>
//                                 </div>
//                                 <div className="row__column--half">
//                                     <p><FontAwesomeIcon icon={faCalendarDay} size='1x' fixedWidth /> Ngày sinh: <span className="bold-medium">{patient.dob.toLocaleString('vi-VI').slice(10)}</span></p>
//                                 </div>
//                             </div>
//                         </li>
//                         <li className="nobullet">
//                             <div className="row">
//                                 <div className="row__column--half">
//                                     <p><FontAwesomeIcon icon={faVenusMars} size='1x' fixedWidth /> Giới tinh: <span className="bold-medium">{patient.gender?.toString()}</span></p>
//                                 </div>
//                                 <div className="row__column--half">
//                                     <p><FontAwesomeIcon icon={faHome} size='1x' fixedWidth /> Địa chỉ: <span className="bold-medium">{patient.address}</span></p>
//                                 </div>
//                             </div>
//                         </li>
//                     </ul>
//                 </div>
//             </div>
//             <div id="history" className="page__displayer__section">
//                 <MedicalHistory
//                     hpi={props.history.hpi}
//                     allergies={props.history.allergies}
//                     socialHistory={props.history.socialHistory} 
//                     medicationHistory = {props.history.medicationHistory}/>
//             </div>
//             <div id="prescription" className="page__displayer__section">
//                 <h2>Đơn thuốc</h2>
//                 <div className="row">
//                 </div>
//             </div>
//         </div>
//     )
// }

// export const TreatmentSession = () => {
//     let patient: IPatient = {
//         id: 1,
//         firstName: 'John',
//         lastName: 'Doe HAHHHHHHH',
//         avatar: '',
//         address: '',
//         dob: new Date('2022-12-12'),
//         gender: 'Nam',
//     }
//     let history: PatientMedicalHistory = {
//         allergies: ['Cafein', 'Issulin'],
//         socialHistory: ['Hút thuốc lá', 'Uống bia rượu'],
//         medicationHistory: [{medicine: 'Aspirin 250mg', status:'Active'}, {medicine: 'Aspirin 250mg', status:'Active'}, {medicine: 'Aspirin 250mg',status:'Unknown'}]
//     }
//     return (
//         <div className="page">
//             <HealthRecordDisplayer patient={patient} history= {history}/>
//             <HealthRecordListSideBar />
//         </div>
//     )
// }
