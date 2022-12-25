import { faChevronCircleDown, faClose, faMinusCircle, faP, faPlusCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { cancelInstruction, getInstructionCategories } from 'api/contract_api';
import { getDisease, getMedicine, getPrescription, makePrescription } from 'api/prescriptionApi';
import { CustomDatePicker } from 'components/common/DatetimePicker';
import { dob } from 'constants/ConstValue';
import { ITreamtentContract } from 'models/contract';
import { Diseases } from 'models/diseases';
import { HealthRecord, IPrescription, IPrescription2, IPrescriptionDetails, IPrescriptionDetails2 } from 'models/health_record';
import { Medicines } from 'models/medicines';
import moment from 'moment';
import { ChangeEvent, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import '../style/modal.scss';

export const PrescriptionDetailModal = (props: { prescription: any, close: () => void, contract: ITreamtentContract }) => {
    const [prescription, setPrescription] = useState<IPrescription2>()
    useEffect(() => {
        async function init() {
            let data = await (await getPrescription(props.prescription)).data.data
            console.log('prescription', data)
            setPrescription(data)
        }
        init()
    }, [props.prescription])
    console.log('props detail', props.prescription);
    return prescription ? <div className="prescription_container">
        <div className="prescription_wrapper">
            <div className="prescription_header">
                <p>Chi tiết đơn thuốc</p>
            </div>
            <div className='prescription_horizontal_divider'></div>
            <div className="prescription_body">
                <div className='prescription_date'>
                    <div className='prescription_date_item'>
                        <p>Ngày tạo: {new Date(prescription!.createdAt).toLocaleDateString('vi-Vi', dob)}</p>
                    </div>
                    <div className='prescription_date_item'>
                        <p>Từ ngày: {new Date(prescription!.fromDate).toLocaleDateString('vi-Vi', dob)}</p>
                    </div>
                    <div className='prescription_date_item'>
                        <p>Đến ngày: {new Date(prescription!.toDate).toLocaleDateString('vi-Vi', dob)}</p>
                    </div>
                    {props.prescription.cancelReason ? <div className='prescription_date_item'>
                        <p>Lí do hủy: {props.prescription.cancelReason}</p>
                    </div>
                        : <></>}
                    <div className='prescription_date_item'>
                        <p>Trạng trái: {props.contract.endedAt > new Date() || props.prescription.toDate > new Date() ? 'Đã hết hạn'
                            : props.prescription.cancelReason === undefined ? 'Đã kê' : 'Đã Hủy'}</p>
                    </div>
                </div>
                <div className="prescription_diagnose">
                    <h6>Chuẩn đoán</h6>
                    {
                        prescription!.diagnose ? prescription!.diagnose.map((d: any) => {
                            return <div className='prescription_diagnose_item'>
                                <p>{d.code === undefined ? d : d.code!.concat('', d.diseaseName as string)}</p>
                            </div>
                        }) : <div className='prescription_diagnose_item'>
                            <p>Đơn thuốc hiện chưa có chuẩn đoán</p>
                        </div>
                    }
                </div>
                <div className='prescription_details_wrapper'>
                    <h6>Thuốc đã kê</h6>
                    <div className='prescription_details_content'>
                        <div className="prescription_details_content_wrapper">
                            {/* <div className="prescription_detail_item">
                                <div className="prescription_detail_name">
                                    <h6>Tên thuốc</h6>
                                    <p>Medicine 1</p>
                                </div>
                                <div className='verticalDivider'></div>
                                <div className="prescription_detail_usage">
                                    <h6>Cách dùng</h6>
                                    <p>Sáng 1 viên, chiều 1 viên, tối 1/2 viên</p>
                                </div>
                                <div className='verticalDivider'></div>
                                <div className="prescription_detail_note">
                                    <h6>Chú thích</h6>
                                    <p>Medicine 1</p>
                                </div>
                            </div> */}
                            {
                                prescription!.details && prescription!.details.map((de: any) => {
                                    console.log(de.medicine)
                                    return <div className="prescription_detail_item">
                                        <div className="prescription_detail_name">
                                            <h6>Tên thuốc</h6>
                                            <p>{de.medicine}</p>
                                        </div>
                                        <div className='verticalDivider'></div>
                                        <div className="prescription_detail_usage">
                                            <h6>Cách dùng</h6>
                                            <p>{de.guide}</p>
                                        </div>
                                        <div className='verticalDivider'></div>
                                        <div className="prescription_detail_note">
                                            <h6>Số lượng - đơn vị</h6>
                                            <p>{de.quantity && de.quantity.toLocaleString().concat(' ', de.unit)}</p>
                                        </div>
                                    </div>
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
            <div className='prescription_footer'>
                {
                    props.contract.status.toLowerCase().replaceAll('_', '') === 'IN_PROGRESS'.replaceAll('_', '').toLowerCase() && props.prescription.cancelReason === undefined ?
                        <button className='btnCancelAction' onClick={e => { props.close() }}>Hủy đơn thuốc</button>
                        : <></>
                }
                <button className='btnCloseAction' onClick={e => { props.close() }}>Đóng</button>
            </div>
        </div>
    </div> : <div className='prescription_container'>
        <p>Loading</p>
    </div>
}

export const AddNewModal = (props: {
    addInput: React.Dispatch<React.SetStateAction<Array<IPrescriptionDetails2>>>,
    closeModal: () => void
}) => {
    const unit = ['Viên', 'Gói', 'Chai']
    const [suggestedMedicine, setSuggestedMedicine] = useState<Array<Medicines>>([])
    const [usage, setNewUsage] = useState<string>('')
    const [currentUnit, setCurrentUnit] = useState(unit[0])
    const [quantity, setQuantity] = useState(0)
    const [selectedMedicine, setSelectedMedicine] = useState<Medicines>()
    const [medicineError, setMedicineError] = useState<string>()
    const [usageError, setUsageError] = useState<string>()
    const [quantityError, setQuantityError] = useState<string>()

    const [prescriptionDetail, setPrescriptionDetail] = useState<IPrescriptionDetails2>()
    const [prescirptionDetailError, setPrescriptionDetailError] = useState({
        'medicineError': '',
        'usageError': '',
        'quantityError': '',
        'prescriptionError': ''
    })

    useEffect(() => {
        async function init() {
            let suggestedMedicine = await (await getMedicine('a')).data.data
            setSuggestedMedicine(suggestedMedicine);
            setPrescriptionDetail({
                medicine: suggestedMedicine[0],
                guide: '',
                quantity: 0,
                unit: unit[0]
            })
        }
        init();
    }, [])

    const handleMedicineInputChange = async (e: ChangeEvent<HTMLInputElement>) => {
        let result = await (await getMedicine(e.target.value)).data.data
        console.log('search medicine', result)
        setSuggestedMedicine(result)
    }
    const handleUsageInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setNewUsage(e.currentTarget.value)
    }

    const handleQuantityChange = (e: ChangeEvent<HTMLInputElement>) => {
        try {
            let num = Number.parseInt(e.currentTarget.value)
            setQuantity(num)
        }
        catch (e) {
            setQuantityError('Số lượng phải là chữ số')
        }
    }

    const onAddNew = (detail: IPrescriptionDetails2) => {
        console.log(selectedMedicine);
        let isError = false;
        if (selectedMedicine === undefined || selectedMedicine === null) {
            setMedicineError('Loại thuốc không được bỏ trống')
            isError = true;
        }
        if (usage === undefined || usage.concat('').replaceAll(' ', '') === '') {
            setUsageError('Cách dùng không được để trống')
            isError = true;
        }
        if (quantity <= 0) {
            setQuantityError('Số lượng phải nguyên dương')
            isError = true;
        }
        console.log(isError, prescirptionDetailError)
        if (isError) {
            // setPrescriptionDetailError({medicineError: prescirptionDetailError.medicineError, quantityError: prescirptionDetailError.quantityError, usageError: prescirptionDetailError.usageError,prescriptionError: prescirptionDetailError.prescriptionError})
            return;
        }
        setQuantityError('')
        setUsageError('')
        setMedicineError('');
        console.log('call success')
        props.addInput((prev) => {
            console.log('prev state', prev)
            return prev.concat(detail)
        })
    }

    const addMedicine = (e: Medicines) => {
        setSelectedMedicine(e)
        // prescriptionDetail!.medicine = e
        console.log(prescriptionDetail?.medicine, e)
        // setPrescriptionDetail(copy(prescriptionDetail as IPrescriptionDetails2))
    }

    return <div className='prescription_prescription_form'>
        <div className='prescription_prescription_form_add'>
            <div className='form_title'>
                <h4>Thêm thuốc mới</h4>
            </div>
            <div className='field field--hover'>
                <h6>Loại thuốc*</h6>
                <input className='text_input' type='text' value={selectedMedicine ? selectedMedicine.name : ''} />
                <div className='error'>{medicineError}</div>
                <div className='medicineSuggestion'>
                    <input className='text_input' type='text' onChange={handleMedicineInputChange} placeholder={'Nhập tên thuốc cần tìm'} />
                    <div className='suggest_result'>
                        {suggestedMedicine.map(m => <p key={m.id} onClick={(e) => addMedicine(m)}>{m.name}</p>)}
                    </div>
                </div>
            </div>
            <div className='field'>
                <h6>Cách dùng*</h6>
                <input className='text_input' type='text' onChange={handleUsageInputChange} placeholder="Sáng n viên tối, n1 viên" />
                <div className='error'>{usageError}</div>
            </div>
            <div className='field field--half'>
                <h6>Đơn vị*</h6>
                <div className='unit_dropdown'>
                    <div className='dropdown_selection'>
                        <p className='dropdown_selection_text'>{currentUnit}</p>
                        <div className='icon_container'>
                            <div className='icon'>
                                <FontAwesomeIcon icon={faChevronCircleDown} size='1x' fixedWidth></FontAwesomeIcon>
                            </div>
                        </div>
                    </div>
                    <div className='dropdown_option'>
                        {unit.map(u => <div className='dropdown_option_item' onClick={e => { setCurrentUnit(u) }}>
                            <p>{u}</p>
                        </div>
                        )}
                    </div>
                </div>
            </div>
            <div className='field field--half'>
                <h6>Số lượng*</h6>
                <input className='text_input' type='number' placeholder="Sáng n viên tối, n1 viên" onChange={handleQuantityChange} />
                <div className='error'>{quantityError}</div>
            </div>
            <div className='field field--action'>
                <button className='field__button--half' onClick={e => { console.log('add new clicked'); onAddNew({ medicine: selectedMedicine, guide: usage, quantity: quantity, unit: currentUnit }) }}>Thêm thuốc</button>
                <button className='field__button--half' onClick={e => props.closeModal()}>Hủy bỏ</button>
            </div>
        </div>
    </div>
}

export const PrescriptionCreatorprescription = (props: { onClose: () => void, healthRecord: HealthRecord }) => {
    const [diagnoses, setDiagnose] = useState<Array<Diseases>>([])
    const [medicines, setMedicine] = useState<Array<IPrescriptionDetails2>>([])
    const [suggestedDisease, setSuggestedDisease] = useState<Array<Diseases>>([])
    const [modal, setOpenModal] = useState<boolean>(false)
    const [fromDate, setFromDate] = useState<string>(new Date().toISOString())
    const [toDate, setToDate] = useState<string>(new Date().toISOString())
    const [datetimeError, setTimeError] = useState({ 'fromDateErro': '', 'toDateErro': '' })


    useEffect(() => {
        async function init() {
            let result = await (await getDisease('a')).data.data
            setSuggestedDisease(result);
        }
        init();
    }, [])

    useEffect(() => {
        console.log('medicine list: ', medicines);
    }, [medicines])

    const addDisease = (disease: Diseases) => {
        setDiagnose(diagnoses.concat(disease));
    }
    const closeModal = () => {
        setOpenModal(!modal);
    }
    const removeDisease = (removeItem: Diseases) => {
        let newArray = diagnoses.filter(disease => removeItem.id !== disease.id);
        setDiagnose(newArray);
    }
    const removeMedicines = (removeItem: IPrescriptionDetails2) => {
        let newArray = medicines.filter(m => m.guide !== removeItem.guide || m.medicine.id !== removeItem.medicine.id);
        setMedicine(newArray);
    }
    const handleDiseasesInputChange = async (e: ChangeEvent<HTMLInputElement>) => {
        console.log(e.currentTarget.value)
        let result = await (await getDisease(e.currentTarget.value)).data.data
        setSuggestedDisease(result)
    }
    const openModal = () => {
        setOpenModal(!modal);
    }

    const handleFromDateChange = (date: string, comparator: string) => {
        if (new Date().getDate() > new Date(date).getDate()) {
            datetimeError.fromDateErro = 'Ngày bắt đầu phải lớn hơn bằng với hiện tại'
            return;
        }
        setFromDate(date)
    }

    const handleToDateChange = (date: string, comparator: string) => {
        console.log(date)
        if (new Date(fromDate).getDate() > new Date(date).getDate()) {
            datetimeError.fromDateErro = 'Ngày bắt đầu phải lớn hơn bằng với hiện tại'
            setTimeError({
                toDateErro: datetimeError.toDateErro,
                fromDateErro: datetimeError.fromDateErro
            })
            return;
        }
        if (new Date().getDate() > new Date(date).getDate()) {
            datetimeError.fromDateErro = 'Ngày bắt đầu phải lớn hơn bằng với hiện tại'
            setTimeError({
                toDateErro: datetimeError.toDateErro,
                fromDateErro: datetimeError.fromDateErro
            })
            return;
        }
        setToDate(date)
    }

    const asyncAddPrescriptions = async () => {
        let prescription: IPrescription = {
            id: 1,
            cancelReason: '',
            createdAt: new Date().toISOString(),
            details: medicines,
            diagnose: suggestedDisease,
            fromDate: fromDate,
            toDate: toDate,
            healthRecord: props.healthRecord.recordId,
            note: []
        }
        await makePrescription(prescription, props.healthRecord.recordId, props.healthRecord.patient.id).then((res) => {
            window.alert('Create Prescription Success')
        }).catch(e => {
            console.log(e);
        })

    }

    return (
        <div className='prescription_creation_form_wrapper'>
            <div className='prescription_creation_form'>
                <div className='prescription_creation_form_content'>
                    <div className='prescription_datetime'>
                        <div className='field field--half'>
                            <h6>Ngày bắt đầu</h6>
                            <CustomDatePicker comparator='lte' selectedDate={new Date(fromDate).toISOString()} changeDate={handleFromDateChange}></CustomDatePicker>
                        </div>
                        <div className='field field--half'>
                            <h6>Ngày hết hạn</h6>
                            <CustomDatePicker comparator='lte' selectedDate={new Date(toDate).toISOString()} changeDate={handleToDateChange}></CustomDatePicker>
                        </div>
                    </div>
                    <div className='prescription_diagnose_form'>
                        <h6>Chuẩn đoán</h6>
                        <div className='selection_list'>
                            {
                                diagnoses.map(
                                    (diagnose) => <div className='prescription_diagnose_item'>
                                        <p>{diagnose.code?.concat('-', diagnose.diseaseName as string)}<FontAwesomeIcon icon={faClose} size='1x' fixedWidth onClick={e => removeDisease(diagnose)} /></p>
                                    </div>
                                )
                            }

                        </div>
                        <div className='prescription_diagnose_form_addInput'>
                            <input type={'text'} placeholder={'Nhập tên bệnh cần tìm'} onChange={handleDiseasesInputChange} className='focus_input'></input>
                            {/* <div className='button_wrapper'>
                                <FontAwesomeIcon icon={faPlusCircle} size='1x' fixedWidth />
                            </div> */}
                            <div className='diseaseSuggestion'>
                                {suggestedDisease.map(disease => <div className='disease' onClick={e => addDisease(disease)}>{disease.diseaseName}</div>)}
                            </div>
                        </div>
                    </div>
                    <div className='prescription_medicine_list'>
                        <div className='prescription_medicine_list_title'>
                            <h5>Toa thuốc</h5>
                        </div>
                        <div className='prescription_medicine_list_action'>
                            <button className='btnAction' onClick={e => openModal()}>Thêm thuốc mới</button>
                        </div>
                        {/* <div className='prescription_medicine_list_item'>
                        <div className='prescription_medicine_list_item_detail'>
                            <h6>Tên thuốc: số 1 - Số lượng: 20 viên</h6>
                            <p>Liều dùng: Sáng 1 viên, Tối 2 viên</p>
                        </div>
                        <div className='remove_action'>
                            <div className='icon'>
                                <FontAwesomeIcon icon={faMinusCircle} size='2x' fixedWidth />
                            </div>
                        </div>
                    </div> */}
                        <div className='prescription_medicine_list_wrapper'>
                            {
                                medicines.map(m => {
                                    console.log(m);
                                    return <div className='prescription_medicine_list_item'>
                                        <div className='prescription_medicine_list_item_detail'>
                                            <h6>Tên thuốc: {m.medicine.name} - Số lượng {m.quantity} - {m.unit}</h6>
                                            <p>Liều dùng: {m.guide}</p>
                                        </div>
                                        <div className='remove_action'>
                                            <div className='icon'>
                                                <FontAwesomeIcon icon={faMinusCircle} size='2x' fixedWidth onClick={e => removeMedicines(m)} />
                                            </div>
                                        </div>
                                    </div>
                                })
                            }
                        </div>
                    </div>
                    {modal ? <AddNewModal addInput={setMedicine} closeModal={closeModal} /> : <></>}
                </div>
                <div className='prescription_creation_form_footer'>
                    <button className='half-width' onClick={(e) => { asyncAddPrescriptions() }}>Tạo mới</button>
                    <button className='half-width' onClick={e => props.onClose()}>Hủy</button>
                </div>
            </div>
        </div>
    )
}

export const MedicalInstructionDetailModal = (props: { instruction: any, onClose: () => void, rerender: () => void}) => {
    let requirement = props.instruction.requirments.replaceAll("\"", "");
    let isUrl = requirement.startsWith("http") || requirement.startsWith("https");
    let submissions = props.instruction.submissions.replaceAll("\"", "");
    let isSubUrl = submissions.startsWith("http") || requirement.startsWith("https");

    const handleCancelInstruction = async (id: number) => {
        cancelInstruction(id).then((r: any) => {
            props.rerender();
        }).catch((e:any) => {
            console.log('error', e);
        })
    }

    return <div className='prescription_modal'>
        <div className='modal_box'>
            <div className='modal_box_header'>
                <h5>Chi tiết y lệnh</h5>
            </div>
            <div className='modal_divider'></div>
            <div className='modal_box_content'>
                <div className='instruction_date'>
                    <h6>Ngày tao: </h6>
                    <div className='short_detail'>
                        <p>{moment(props.instruction.createdAt).format('DD-MM-yyyy')}</p>
                    </div>
                </div>
                <div className='instruction_type'>
                    <h6>Loại y lệnh:</h6>
                    <div className='short_detail'>
                        <p>{props.instruction.category}</p>
                    </div>
                </div>
                <div className='requirment'>
                    <h6>Yêu cầu chi tiết</h6>
                    <div className='requirment_detail'>
                        {isUrl ? <a target={'_blank'} href={requirement}>Minh họa đơn thuốc</a> : props.instruction!.requirement}
                    </div>
                    <h6>Kết quả y lệnh</h6>
                    <div className='requirment_detail'>
                        {isSubUrl ? <a target={'_blank'} href={submissions}>Kết quả đơn thuốc</a> : props.instruction!.submissions}
                    </div>
                </div>
            </div>
            <div className='modal_box_footer'>
                <div className='wrapperCenter'>
                    <button className='btn' onClick={e => { props.onClose() }}>Đóng lại</button>
                    <button className='btn' onClick={e => {}} disabled= {props.instruction.status.toUpperCase() !== 'PENDING'}>Hủy y lệnh</button>
                </div>
            </div>
        </div>
    </div>
}


export const InitPrescriptionReadonly = () => {
    const [prespcrion, setPrescription] = useState<number>()
    const location = useLocation<any>()
    useEffect(() => {
        setPrescription(location.state)
        console.log('history state', location.state)
    }, [location.state])
    return <></>
    // return <PrescriptionDetailModal prescription={prespcrion} close={() => { }} />
}


export const MedicalInstructionDetailCreatorModal = (props: { onClose: () => void }) => {
    const [date, setDate] = useState<string>(new Date().toISOString().slice(0, 10))
    const [category, setCategory] = useState<any[]>()
    const [requirements, setRequirements] = useState<string>('')
    const [selectCategory, setSelectCategory] = useState<any>()
    useEffect(() => {
        let result = [];
        let category = getInstructionCategories();
        category.then(res => {
            result = res.data.data
        })
    }, [])

    const handleChangeDate = (date: string, comparator: string) => {
        setDate(date)
    }

    return <div className='prescription_modal'>
        <div className='modal_box'>
            <div className='modal_box_header'>
                <h5>Y lệnh mới</h5>
            </div>
            <div className='modal_divider'></div>
            <div className='modal_box_content'>
                <div className='instruction_date'>
                    <h6>Ngày tạo: </h6>
                    <CustomDatePicker selectedDate={date} changeDate={handleChangeDate} comparator='' />
                </div>
                <div className='instruction_type'>
                    <h6>Loại y lệnh</h6>
                    <div className='dropdown'>
                        <div className='dropdown_selection'>
                            <p className='result'>{selectCategory && selectCategory.name}</p>
                        </div>
                        <div className='dropdown_options'>
                            {
                                category && category.map(c => {
                                    return <p className='dropdown_options_item'>{c.name}</p>
                                })
                            }
                        </div>
                    </div>

                </div>
                <div className='requirment'>
                    <h6>Yêu cầu chi tiết</h6>
                    <textarea cols={60} onChange={e => { setRequirements(e.currentTarget.value) }}></textarea>
                </div>
            </div>
            <div className='modal_box_footer'>
                <div className='wrapperCenter'>
                    <button className='btn' onClick={e => { props.onClose() }}>Thêm y lệnh</button>
                    <button className='btn'>Hủy y lệnh</button>
                </div>
            </div>
        </div>
    </div>
}