import { current } from "@reduxjs/toolkit";
import { createContractSession, getWorkingShift, ITreatmentSessionRequest, suggestDoctorHour } from "api/sessionApi";
import { CustomDatePicker } from "components/common/DatetimePicker";
import { validSessionCreateForm } from "features/contract/util/validation";
import { ITreamtentContract, ITreatmentSession } from "models/contract";
import moment from "moment";
import { ChangeEvent, KeyboardEvent, useEffect, useState } from "react";
import { ShiftTimes } from '../../../../models/shiftTime'
export const SessionForm = (props: { contract: any | ITreamtentContract }) => {
    let max = new Date(props.contract.endedAt);
    max.setDate(max.getDate() + 1);
    const [date, setDate] = useState<string | Date>(props.contract.startedAt)
    const [startTime, setStartTime] = useState<string | undefined>()
    const [endTime, setEndTime] = useState<string | undefined>()
    const [notes, setNotes] = useState<Array<any | string>>([])
    const [suggestions, setSuggestions] = useState<Array<any | object>>([])
    const asyncCreateSession = async (request: ITreatmentSessionRequest) => {
        createContractSession(request).then(res => {
            console.log('success', res);
        }).catch(err => {
            console.error(err)
        });
    }

    useEffect(() => {
        asyncGetSuggestion(new Date(date).toISOString().slice(0,10));
    },[])


    const calculateSuggestionsInShift = (shift: any, selectedDate: any) => {
        console.log(shift)
        let currentDate = new Date(selectedDate);
        let currentDateCopy = new Date(selectedDate);
        let hours: any[] = shift.startTime.split(':');
        currentDate.setHours(hours[0], hours[1], 0)
        hours = shift.endTime.split(':');
        currentDateCopy.setHours(hours[0], hours[1], hours[2], 0)
        let result: any[] = []
        while (currentDate.getTime() < currentDateCopy.getTime()) {
            let from = new Date(currentDate.toLocaleString());
            currentDate.setMinutes(currentDate.getMinutes() + 15, 0);
            let slot = {
                'from': from.toLocaleString('vi-VI').slice(0, 5).trim(),
                'to': currentDate.toLocaleString('vi-VI').slice(0, 5).trim(),
            }
            result = [...result, slot];
        }
        console.log('result', result);
        return result;
    }

    const handleSlotAvaliableTime = (slot: any, selectedDate: string) => {
        let from: moment.Moment = moment(slot.from, 'hh:mm').utcOffset("+07:00", true);
        let to: moment.Moment = moment(slot.to, 'hh:mm').utcOffset("+07:00", true);
        let duration: moment.Duration = moment.duration(to.diff(from));
        if (duration.asMinutes() > 15) {
            let result: any[] = [];
            let current = from;
            let array = new Array(Math.floor(duration.asMinutes() / 15))
            let i = 0;
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
            return result;

        } else {
            return []
        }
    }

    const asyncGetSuggestion = async (selectedDate: any) => {
        if (selectedDate === undefined) {
            return;
        }
        await suggestDoctorHour(selectedDate).then(res => {
            console.log('response data', res.data.data);
            if (res.data.data === undefined || res.data.data.length === undefined) {
                getWorkingShift().then(res => {
                    let shiftOfWeeks: Map<string, ShiftTimes> = new Map<string, ShiftTimes>(Object.entries(res.data.data))
                    let weekday = new Date(selectedDate).getDay() + 1;
                    let shiftsOfDay = shiftOfWeeks.get(weekday.toString());
                    if (shiftsOfDay!.length > 0) {
                        let map = shiftsOfDay!.map(s => {
                            return calculateSuggestionsInShift(s, selectedDate);
                        }).flat(1);
                        setSuggestions(map);
                    } else {
                        console.log(shiftsOfDay);
                    }

                }).catch(e => {
                    console.log(e);
                });
                return;
            }
            let preCutRange: any[] = res.data.data;
            let cutedRange = preCutRange.map((slot) => handleSlotAvaliableTime(slot, selectedDate)).flat(1)
            setSuggestions(cutedRange);
        }).catch(e => {
            console.log('errror', e)
        });
    }

    const handleTimeInput = (start: any, end: any) => {
        setStartTime(start);
        setEndTime(end);
    }

    const handleChangeDate = (date: string, lte: string) => {
        setDate(date);
        setStartTime(undefined);
        setEndTime(undefined);
        asyncGetSuggestion(moment(new Date(date)).toISOString().slice(0, 10));
    }

    const handleSubmit = async () => {
        let startTimeSlot = moment(date.toString().slice(0,10).concat(' ',startTime!.toString()), "YYYY-MM-DD HH:mm").format('yyyy-MM-DD HH:mm:ss')
        let endTimeSlot = moment(date.toString().slice(0,10).concat(' ',endTime!.toString()), "YYYY-MM-DD HH:mm").format('yyyy-MM-DD HH:mm:ss')
        console.log(startTimeSlot , endTime, date.toString().slice(0,10) + '|')
        validSessionCreateForm(startTime, endTime, date, props.contract);
        await asyncCreateSession({
            assessment: [],
            note: notes,
            contract: props.contract.id,
            endTime: endTimeSlot,
            patient: props.contract.patient.id,
            startTime: startTimeSlot,
        });
    }

    const handleAddNotes = (event: KeyboardEvent<HTMLInputElement>) => {
        console.log(event.code, event.key)
        if (event.currentTarget.value.trim() === '') {
            return;
        }
        if (event.key.toLowerCase().trim() === 'enter') {
            let result = notes.concat(event.currentTarget.value);
            console.log(event.currentTarget.value, event.key, result);

            setNotes(result)
        }
    }

    return (
        <div className="session_creation_form">
            <div className="session_creation_form_header">
                <h6>Thêm buổi theo dõi đánh giá/điều trị</h6>
            </div>
            <div className="session_creation_form_content">
                <div className="field">
                    <h6>Ngày hẹn</h6>
                    <CustomDatePicker changeDate={handleChangeDate} selectedDate={date as string} comparator='lte' />
                </div>
                <div className="field field--suggestion">
                    <h6>Khung giờ: {startTime && endTime ? <span>{startTime} - {endTime}</span> : <span>Chưa có khung giờ được chọn</span>}</h6>
                    {
                        suggestions && suggestions.length > 0 ? suggestions.map((s, index) => <div key={index} className="suggestion" onClick={e => { handleTimeInput(s.from, s.to) }}>
                            {s.from} - {s.to}
                        </div>
                        ) : <p>Không có khung giờ trống trong ngày </p>}
                </div>
                <div className="field">
                    <h6>Chú thích</h6>
                    <input className="text_input" type={'text'} onKeyDown={handleAddNotes} />
                    <div className="field field--note">
                        <h6>Chú thích đã thêm:</h6>
                        {
                            notes && notes.length > 0 ? notes.map((s, index) => <div key={index} className="note" onClick={e => { }}>
                                <p>{s}</p>
                            </div>
                            ) : <p>Chưa có chú thích được thêm vào</p>
                        }
                    </div>
                </div>
                <div className="field">
                    <button className="btnAction" onClick={e => { handleSubmit()}}>Thêm buổi đánh giá - điều trị</button>
                </div>
            </div>
        </div>
    )
}