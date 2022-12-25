// Scripts for firebase and firebase messaging
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

// Initialize the Firebase app in the service worker by passing the generated config
var firebaseConfig = {
  apiKey: 'AIzaSyB3rXSLDAfGyhzefFhh07JXnL0FcrIpYuw',
  authDomain: 'capstone-95504.firebaseapp.com',
  projectId: 'capstone-95504',
  storageBucket: 'capstone-95504.appspot.com',
  messagingSenderId: '162922742863',
  appId: '1:162922742863:web:1c70b179c82ac5b14c963a',
};

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function (payload) {
  // console.log('Received background message ', payload);


  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
