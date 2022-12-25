import { faCakeCandles, faFile, faFileMedical, faHome, faPerson, faVenusMars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { t } from "i18next";
import { HealthRecord, PatientMedicalHistory } from "models/health_record";
import { IPatient } from "models/patient";
import { useTranslation } from "react-i18next";
import './page.scss'
export const PatientInfo = (props: {
    patient: IPatient,
    medicalHistory: PatientMedicalHistory
}) => {
    var patient = props.patient;
    var medicalHistory = props.medicalHistory;
    const { t, i18n } = useTranslation();
    return (
        <div className="patient_info">
            <div className="patient_info__summary">
                <div className="patient_info__summary__row">
                    <img
                        className="patient_info__summary__row__avatar"
                        src='https://vcdn1-giaitri.vnecdn.net/2022/08/25/Avatar-213-8923-1661403266.png?w=0&h=0&q=100&dpr=2&fit=crop&s=KWo2kCkyQr5Xxia52ObvvA' />
                    <h3>{props.patient.firstName.concat(' ', props.patient.lastName)}</h3>
                </div>
                <div className="patient_info__summary__row patient_info__summary__row--horizontal_stack">
                    <div className="col col--half">
                        <h4>15</h4>
                        <p>Days Past</p>
                    </div>
                    <div className="br"></div>
                    <div className="col col--half">
                        <h4>15</h4>
                        <p>Days Left</p>
                    </div>
                </div>
                <div className="patient_info__summary__row patient_info__summary__row--fitcontent">
                    <button className="btn">{t('send message')}</button>
                </div>
            </div>
            <div className="patient_info__detail">
                <div className="wrapper">
                    <div className="row">
                        <div className="col col--third">
                            <p>{t('patient.gender')}</p>
                            <h4>{patient.gender}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.dob')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.address')}</p>
                            <h4>{patient.address}</h4>
                        </div>
                    </div>
                </div>
                <div className="wrapper">
                    <div className="row">
                        <div className="col col--third">
                            <p>{t('patient.StartDate')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.EndDate')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.followDate')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                    </div>
                </div>
                <div className="wrapper">
                    <div className="row">
                        <div className="col col--third">
                            <p>{t('patient.chiefOfComplaint')}</p>
                            <h4>{medicalHistory.chiefComplaint}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.format')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                        <div className="col col--third">
                            <p>{t('patient.followDate')}</p>
                            <h4>{patient.dob?.toString()}</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export const HealthRecordTab = (props: {
    healthRecord: HealthRecord,
}) => {
    let healthRecord = props.healthRecord;
    let session: {
        no: number,
        date: Date | string,
        note: string,
        status: string,
    } = {
        no: 1,
        date: new Date(),
        note: 'Not available',
        status: 'pending',
    }
    let dateFormatter = new Intl.DateTimeFormat('vi-VI', {})
    const { t, i18n } = useTranslation();
    return (
        <div className="health_record">
            <div className="health_record__tabBar">
                <div className="health_record__tabBar__item">
                    <h4>Prescription</h4>
                </div>
            </div>
            <div className="health_record__prescription">
                {healthRecord.prescriptions.map((prescription) => {
                    return <div className="health_record__prescription__row">
                        <div className="health_record__prescription__row__col health_record__prescription__row__col--ten">
                            <div className="content">
                                <p>{t('prescription.no')}</p>
                                <h5>{prescription.id}</h5>
                            </div>
                            <div className="br--center">
                                <div className="br--center__content" />
                            </div>
                        </div>
                        <div className="health_record__prescription__row__col health_record__prescription__row__col--fourth">
                            <div className="content">
                                <p>{t('prescription.fromDate')}</p>
                                <h5>{dateFormatter.format(prescription.fromDate as Date)}</h5>
                            </div>
                            <div className="br--center">
                                <div className="br--center__content" />
                            </div>
                        </div>
                        <div className="health_record__prescription__row__col health_record__prescription__row__col--fourth">
                            <div className="content">
                                <p>{t('prescription.toDate')}</p>
                                <h5>{dateFormatter.format(prescription.toDate as Date)}</h5>
                            </div>
                            <div className="br--center">
                                <div className="br--center__content" />
                            </div>
                        </div>
                        <div className="health_record__prescription__row__col health_record__prescription__row__col--fourth">
                            <div className="content">
                                <p>{t('prescription.cancelReason')}</p>
                                <h5>{prescription.cancelReason.trim() === '' ? "Not cancel yet": prescription.cancelReason}</h5>
                            </div>
                            <div className="br--center">
                                <div className="br--center__content" />
                            </div>
                        </div>
                    </div>
                })}
            </div>
        </div>
    )
}

export const HealthRecordPage = () => {
    const patient: IPatient = {
        id: 1,
        firstName: 'John',
        lastName: 'Doe',
        avatar: "https://vcdn1-giaitri.vnecdn.net/2022/08/25/Avatar-213-8923-1661403266.png?w=0&h=0&q=100&dpr=2&fit=crop&s=KWo2kCkyQr5Xxia52ObvvA",
        dob: "2022-12-12",
        gender: 'Male',
        address: "No Address",
    }
    const medicalHistory: PatientMedicalHistory = {
        allergies: ['Cafein', 'Vitamin D'],
        historyOfPresentIllness: [{ illness: 'Viêm Phổi Mãn Tính', severity: 'Nặng', recordDate: new Date() }],
        socialHistory: ['Hút thuốc lá', 'Uống Bia'],
        medicationHistory: [{ medicine: 'Aspirin 250mg', status: 'Active' }, { medicine: 'Aspirin 250mg', status: 'Active' }],
        chiefComplaint: "Đau dạ dày",
    }

    const healthRecord: HealthRecord = {
        recordId: 1,
        description: 'Mo ta',
        medicalHistory: {
            allergies: ['Cafein', 'Vitamin D', 'Phấn Hoa',],
            chiefComplaint: "Đau dạ dày",
            medicationHistory: [{ medicine: 'Aspirin 250mg', status: 'Active' }, { medicine: 'Aspirin 250mg', status: 'Active' }],
            socialHistory: ['Hút thuốc lá', 'Uống tăng lực'],
            historyOfPresentIllness: [{ illness: 'Lao Phổi', recordDate: new Date(2012, 12, 12), severity: 'Normal' }]
        },
        instructions: [],
        patient: patient,
        name: "Hồ sơ sức khỏe từ Bác Sĩ Nguyễn Văn Khoa",
        prescriptions: []
    }

    return (
        <div className="page">
            <div className="page__heading">

            </div>
            <div className="main_section">
                <div className="main_section__half">
                    <PatientInfo patient={patient} medicalHistory={medicalHistory} />
                </div>
                <div className="main_section__half">
                    <HealthRecordTab healthRecord={healthRecord}></HealthRecordTab>
                </div>
            </div>
        </div>
    )
}