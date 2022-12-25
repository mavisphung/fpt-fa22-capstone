import { ITreamtentContract } from "models/contract";

export const validSessionCreateForm = (startTime:string|Date|undefined, endTime:string|Date|undefined, date: string|Date|undefined, contract:ITreamtentContract) => {
    let hasError = false;
    let timeError = '';
    let dateError = '';

    if(date === undefined || date < contract.startedAt){
        dateError = 'Ngày diễn ra buối theo dõi - đánh giá - điểu trị phải nằm trong những ngày hợp đồng có hiệu lực';
        hasError = true;
    }

    if(startTime === undefined || endTime === undefined){
        timeError = 'Cần chọn thời điểm diễn ra';
        hasError = true;
    }
    return {
        'isError': hasError,
        'timeError': timeError,
        'dateError': dateError,
    }
}