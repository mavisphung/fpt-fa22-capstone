import { sendMessage, getMessages } from 'config/firebase'
import { useConversation } from 'hooks/useConversation'
import { FormEvent, ChangeEvent, useEffect, useRef, useState, useReducer } from 'react'
import 'features/communication/conversation.scss'
import { getChatMemberInfo } from 'api/userApi'
import { groupBy, groupByVer2, MessgageGroup } from 'utils/utils'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faClose, faImage, faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import { current } from '@reduxjs/toolkit'
import { uploadImage } from 'api/uploader_api'

export interface ConverationMetadata {
    doctorId: number,
    supervisorId: number,
    lastMessage: string,
    lastTimeStamp: string,
    type: number,
    onClick?: any,
    proposalText?: string
    proposalFile?: string[]
    files?: File[]
}

export interface MessageItem {
    receiverId: number,
    senderId: number,
    content: string,
    createdAt: Date,
    type: number
}


export const Conversation = (props: { 'meta': ConverationMetadata, 'isSelected': boolean }) => {
    let conversation = props.meta
    let isSelected = props.isSelected
    const [guest, setGuest] = useState({
        'fullName': '',
        'avatar': ''
    })
    let dateFormatter = new Intl.DateTimeFormat('vi-VI', { dateStyle: 'full' })
    useEffect(() => {
        const init = async () => {
            let response = await (await getChatMemberInfo(conversation.supervisorId)).data
            console.log('chat member info', response)
            setGuest(response)
        }
        init()
    }, [])
    return (
        <div className={`conversation__list__detail ${isSelected ? 'conversation__list__detail--active' : ''}`} onClick={(e) => { conversation.onClick() }}>
            <img src={guest.avatar} className='conversation__list__detail__avatar'></img>
            <div className='conversation__list__detail__info'>
                <span className='room'>{guest.fullName}</span>
                <div className='last_message'>
                    <span className='last_message__content'>{conversation.lastMessage}</span>
                    <span className='last_message__timestamp'>{dateFormatter.format(Number.parseInt(conversation.lastTimeStamp))}</span>
                </div>
            </div>
        </div>
    )
}

function Messages(props: { message: MessageItem[], host: number, resize: boolean }) {
    const [conversation, setConversation] = useState({
        "guest": {
            'fullName': "",
            'avatar': ""
        },
        "host": {
            'fullName': "",
            'avatar': ""
        }
    })
    const [groupedMessages, setGroupedMessages] = useState<Array<MessgageGroup>>([])
    let messages = props.message
    useEffect(() => {
        const init = async () => {
            let host = props.host
            let guest = props.message.find((mess) => { return mess.senderId != host })?.senderId
            let guestResponse = (await getChatMemberInfo(guest!)).data;
            let hostResponse = (await getChatMemberInfo(host)).data;
            setConversation({
                host: hostResponse,
                guest: guestResponse
            })
            setGroupedMessages(groupByVer2(messages))
        }
        init()
    }, [props.message])
    return (
        <div className={`conversation__detail__messages ${props.resize ? 'conversation__detail__messages--resize' : ''}`}>
            {
                groupedMessages.map((messages) => {
                    let isOwn = messages.message[0].senderId === props.host
                    return <div className='message_line'>
                        <div className={`message_wrapper ${isOwn ? 'message_wrapper--own' : 'message_wrapper--guest'}`}>
                            {!isOwn ?
                                <div className='message_wrapper__avatar'>
                                    <img className='message_wrapper__avatar__img' src={`${isOwn ? conversation.host.avatar : conversation.guest.avatar}`} />
                                </div> : ''}
                            {
                                <div className={`message_wrapper__message ${isOwn ? 'message_wrapper__message--own' : ''}`}>
                                    {
                                        messages.type === 1 ? <div className='image_group'>
                                            {messages.message.map(msg => {
                                                return <img className={`message_wrapper__message__span message_wrapper__message__span--img ${isOwn ? 'message_wrapper__message__span_img--own' : ''}`} src={msg.content} />

                                            })}
                                        </div> : messages.message.map(msg =>
                                            <span className={`message_wrapper__message__span ${isOwn ? 'message_wrapper__message__span--own' : ''}`}>
                                                {msg.content}
                                            </span>
                                        )
                                    }
                                </div>
                            }
                        </div>
                    </div>
                })
            }
        </div>
    );
}

interface StyleReduceState{
    center: boolean;
    hasImage: boolean;
} 

