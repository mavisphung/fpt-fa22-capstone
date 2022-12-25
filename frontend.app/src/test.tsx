import { AxiosResponse } from 'axios'
import { HealthRecord } from 'models/health_record'
import { useState, useEffect } from 'react'
import { loadHealthRecordByContract } from '../src/api/health_record_api'
export const Test = () => {
    const [healthRecords, setHealthRecords] = useState<any>(null)

    const init= () =>{
        let data: Promise<any> = loadHealthRecordByContract(1)
        data.then((response) =>{
            console.log('fulfilled', response)
            setHealthRecords(response.data)
        })
    }

    useEffect(() => {
        init()
    }, [])

    return (
        <>
        {
            healthRecords?.map((record:any) => {
                return <p>{record.recordId}</p>
            })
        }
        </>
    )
}