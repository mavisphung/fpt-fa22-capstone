import { faFile, faFileMedical } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { HealthRecord } from 'models/health_record'
import { useState, useEffect } from 'react'
import '../../style/contract_healthRecord.scss'
export const HealthRecordSharedDoccument = (props: { healthRecord: HealthRecord }) => {
    const [record, setRecord] = useState(props.healthRecord)

    useEffect(() => {
        console.log(record.detail.diseases !== undefined, record.detail)
        setRecord(props.healthRecord)
        console.log(record.detail.diseases !== undefined, record.detail)
    }, [props.healthRecord])

    return (
        <div className='contract_health_record'>
            <div className='contract_health_record_header'>
                <h5 className='text_bold'>Thông tin sức khỏe</h5>
            </div>
            <div className='contract_health_record_content'>
                <div className='contract_health_record_content_section'>
                    <h6 className='text_bold'>Bệnh lý yêu cầu theo dõi</h6>
                    <div className='contract_health_record_item '>
                        {
                            record.detail.diseases !== undefined && record.detail.diseases.length > 0 ? record.detail.diseases.map((d: any) => {
                                return <div className='contract_health_record_item_disease'>
                                    <div className='contract_health_record_item_disease_wrapper'>
                                        <h6 className='title'>Mã bệnh lý - tên bệnh lý</h6>
                                        <p className='no_padding'>{d.code} - {d.diseaseName}</p>
                                    </div>
                                </div>
                            }) : <p className='no_padding'>Chưa có bệnh lý được ghi nhận</p>
                        }
                    </div>
                </div>
                <div className='contract_health_record_content_section'>
                    <h6 className='text_bold'>Tiền sử bệnh tật đã ghi nhận:</h6>
                    <div className='contract_health_record_item '>
                        {
                            record.detail.pathologies !== undefined && record.detail.pathologies.length > 0 ? record.detail.pathologies.map((d: any) => {
                                return <div className='contract_health_record_item_disease'>
                                    <div className='contract_health_record_item_disease_wrapper'>
                                        <p className='no_padding'>{d.code} - {d.diseaseName}</p>
                                    </div>
                                </div>
                            }) : <p className=''>Chưa có bệnh lý đã ghi nhận</p>
                        }
                    </div>
                </div>
                <div className='contract_health_record_content_section'>
                    <h6 className='text_bold'>Tiền sử dị ứng đã ghi nhận:</h6>
                    <div className='contract_health_record_item '>
                        {
                            record.detail.allergies !== undefined && record.detail.allergies.length > 0 ? record.detail.allergies.map((d: any) => {
                                return <div className='contract_health_record_item_disease'>
                                    <div className='contract_health_record_item_disease_wrapper'>
                                        <p className='no_padding'>{d}</p>
                                    </div>
                                </div>
                            }) : <p className=''>Chưa có bệnh lý đã ghi nhận</p>
                        }
                    </div>
                </div>

                <div className='contract_health_record_content_section'>
                    <h6 className='text_bold'>Tiền sử xã hội:</h6>
                    <div className='contract_health_record_item '>
                        {
                            record.detail.socialHistory !== undefined && record.detail.socialHistory.length > 0 ? record.detail.socialHistory.map((d: any) => {
                                return <div className='contract_health_record_item_disease'>
                                    <div className='contract_health_record_item_disease_wrapper'>
                                        <p className='no_padding'>{d}</p>
                                    </div>
                                </div>
                            }) : <p className=''>Chưa có ghi nhận về tiền sử xã hội</p>
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}