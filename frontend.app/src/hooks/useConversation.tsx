import React from "react"
import {getConversation} from 'config/firebase'

export const useConversation = (doctorId:number) => {
    const [conversations, setConversations] = React.useState([])
    React.useEffect(() => {
       getConversation(doctorId, setConversations)
    },[doctorId])
    return conversations
} 