interface StyleActionState{
    type: string;
    payload: StyleReduceState

}

const defaultStyle:StyleReduceState = {
    center: true,
    hasImage: false,
}

export const MessageList = (props: { doctorId: number }) => {
    const layoutReducer = (state:StyleReduceState,action:StyleActionState) => {
        switch(action.type){
            case 'ADD_MORE_MEDIA': {
                return {
                    center: true,
                    hasImage: true,
                }
            }
            case 'REMOVE_MEDIA':{
                return {
                    center: true,
                    hasImage: false,
                }
            }
            case 'TEXT_NEED_CENTER':{
                return {
                    center: true,
                    hasImage: false,
                }
            }
            default:{
                return state
            }
        }
    }
    const conversations = useConversation(props.doctorId);
    const [messages, setMessages] = useState([])
    const [selectedConversation, setSelectedConversation] = useState<ConverationMetadata>()
    const [messageLoading, setMessageLoading] = useState(true)
    const [center, setCenter] = useState(true)
    const [state, dispatch] = useReducer(layoutReducer, defaultStyle)
    const fieldRef = useRef<HTMLSpanElement>(null)
    let inputSpan = document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input')
    let messagesElement = document.getElementsByClassName('conversation__detail__messages').item(0) as HTMLElement
    useEffect(() => {
        let conversation = conversations[0] as ConverationMetadata
        if (conversation !== undefined && conversations !== undefined) {
            getMessages(conversation.supervisorId + '-' + conversation.doctorId, setMessages)
            setSelectedConversation(conversation)
            setMessageLoading(false)
        }
    }, [conversations])

    useEffect(() => {
        if (messagesElement !== undefined && messagesElement !== null) {
            messagesElement.scrollTop = messagesElement.scrollHeight;
        }
        if (selectedConversation !== undefined) {
            getMessages(selectedConversation.supervisorId + '-' + selectedConversation.doctorId, setMessages)
            if (selectedConversation?.files === undefined) {
                selectedConversation!.files = []
            }
        }
        if (fieldRef.current?.innerText !== undefined) {
            let text = selectedConversation?.proposalText as string;
            console.log('proposal Text', text)
            if (text) {
                fieldRef.current.innerText = text;
            } else {
                fieldRef.current.innerText = '';
            }
        }
    }, [selectedConversation])

    useEffect(() => {
        if (messagesElement !== undefined && messagesElement !== null) {
            messagesElement.scrollTop = messagesElement.scrollHeight;
        }
        console.log('effect with no dependencies')
    }, [])

    const handleTextOnChange = (conversation: ConverationMetadata, e: FormEvent<HTMLSpanElement>) => {
        let span_input = getComputedStyle(document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input').item(0) as Element);
        if (!inputSpan) {
            return
        }
        if (messagesElement) {
            messagesElement.style.height = `calc(100%  - ${span_input.height})`
        }
        if (state.hasImage) {
            messagesElement.style.height = `calc(100%  - ${span_input.height} - 70px)`
        }
        if (Number.parseInt(span_input.height) > 37) {
        } else {
        }
        conversation.proposalText = inputSpan.item(0)?.textContent as string
    }

    const handleChangeConversation = (conversation: ConverationMetadata) => {
        getMessages(conversation.supervisorId + '-' + conversation.doctorId, setMessages)
        setSelectedConversation(conversation);
    }

    const handleOnImageChange = (index: ConverationMetadata, e: ChangeEvent<HTMLInputElement>) => {
        if (e.currentTarget.files) {
            let files = e.currentTarget.files as FileList
            let span_input = getComputedStyle(document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input').item(0) as Element)
            let imgCacheUrls = selectedConversation?.proposalFile
            let conversationFile = selectedConversation?.files
            if (messagesElement) {
                messagesElement.style.height = `calc(100%  - ${span_input.height} - 70px)`
            }
            if (imgCacheUrls === undefined) {
                imgCacheUrls = []
            }
            if (conversationFile === undefined) {
                conversationFile = []
            }
            for (let i = 0; i < files.length; i++) {
                let file = files.item(i) as File
                imgCacheUrls.push(URL.createObjectURL(file))
                conversationFile.push(file)
            }
            selectedConversation!.proposalFile = imgCacheUrls
            selectedConversation!.files = conversationFile
            console.log('selectedConversation files', selectedConversation?.proposalFile)
            let updatedConversation = Object.assign({}, selectedConversation)
            setSelectedConversation(updatedConversation)
            dispatch({type: 'ADD_MORE_MEDIA', payload:{
                center: false,
                hasImage: true,
            }})
        }
        console.log('trigger input event')
    }

    const removeImage =  (selectedIndex:number) =>{
        let span_input = getComputedStyle(document.getElementsByClassName('conversation__detail__form__textAndPreview__text__input').item(0) as Element)
        if(selectedConversation){
            selectedConversation.files = selectedConversation?.files?.filter((value, index) => {
                return index != selectedIndex
            })
            selectedConversation.proposalFile = selectedConversation?.proposalFile?.filter((value, index) => {
                return index != selectedIndex
            })
            let updatedConversation = Object.assign({}, selectedConversation)
            if(selectedConversation.proposalFile?.length == 0){
                dispatch({type: 'REMOVE_MEDIA', payload: {center: true, hasImage:false}})
                if(span_input && messagesElement)
                    messagesElement.style.height =`calc(100% - ${span_input.height})`
            }
            setSelectedConversation(updatedConversation)
        }
    } 

    const handleSendMultiTypeMessage = async (selectedConversation: ConverationMetadata) => {
        let textMessage = selectedConversation.proposalText;
        let mediaFile = selectedConversation.files as File[];
        if(textMessage){
            sendMessage(selectedConversation.supervisorId, selectedConversation.doctorId, textMessage, 0)
        }
        if(mediaFile){
            let urls = await uploadImage(mediaFile)
            let urlMessages = urls.map(url => url.slice(0, url.lastIndexOf('?')))
            let imgPromise = urlMessages.map((imgUrl) => {
                return sendMessage(selectedConversation.supervisorId, selectedConversation.doctorId, imgUrl, 1)
            })
            Promise.all(imgPromise.concat(textMessage ? sendMessage(selectedConversation.supervisorId, selectedConversation.doctorId, textMessage, 0) : []))
        }
        selectedConversation.files = []
        selectedConversation.proposalFile = []
        selectedConversation.proposalText= undefined;
    }

    return (
        <div className='conversation'>
            <div className='conversation__list'>
                {
                    conversations.map((conversation: ConverationMetadata, index) => {
                        conversation.onClick = () => {
                            handleChangeConversation(conversation);
                        }
                        return <Conversation meta={conversation} isSelected={selectedConversation?.supervisorId === conversation.supervisorId} />
                    })
                }
            </div>
            <div className='conversation__detail'>
                {
                    !messageLoading ?
                        <Messages message={messages} host={props.doctorId} resize={false} /> : <p>Loading</p>
                }
                <div className={`conversation__detail__form`}>
                    <div className='conversation__detail__form__file'>
                        <label htmlFor='input_file' className={`file_label  ${state.center ? 'file_label--center' : ''}`}>
                            <FontAwesomeIcon icon={faImage} fixedWidth size='1x'></FontAwesomeIcon>
                        </label>
                        <input id='input_file' type={'file'} onChange={(e) => handleOnImageChange(selectedConversation as ConverationMetadata, e)}></input>
                    </div>
                    <div className='conversation__detail__form__textAndPreview' >
                        <div className={`conversation__detail__form__textAndPreview__preview ${state.hasImage ? 'conversation__detail__form__textAndPreview__preview--show' : ''}`}>
                            {selectedConversation !== undefined && selectedConversation!.proposalFile !== undefined ? selectedConversation!.proposalFile!.map(
                                (src, index) =>
                                    <div className='conversation__detail__form__textAndPreview__preview__item'>
                                        <span className='icon'><FontAwesomeIcon icon={faClose} size='1x' fixedWidth onClick={(e) => {removeImage(index)}} color={'#000000'}/></span>
                                        <img src={src} className='conversation__detail__form__textAndPreview__preview__item' />
                                    </div>

                            ) : <></>
                            }
                        </div>
                        <div className='conversation__detail__form__textAndPreview__text'>
                            <span className='conversation__detail__form__textAndPreview__text__input' contentEditable onInput={e => { handleTextOnChange(selectedConversation as ConverationMetadata, e) }} ref={fieldRef}></span>
                        </div>
                    </div>
                    <div className='conversation__detail__form__button'>
                        <div className={`conversation__detail__form__button__icon  ${state.center ? 'conversation__detail__form__button__icon--center' : ''}`} onClick={(e) => {
                            handleSendMultiTypeMessage(selectedConversation as ConverationMetadata)
                        }}>
                            <FontAwesomeIcon icon={faPaperPlane} size='1x' fixedWidth />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}