/*
=========================================================
SRG.ai
Firebase Controller
=========================================================
*/

import { initializeApp, getApps } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";

import {

    getAuth,
    GoogleAuthProvider,
    signInWithPopup,
    signOut,
    onAuthStateChanged

} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

/*-------------------------------------------------------
Firebase Configuration
-------------------------------------------------------*/

const firebaseConfig = {

    apiKey: "YOUR_API_KEY",

    authDomain: "YOUR_PROJECT.firebaseapp.com",

    projectId: "YOUR_PROJECT",

    storageBucket: "YOUR_PROJECT.firebasestorage.app",

    messagingSenderId: "YOUR_SENDER_ID",

    appId: "YOUR_APP_ID"

};

/*-------------------------------------------------------
Initialize Firebase
-------------------------------------------------------*/

const app = getApps().length
    ? getApps()[0]
    : initializeApp(firebaseConfig);

const auth = getAuth(app);

const provider = new GoogleAuthProvider();

let currentUser = null;

/*-------------------------------------------------------
Initialize Firebase
-------------------------------------------------------*/

export function initializeFirebase() {

    onAuthStateChanged(auth, (user) => {

        currentUser = user || null;

        if (currentUser) {

            console.log("✅ Logged in:", currentUser.displayName);

            updateProfile(currentUser);

        } else {

            console.log("👤 User not logged in");

            updateProfile(null);

        }

    });

}

/*-------------------------------------------------------
Google Login
-------------------------------------------------------*/

export async function loginWithGoogle() {

    try {

        const result = await signInWithPopup(auth, provider);

        currentUser = result.user;

        updateProfile(currentUser);

        return currentUser;

    }

    catch (error) {

        console.error("Google Login Failed", error);

        return null;

    }

}

/*-------------------------------------------------------
Logout
-------------------------------------------------------*/

export async function logout() {

    try {

        await signOut(auth);

        currentUser = null;

        updateProfile(null);

    }

    catch (error) {

        console.error("Logout Failed", error);

    }

}

/*-------------------------------------------------------
Current User
-------------------------------------------------------*/

export function getCurrentUser() {

    return currentUser;

}

/*-------------------------------------------------------
Is Logged In
-------------------------------------------------------*/

export function isLoggedIn() {

    return currentUser !== null;

}

/*-------------------------------------------------------
Authentication Listener
-------------------------------------------------------*/

export function onUserChanged(callback) {

    return onAuthStateChanged(auth, callback);

}

/*-------------------------------------------------------
Update Profile
-------------------------------------------------------*/

function updateProfile(user) {

    const profileImage =
        document.getElementById("profileImage");

    if (!profileImage) return;

    if (user && user.photoURL) {

        profileImage.src = user.photoURL;

        profileImage.alt = user.displayName || "User";

    } else {

        profileImage.src = "/static/images/logo.png";

        profileImage.alt = "SRG.ai";

    }

}