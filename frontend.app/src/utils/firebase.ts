// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: 'AIzaSyB3rXSLDAfGyhzefFhh07JXnL0FcrIpYuw',
  authDomain: 'capstone-95504.firebaseapp.com',
  projectId: 'capstone-95504',
  storageBucket: 'capstone-95504.appspot.com',
  messagingSenderId: '162922742863',
  appId: '1:162922742863:web:1c70b179c82ac5b14c963a',
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = getMessaging(firebaseApp);

export const getMyToken = () => {
  return getToken(messaging, {
    vapidKey:
      'BIWKLxXOgNHa2ceDOYbpWC4iErgICy6Be-vB61G7Wj_QWQDEPhI0-Rx-kKeqr6i4aDPdTRXVre3wWwG8t3b2ppE',
  })
    .then((currentToken) => {
      if (currentToken) {
        console.log('current token for client: ', currentToken);

        // Track the token -> client mapping, by sending to backend server
        // show on the UI that permission is secured
      } else {
        console.log('No registration token available. Request permission to generate one.');

        // shows on the UI that permission is required
      }
    })
    .catch((err) => {
      console.log('An error occurred while retrieving token. ', err);
      // catch error while creating client token
    });
};

export const onMessageListener = () =>
  new Promise((resolve) => {
    onMessage(messaging, (payload) => {
      resolve(payload);
      // console.log('Message received. ', payload);
    });
  });

export const requestPermission = () => {
  console.log('Requesting permission...');

  Notification.requestPermission().then(async (permission) => {
    if (permission === 'granted') {
      console.log('Notification permission granted.');
      await getMyToken();
      // TODO(developer): Retrieve a registration token for use with FCM.
      // In many cases once an app has been granted notification permission,
      // it should update its UI reflecting this.
    } else {
      console.log('Unable to get permission to notify.');
    }
  });
};
