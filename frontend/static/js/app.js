/*
=========================================================
SRG.ai
Main Application Controller
=========================================================
*/

import { initializeUI } from "./ui.js";
import { initializeHistory } from "./history.js";
import { initializeTheme } from "./theme.js";
import { initializeVoice } from "./voice.js";
import { initializeFirebase } from "./firebase.js";
import { initializeChat } from "./chat.js";

/*-------------------------------------------------------
Initialize Quick Prompts
-------------------------------------------------------*/

function initializeQuickPrompts() {

    const prompts = document.querySelectorAll(".quick-prompt");
    const messageInput = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    if (!prompts.length || !messageInput || !sendBtn) return;

    prompts.forEach(button => {

        button.addEventListener("click", () => {

            const prompt = button.dataset.prompt;

            if (!prompt) return;

            messageInput.value = prompt;

            messageInput.focus();

            messageInput.dispatchEvent(new Event("input"));

            sendBtn.click();

        });

    });

}

/*-------------------------------------------------------
Application Startup
-------------------------------------------------------*/

document.addEventListener("DOMContentLoaded", () => {

    console.group("🚀 SRG.ai Startup");

    try {

        initializeUI();
        console.log("✅ UI Initialized");

        initializeHistory();
        console.log("✅ History Initialized");

        initializeTheme();
        console.log("✅ Theme Initialized");

        initializeVoice();
        console.log("✅ Voice Initialized");

        initializeFirebase();
        console.log("✅ Firebase Initialized");

        initializeChat();
        console.log("✅ Chat Initialized");

        initializeQuickPrompts();
        console.log("✅ Quick Prompts Initialized");

        console.log("🎉 SRG.ai Started Successfully");

    }
    catch (error) {

        console.error("❌ SRG.ai Initialization Failed");

        console.error(error);

    }

    console.groupEnd();

});