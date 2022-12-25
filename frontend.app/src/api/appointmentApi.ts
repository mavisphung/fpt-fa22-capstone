import axios, { AxiosRequestConfig } from 'axios';
import { AppointmentPayload } from 'features/appointment/appointmentSlice';
import { IAppointmentFilter } from 'models/appointment';
import { localUrl, urlApi } from 'constants/UrlApi';

const createAppointmentRequestBody = (
  checkInCode: string | null,
  action: string,
  paymentTransaction?: any,
  returnTransaction?: any
) => {};

const config: AxiosRequestConfig = {
  baseURL: urlApi,
  headers: {
    Authorization: `Bearer ${localStorage.getItem('access_token')!}`,
    'Content-Type': 'application/json',
  },
};

const generateParams = (map: object) => {
  let param = '';
  for (const [key, value] of Object.entries(map)) {
    console.log(key, value);
    if (value !== undefined && value !== null) {
      param = param.concat(key, '=', value, '&');
    }
  }
  return param.slice(0, param.length - 1);
};

export const loadAppointment = async (filter: IAppointmentFilter) => {
  return await axios.get(urlApi + `appointments/doctor/?${generateParams(filter)}`, config);
};

export const checkInAppointment = async (id: number, checkInCode: string | null) => {
  let body = createAppointmentRequestBody(checkInCode, 'checkIn');
  return await axios.post(urlApi + `appointments/doctor/${id}`, body, config);
};

export const completeAppointment = async (id: number) => {
  let body = createAppointmentRequestBody(null, 'complete');
  return await axios.post(urlApi + `appointments/doctor/${id}`, body, config);
};

export const fetchAppointment = async (id: number) => {
  return await axios.get(urlApi + `appointments/${id}`,config);
};
