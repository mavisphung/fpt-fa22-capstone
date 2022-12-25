// Import the functions you need from the SDKs you need
import { getChatMemberInfo } from "api/userApi";
import { initializeApp} from "firebase/app";
import { addDoc, collection, CollectionReference, doc, DocumentReference, getDoc, getDocs, getFirestore, onSnapshot, orderBy, query, updateDoc, where } from 'firebase/firestore';
import { InfoUser } from "models/infoUser";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB3rXSLDAfGyhzefFhh07JXnL0FcrIpYuw",
  authDomain: "capstone-95504.firebaseapp.com",
  projectId: "capstone-95504",
  storageBucket: "capstone-95504.appspot.com",
  messagingSenderId: "162922742863",
  appId: "1:162922742863:web:1c70b179c82ac5b14c963a"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export async function sendToAppointment(id:number, supervisorId: number, doctorId: number, text: string, type: number) {
    await addDoc(collection(db,'messages', id.toString(),id.toString()), {
        senderId:doctorId,
        receiverId:supervisorId,
        content: text,
        type: type,
        createdAt: new Date().getTime()
    }).catch(e => console.log(e))
}

export async function sendMessage( supervisorId:number, doctorId:number, text:string, type: number){
    let room = supervisorId.toString().concat('-',doctorId.toString())
    console.log('room to send ', room);
    const roomDocRef = doc(db, "messages", room);
    updateDoc(roomDocRef, {
        'lastMessage': text
    })

    await addDoc(collection(db,'messages', room,room), {
        senderId:doctorId,
        receiverId:supervisorId,
        content: text,
        type: type,
        createdAt: new Date().getTime()
    })
    // await addDoc(collection(db,'messages),{
    //     senderId:senderId,
    //     receiverId:receiverId,
    //     content: text,
    //     type: type,
    //     createdAt: new Date().getTime()
    // })
}

export function getMessages(room:string, callback:any){
    return onSnapshot(query(collection(db, 'messages', room, room),orderBy('createdAt','asc')),(snapshot) => {
        const messages = snapshot.docs.map(doc => ({
            id: doc.id,
            proposalText: '',
            proposalFile: [],
            ...doc.data(),
        }))
        callback(messages)
    })
}


export async function getConversation(doctorId: number, callback: any){
    let ref = collection(db,'messages')
    let query2 = query(ref, where('doctorId', "==", 5))
    let snapspot = await getDocs(query2)
    return onSnapshot(query2, (snapshot) => {
        const conversation = snapshot.docs.map(doc => ({
            ...doc.data(),
        }))
        callback(conversation)
    })
}