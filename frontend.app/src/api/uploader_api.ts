import axios, { AxiosRequestConfig } from 'axios'
import { imageHeader, jsonHeaders, requestOption } from 'constants/HeadersRequest';
import { urlApi } from 'constants/UrlApi';
import { config } from 'process';
import { InputFiles } from 'typescript';

requestOption.headers = imageHeader
requestOption.method = 'PUT'

const prepareParams = (files: File[]) => {
    let i = 0;
    let result: {
        'images': {
            ext: string,
            size: number,
        }[]
    } = {
        'images': []
    }
    let meta: {ext: string,
        size: number}[] = files.map((file) => {
        let name = file.name
        let fileExt = file.name.slice(name.lastIndexOf('.')+ 1)
        let fileSize = file.size / (1024 * 1024)
        return {
            ext: fileExt,
            size: fileSize
        }
    })
    files.forEach((file) =>{
        let name = file.name
        let fileExt = file.name.slice(name.lastIndexOf('.') + 1)
        console.log(fileExt)
    })
    result.images = result.images.concat(meta)
    return result;
}

export const uploadImage = async (files: File[]) => {
    let result = prepareParams(files);
    let response = await axios.post(urlApi + 'get-presigned-urls/', result, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
    let urls: string[] = response.data.data.urls as string[]

    let promise = urls.map((url, index) => {
        return axios.put(url, files[index], {
            headers: { 'Content-Type': 'image/jpeg' }
        })
            .then((res) => { console.log(res) })
            .catch((err) => { console.log(err) })
    })
    Promise.all(promise)
    return urls;
}