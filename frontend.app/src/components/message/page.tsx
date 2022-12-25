import { sendMessage } from "config/firebase";
import { useMessage } from "hooks/useMessage";
import { ChangeEvent, FormEvent, useRef, useState } from "react";



interface MessageItem {
    receiverId: number, 
    senderId: number, 
    content: string, 
    createdAt: Date, 
    type: number
}

function Message(props: { message: MessageItem, isOwnMessage: boolean }) {
    return (
        <li className={['message', props.isOwnMessage && 'own-message'].join(' ')}>
            <h4 className="sender">{props.isOwnMessage ? 'You' : props.message.senderId}</h4>
            <div>{props.message.content}</div>
        </li>
    );
}

export enum MessageType{
    text = 0,
    image = 1,
    file = 2,
    video = 3,
}

export const ChatRoom = (props: {
    room: string;
    sender: number;
    receiver: number;
}) => {
    const sender = props.sender
    const receiver = props.receiver
    const containerRef = useRef<HTMLDivElement>(null);
    const messages = useMessage(props.room);
    const [newMessage,setNewMessage] = useState("")

    const handleTextSumbit = (event: FormEvent<HTMLFormElement>) =>{
        event.preventDefault();
        sendMessage(sender, receiver, newMessage, MessageType.image)
        setNewMessage('')
    }

    const handleChangeNewMessage = (event: ChangeEvent<HTMLInputElement>) =>{
        setNewMessage(event.target.value)   
    }

    return (
        <div className="message-list-container" ref={containerRef}>
            <ul className="message-list">
                {messages.map((x: MessageItem) => (
                    <Message message={x} isOwnMessage = {sender === x.senderId}></Message>
                ))}
            </ul>
            <form onSubmit={e => handleTextSumbit(e)}>
                <input type="text" value={newMessage} onChange = {e => handleChangeNewMessage(e)}/>
            </form>
        </div>
    );
}



export const ChatPage = () => {
    return (<ChatRoom room="7-5" sender = {5} receiver= {7} />)
}