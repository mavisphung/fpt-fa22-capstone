import axios, {AxiosRequestConfig} from 'axios';
import { LoginPayload } from 'features/auth/authSlice';
import { localUrl, urlApi } from 'constants/UrlApi';

export const loginApi = async (user: LoginPayload) => await axios.post(urlApi + 'login/', user);

const config: AxiosRequestConfig = {
    baseURL: urlApi,
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')!}`,
        'Content-Type': 'application/json',
    },
}

export const getToken = async () => await axios.get(urlApi + 'user/me/agora-token/', config)


const configWithUnauthen: AxiosRequestConfig = {
    baseURL: urlApi,
    headers: {
        'Content-Type': 'application/json',
    },
}
export const getChatMemberInfo = async (userId: number) => await axios.get(urlApi + `/user?userId=${userId}`, configWithUnauthen)
