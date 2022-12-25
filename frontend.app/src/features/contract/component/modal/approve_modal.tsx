import { faClose } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { approveContract, approveRequestBody } from 'api/contract_api';
import { CustomDatePicker } from 'components/common/DatetimePicker';
import { ITreamtentContract } from 'models/contract';
import { InfoUser } from 'models/infoUser';
import moment from 'moment';
import 'moment/locale/vi';
import { useState, useEffect } from 'react';
import { suggestDoctorHour } from '../../../../../src/api/sessionApi'
import '../../style/approval_modal.scss'

export interface IWeekDay {
    "day": number,
    "title": string
}
export const SelectedSchedules = (props: {
    contract: ITreamtentContract,
    onSubmit: (session: any[]) => void,
    onChangeEnd: (endAt: string) => void,
    next: (next: number) => void,
}) => {
    const [endDate, setEndDate] = useState<string | undefined>(moment(props.contract.startedAt).format('yyyy-MM-DD'))
    const [schedule, setSchedules] = useState<Map<string, any>>(new Map<string, any>([]))
    const [suggestions, setSuggestions] = useState<{ "date": string, slots: any[] }[]>([])
    const [weekSchedule, setWeekSchedule] = useState<Array<IWeekDay>>([])
    const [tab, setTab] = useState(1);
    const daysofweek = [
        { 'day': 0, 'title': 'Chủ nhật' },
        { 'day': 1, 'title': 'Thứ hai' },
        { 'day': 2, 'title': 'Thứ ba' },
        { 'day': 3, 'title': "Thứ tư" },
        { 'day': 4, 'title': "Thứ năm" },
        { 'day': 5, 'title': "Thứ sáu" },
        { 'day': 6, 'title': "Thứ bảy" },
    ]
    const handleChangeDate = (date: string, com: string) => {
        props.onChangeEnd(date)
        setEndDate(date);
    }

    const submitStep = () => {
        let sessions: any[] = []
        schedule.forEach((value, key) => {
            let session = {
                "startTime": moment(key.concat(" ", value.from)).format("YYYY-MM-DD HH:mm:ss"),
                "endTime": moment(key.concat(" ", value.to)).format("YYYY-MM-DD HH:mm:ss")
            }
            sessions.push(session)
        })
        console.log('session created', sessions);
        return sessions
    }

    const handleSlotAvaliableTime = (slot: any) => {
        let from: moment.Moment = moment(slot.from, 'hh:mm').utcOffset("+07:00", true);
        let to: moment.Moment = moment(slot.to, 'hh:mm').utcOffset("+07:00", true);
        let duration: moment.Duration = moment.duration(to.diff(from));
        if (duration.asMinutes() > 15) {
            let result: any[] = [];
            let current = from;
            let array = new Array(Math.floor(duration.asMinutes() / 15))
            let i = 0;
            console.log(array.length);
            while (i < array.length) {
                console.log('utcOffset', current.utcOffset("+07:00", true).toDate().toLocaleTimeString('vi-VI', {
                    hourCycle: 'h24'
                }));
                let slot = {
                    'from': current.utcOffset("+07:00", true).toDate().toLocaleTimeString('vi-VI', {
                        hourCycle: 'h24'
                    }).slice(0, 5),
                    'to': current.utcOffset("+07:00", true).add(15, 'minutes').toDate().toLocaleTimeString('vi-VI', {
                        hourCycle: 'h24'
                    }).slice(0, 5),
                }
                result = result.concat(slot);
                i++;
            }
            console.log('cuted result: ', result);
            return result;
        } else {
            return []
        }
    }

    const getSuggestion = async (dates: any[]) => {
        let suggestion: any[] = [];
        let promise;
        promise = dates.map(d => {
            return suggestDoctorHour(d);
        })
        await Promise.all(promise).then((res) => {
            let newMap = new Map<string, any>(schedule.entries());
            res.forEach((r, index) => {
                console.log(r);
                suggestion = suggestion.concat({
                    'date': dates[index],
                    'slots': r.data.data
                })
            })
            suggestion = suggestion.map(a => {
                let slots: any[] = a.slots
                slots = slots.map(sl => {
                    return handleSlotAvaliableTime(sl);
                }).flat(1)
                newMap.set(a.date, slots[0])
                return {
                    "date": a.date,
                    "slots": slots,
                }
            })
            setSchedules(newMap);
            setSuggestions(suggestion);
        })
    }

    const generateDate2 = (from: string, to: string, dayofweek: any[]) => {
        let result: any = []
        let endMoment = moment(to)
        let currentMoment = moment(from)
        while (currentMoment <= endMoment) {
            if (dayofweek.find(d => d.day === currentMoment.day()))
                result = result.concat(currentMoment.format('yyyy-MM-DD'))
            currentMoment.add(1, 'day')
        }
        console.log(result);
        return result;
    }
    const handleSubmitWeekSchedule = () => {
        let dates = generateDate2(moment(props.contract.startedAt).format('yyyy-MM-DD'), moment(endDate).format('yyyy-MM-DD'), weekSchedule);
        getSuggestion(dates);
    }

    const handleSubmitDaySlot = (date: any, slot: any, session: any) => {
        if (!schedule) {
            let newSchedule = new Map<string, IWeekDay>([
                [date, slot]
            ])
            console.log(newSchedule);
            setSchedules(newSchedule);
            return;
        }
        let newSchedule = new Map<string, IWeekDay>(schedule.entries());
        newSchedule.set(date, slot);
        console.log('new schedule', newSchedule, 'slot ', session);
        setSchedules(newSchedule);
    }

    const handleNext = () => {
        let session = submitStep();
        props.onSubmit(session);
        props.next(2);
    }

    useEffect(() => {
        console.log('before render', schedule);
        handleSubmitWeekSchedule();
    }, [endDate, weekSchedule])

    return (
        <div className='schedule_container'>
            <div className='schedule_container_config'>
                <div className='schedule_container_datepicker'>
                    <h6 className="bold_text">Chọn ngày kết thúc hợp đồng</h6>
                    <CustomDatePicker selectedDate={endDate as string} changeDate={handleChangeDate} comparator='lte'></CustomDatePicker>
                </div>
                <div className='weekly_schedule'>
                    <h6 className="bold_text">Chọn thời gian biểu trong tuần</h6>
                    <div className='weekly_schedule_days'>
                        <div className='weekly_schedule_days_selection'>
                            {
                                weekSchedule && weekSchedule.length > 0 ? weekSchedule.map(w => {
                                    return <span className='week_day_selection'>{w.title}</span>
                                }) : <span className='week_day_place_holder'>Chọn ngày trong tuần</span>
                            }
                        </div>
                        <div className='weekly_schedule_days_options'>
                            {
                                daysofweek.map(d => {
                                    return <div className='weekly_schedule_days_options_item'>
                                        <input key={d.day} type={'checkbox'} onChange={(e) => {
                                            if (e.currentTarget.checked) {
                                                setWeekSchedule(weekSchedule.concat(d).sort((a: IWeekDay, b: IWeekDay) => (a.day - b.day)));
                                                return;
                                            }
                                            setWeekSchedule(weekSchedule.filter(c => c.day !== d.day));
                                        }} value={d.title} /> {d.title}</div>
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
            <div className='suggestion_slot'>
                <h6 className="bold_text">Thiết lập lịch theo dõi đánh giá - điều trị</h6>
                <div className='suggestion_slot_result'>
                    {
                        suggestions.map((s) => {
                            let localLocale = moment(s.date);
                            localLocale.locale('vi')
                            return <div className='slot_datetime_item'>
                                <h6 className='slot_datetime_item_date'>{localLocale.format('LLLL').replace('00:00', '')}</h6>
                                <div className='slot_datetime_item_selection'>
                                    <p className='slot_datetime_item_time_result'>
                                        <span className='slot_wrapper'>
                                            {schedule.get(s.date) && schedule!.get(s.date).from} - {schedule.get(s.date) && schedule!.get(s.date).to}
                                        </span>
                                    </p>
                                </div>
                                <div className='slot_datetime_item_time_options'>
                                    {s.slots.map(slot => {
                                        return <p className='slot_datetime_item_time'><span className='slot_wrapper' onClick={e => handleSubmitDaySlot(s.date, slot, s)}>{slot.from} - {slot.to}</span></p>
                                    })}
                                </div>
                            </div>
                        })
                    }
                </div>
            </div>
            <div className='horizontal_divider horizontal_divider--stickbottom'></div>
            <div className='footer_action'>
                <button className='footer_action_wrapper_submit' onClick={e => {
                    handleNext();
                }}>Tiếp theo</button>
            </div>
        </div>
    )
}


export const AcceptRule = (props: {
    onSign: (signed: boolean) => void,
    onFinalize: () => void
    contract: ITreamtentContract,
    endDate: string,
}) => {
    const [step, setStep] = useState(1);
    const [isApprove, setIsApprove] = useState(false);

    const handleChangeState = (direction: string) => {
        if (direction == 'forward'){
            if(step < 3){
                setStep(step + 1);
            }else{
                setStep(1);
            }
        }else{
            if(step >= 2){
                setStep(step - 1);
            }else{
                setStep(3);
            }
        }
    }

    const handleSelectState = (direction: number) => {
        setStep(direction);
    }

    let patient = props.contract.patient;
    let doctor = props.contract.doctor as InfoUser;
    let supervisor = props.contract.supervisor;
    let rights = [
        '1. Hệ thống hỗ trợ lưu trữ hồ sơ bệnh án của bệnh nhân chỉ để phục vụ cho việc khám chữa bệnh.',
        '2. Hệ thống đảm bảo tính riêng tư của những hồ sơ bệnh án trong quá trình khám chữa bệnh từ bác sĩ của hệ thống.',
        '3. Hệ thống đảm bảo việc giao tiếp giữa bệnh nhân và bác sĩ dựa trên nhắn tin hay gọi điện trực tuyến. Nhật ký trao đổi sẽ được ghi lại để làm bằng chứng cho những bất cập sau này.',
        '4. Bác sĩ đảm bảo lịch hẹn thăm khám, kiểm tra và cập nhật đơn thuốc với bệnh nhân căn cứ trên hợp đồng đã ký.',
    ];
    let duties = [
        '1. Bệnh nhân cần có trách nhiệm thực hiện các yêu cầu cần thiết và chia sẻ các y lệnh mà bác sĩ yêu cầu trong suốt quá trình khám chữa bệnh.',
        '2. Bệnh nhân cần đảm bảo việc thực hiện đầy đủ các y lệnh mà bác sĩ đưa ra trong suốt thời hạn hợp đồng.',
    ];
    let laws = [
        '- Căn cứ Bộ luật Dân sự ngày 14 tháng 6 năm 2005;',
        '- Căn cứ Luật khám bệnh, chữa bệnh ngày 23 tháng 11 năm 2009;',
        '- Căn cứ Nghị định số 87/2011/NĐ-CP ngày 27 tháng 9 năm 2011 của Chính phủ quy định chi tiết và hướng dẫn thi hành một số điều của Luật khám bệnh, chữa bệnh;',
    ];
    let claims = [
        'Sau khi thỏa thuận, Hai bên thống nhất ký kết hợp đồng khám, chữa bệnh theo các điều khoản cụ thể như sau:',
        'Tôi xác nhận tất cả các thông tin chia sẻ là sự thật và hoàn toàn chịu trách nhiệm trước phấp luật.',
    ];
    let articles = [
        'Điều 1: Thời hạn và nhiệm vụ hợp đồng:',
        'Điều 2: Chế độ thăm khám và theo dõi:',
        'Điều 3: Nghĩa vụ và quyền lợi của bên A',
        '1. Quyền lợi của bên A',
        '2. Nghĩa vụ của bên A',
        'Điều 4: Nghĩa vụ và quyền lợi của bên B',
        '1. Quyền lợi của bên B',
        '2. Nghĩa vụ của bên B',
        'Điều 5: Giải quyết tranh chấp',
        'Điều 6: Tiền dịch vụ và phương thức thanh toán',
        'Điều 7: Cam kết chung',
    ];
    let contents = [
        'Từ ngày: '.concat(moment(props.contract.startedAt).format('LLL'), ' - Đến ngày: ', moment(props.endDate).format('LLL').slice()),
        'Bên B sẽ sử dụng hệ thống HiDoctor để hỗ trợ khám và tư vấn cho bên A.',
        'a) Bên A được khám, tư vấn, và theo dõi dưới sự giám sát của bên B.',
        'b) Bên A được đề xuất, khiếu nại, đề nghị thay đổi hoặc chấm dứt hợp đồng.',
        'c) Bên A có thể chấm dứt hợp đồng bất cứ khi nào.',
        'a) Bên A cần cung cấp những thông tin cần thiết cho bên B để có thể theo dõi và khám chữa bệnh.',
        'b) Bên A cần đảm bả0 hoàn thành những nghĩa vụ đã cam kết trong hợp đồng giữa hai bên theo các điều mục 5 và 6 bên dưới.',
        'c) Bên A cần phối hợp theo đúng chỉ định của bên B về việc khám và chữa bệnh.',
        'd) Bên A cần chấp hành nội quy, quy chế theo quy định của bộ y tế về việc tổ chức khám chữa bệnh.',
        'a) Yêu cầu bên A cung cấp và chia sẻ các thông tin cần thiết cho việc khám chữa bệnh.',
        'b) Bên B có thể đơn phương chấm dứt hợp đồng khi có bằng chứng việc bên A có những sai phạm trong các điều khoản 5 và 6 cũng như các nghĩa vụ mà bên A phải thực hiện, hoặc sai phạm luật của bộ y tế theo nghị định số 87/2011/NĐ-CP ngày 27 tháng 9 năm 2011 cũng như không tuân thủ các quy định được đưa ra trong ứng dụng HiDoctor, gây ảnh hưởng tới việc không thể theo dõi và chăm sóc bệnh nhân.',
        'a) Xác nhận quá trình theo quy định của Luật khám bệnh, chữa bệnh ngày 23 tháng 11 năm 2009; Nghị định số 87/2011/NĐ-CP ngày 27 tháng 9 năm 2011 của Chính phủ quy định chi tiết và hướng dẫn thi hành một số điều của Luật khám bệnh, chữa bệnh và Thông tư số 41/2011/TT-BYT ngày 14 tháng 11 năm 2011 của Bộ trưởng Bộ Y tế Hướng dẫn cấp chứng chỉ hành nghề đối với người hành nghề và cấp giấy phép hoạt động đối với cơ sở khám bệnh, chữa bệnh.',
        'b) Đảm bảo thực hiện đầy đủ những điều đã cam kết trong hợp đồng làm việc.',
        'c) Không được chấm dứt hợp đồng nếu bên A không sai phạm các điều luật đã quy định trong hợp đồng.',
        'd) Khi bên B tự động chấm dứt hợp đồng trước thời hạn, phải bồi thường cho bên A theo quy định của pháp luật.',
        '1. Khi có tranh chấp, hai bên thống nhất giải quyết trên nguyên tắc bình đẳng, hợp tác, hòa giải. Trong thời gian tranh chấp, hai Bên cần phải bảo đảm điều kiện để khám bệnh, chữa bệnh đầy đủ.',
        '2. Trường hợp hai Bên không hòa giải được sẽ báo cáo cơ quan có thẩm quyền giải quyết.',
        '1 Phí tiền dịch vụ: Được cập nhật sau khi bác sĩ phê duyệt',
        '2 Phương thức thanh toán: Thanh toán trực tiếp vào tài khoản của HiDoctor thông qua VNPAY.',
        '1. Hai bên cam kết thực hiện đúng những điều khoản trong hợp đồng, những vấn đề phát sinh khác ngoài hợp đồng, kể cả việc kéo dài hoặc chấm dứt hợp đồng trước thời hạn sẽ được hai bên cùng thảo luận giải quyết, thể hiện bằng việc ký kết một hợp đồng mới, hợp đồng hiện hành sẽ hết hạn kể từ khi hợp đồng mới được ký.',
        '2. Hai bên thống nhất việc sử dụng ứng dụng HiDoctor cho việc khám chữa bệnh và tuân thủ các quy định liên quan tới phần mềm để hỗ trợ việc theo dõi bệnh.',
    ];
    let notes = [
        'Hợp đồng này hiện là bản nháp trước khi có sự ký kết của hai bên.',
    ];

    const handleSubmission = () => {
        if(isApprove)
            props.onFinalize();
        return;
    }

    return (
        <div className='contract_policy_rule'>
            {
            step === 1 && <div className='contract_claim'>
                <div className='contract_claim_content'>
                    <h6 className='bold_text'>Quyền lợi chung</h6>
                    {
                        rights.map(c => {
                            return <p>{c}</p>
                        })
                    }
                </div>
                <div className='contract_claim_content'>
                    <h6 className='bold_text'>Nghĩa vụ chung</h6>
                    {
                        duties.map(c => {
                            return <p>{c}</p>
                        })
                    }
                </div>
            </div>}
            { 
            step === 2 && <div className='policy_container'>
                <h5 className='text_center'>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</h5>
                <h6 className='text_center'>Độc lập - tự do - hạnh phúc</h6>
                <h4 className='text_center'>HỢP ĐỒNG KHÁM CHƯA BỆNH</h4>
                <div className='policy_rule_base'>
                    {
                        laws.map(r => { return <p>{r}</p> })
                    }
                </div>
                <div className='contract_sides'>
                    <div className='half_side'>
                        <h6 className='title'>Bên A - {patient.lastName.concat(' ', patient.firstName)}(Bệnh nhân)</h6>
                        <p>Ngày sinh: {moment(patient.dob).format('dd-MM-yyyy')}</p>
                        <p>Giới tính: {patient.gender?.toLowerCase().trim() === 'male' ? "Nam" : patient.gender?.toLowerCase().trim() === 'female' ? "Nữ" : "Khác"}</p>
                        <p>Địa chỉ: {patient.address}</p>
                    </div>
                    <div className='half_side'>
                        <h6 className='title'>Bên B - {doctor !== undefined ? doctor.lastName!.concat(' ', doctor!.firstName as string) : ""}(Bác sĩ)</h6>
                        <p>Ngày sinh: {moment(doctor.dob).format('dd-MM-yyyy')}</p>
                        <p>Giới tính: {doctor.gender?.toLowerCase().trim() === 'male' ? "Nam" : patient.gender?.toLowerCase().trim() === 'female' ? "Nữ" : "Khác"}</p>
                        <p>Địa chỉ: {doctor.address}</p>
                    </div>
                </div>
                <div className='policies'>
                    <div className='policies_right'>
                        <h5 className='title'>Điều khoản hợp đồng giữa bệnh nhân - giám hộ và bác sĩ</h5>
                        <div>
                            <h6 className="bold_text">{articles[0]}</h6>
                            <p>{contents[0]}</p>
                        </div>
                        <div>
                            <h6 className="bold_text">{articles[1]}</h6>
                            <div>
                                {
                                    contents.slice(1, 2).map(c => {
                                        return <p>{c}</p>
                                    })
                                }
                            </div>
                        </div>
                        <div>
                            <h6 className="bold_text">{articles[2]}</h6>
                            <h6 className="bold_text">{articles[3]}</h6>
                            {
                                contents.slice(2, 5).map(c => {
                                    return <p>{c}</p>
                                })
                            }
                        </div>
                        <div>
                            <h6 className="bold_text">{articles[4]}</h6>
                            {
                                contents.slice(5, 9).map(c => {
                                    return <p>{c}</p>
                                })
                            }
                        </div>
                        <div>
                            <h6 className="bold_text">{articles[5]}</h6>
                            <div>
                                <h6 className="bold_text">{articles[6]}</h6>
                                {
                                    contents.slice(9, 11).map(c => {
                                        return <p>{c}</p>
                                    })
                                }
                            </div>
                            <div>
                                <h6 className="bold_text">{articles[7]}</h6>
                                {
                                    contents.slice(11, 15).map(c => {
                                        return <p>{c}</p>
                                    })
                                }
                            </div>
                            <div>
                                <h6 className="bold_text">{articles[8]}</h6>
                                <div>
                                    {
                                        contents.slice(15, 17).map(c => {
                                            return <p>{c}</p>
                                        })
                                    }
                                </div>
                            </div>
                            <div>
                                <h6 className='bold_text'>{articles[9]}</h6>
                                <div>
                                    {
                                        contents.slice(17, 19).map(c => {
                                            return <p>{c}</p>
                                        })
                                    }
                                </div>
                            </div>
                            <div>
                                <h6 className="bold_text">{articles[10]}</h6>
                                <div>
                                    {
                                        contents.slice(19).map(c => {
                                            return <p>{c}</p>
                                        })
                                    }
                                </div>
                            </div>
                            <div>
                                <h6 className="bold_text">{rights[10]}</h6>
                                <div>
                                    {
                                        contents.slice(19).map(c => {
                                            return <p>{c}</p>
                                        })
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>}
            <div className='carousel'>
                    <div className='carousel_control'>
                        <div className={`carousel_control_button ${step === 1 ? 'carousel_control_active':''}`} onClick={e => handleSelectState(1)}></div>
                        <div className={`carousel_control_button ${step === 2 ? 'carousel_control_active':''}`} onClick={e => handleSelectState(2)}></div>
                    </div>
            </div>
            <div className='approve_section'>
                <div className='approve_checkbox'>
                    <input className='check_approve' type={'checkbox'} onChange = {e => {
                        if (e.currentTarget.checked)
                            setIsApprove(true);
                        else {
                            setIsApprove(false);
                        }
                    }} /> <span>Tôi đồng ý với điều khoản và chính sách của hợp đồng</span>
                </div>
                <div className='approve_action'>
                    <button className='btnApproval'disabled={!isApprove} onClick={e => {handleSubmission()}}>Chấp thuận</button>
                </div>
            </div>
        </div>
    )
}


export const ApprovalModal = (props: { contract: ITreamtentContract, close: () => void, rerender: () => void}) => {
    const [sessions, setSession] = useState<any[]>([])
    const [endContract, setEndContract] = useState<string>('')
    const [confirm, setConfirm] = useState<boolean>(false)
    const [step, setStep] = useState(1)
    const [steps, setSteps] = useState(["Thiết lập lịch khám - điều trị", "Xác nhận hợp đồng"])


    const apiSubmit = async () => {
        let body = approveRequestBody(sessions, endContract);
        console.log('submit body schedule',body);
        if(body !== undefined && endContract.trim() !== ''){
            approveContract(props.contract.id, body).then((res) => {
            props.close();

            }).catch(e => {
                console.error('error approval', e);
            });
        }else{
            return;
        }
    }

    return (
        <div className='approval_modal_container'>
            <div className='approval_modal_content'>
                <div className='approval_modal_content_header'>
                    <h6 className='step_header'>Bước {step} trên 2: {steps[step - 1]}</h6>
                    <div className='close'><FontAwesomeIcon icon={faClose} size='2x' className='approval_modal_content_header_close' fixedWidth onClick={e => {props.close()}}/></div>
                </div>
                <div className='horizontal_divider'></div>
                <div className='approval_modal_content_body'>
                    {
                        step === 1 && <SelectedSchedules contract={props.contract} onSubmit={setSession} onChangeEnd={setEndContract} next={setStep} />
                    }
                    {
                        step === 2 && <AcceptRule contract={props.contract} onSign={setConfirm} onFinalize={apiSubmit} endDate={endContract}></AcceptRule>
                    }
                </div>
            </div>
        </div>
    )
}
