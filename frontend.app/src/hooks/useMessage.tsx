import React from 'react';
import { getMessages } from 'config/firebase';

export function useMessage(room:string){
    const [messages,setMessages] = React.useState([]);
    React.useEffect(()=>{
        const unsubscribe = getMessages(room, setMessages);
        return unsubscribe;
    },[room]);
    return messages;
}