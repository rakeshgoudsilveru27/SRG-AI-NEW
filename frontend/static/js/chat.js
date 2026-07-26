/*
=========================================================
SRG.ai
Chat Controller
=========================================================
*/

import { addMessage } from "./history.js";
import {
    hideTyping,
    showTyping,
    hideWelcome,
    scrollToBottom
} from "./ui.js";

const API_URL = "/api/chat";

let chatArea;
let messageInput;
let sendBtn;

let isSending = false;

/*-------------------------------------------------------
Initialize
-------------------------------------------------------*/

export function initializeChat() {

    chatArea = document.getElementById("chatArea");
    messageInput = document.getElementById("messageInput");
    sendBtn = document.getElementById("sendBtn");

    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessage);
    }

    if (messageInput) {

        messageInput.addEventListener("keydown", (event) => {

            if (event.key === "Enter" && !event.shiftKey) {

                event.preventDefault();

                sendMessage();

            }

        });

    }

}

/*-------------------------------------------------------
Send Message
-------------------------------------------------------*/

async function sendMessage() {

    if (isSending) return;

    const message = messageInput.value.trim();

    if (!message) return;

    isSending = true;

    sendBtn.disabled = true;
    messageInput.disabled = true;

    hideWelcome();

    addUserMessage(message);

    addMessage("user", message);

    messageInput.value = "";
    messageInput.style.height = "auto";

    showTyping();

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message
            })

        });

        if (!response.ok) {

            const errorText = await response.text();

            throw new Error(errorText);

        }

        const data = await response.json();

        if (!data || typeof data.reply !== "string") {

            throw new Error("Invalid server response.");

        }

        const reply = data.reply.trim();

        hideTyping();

        addAIMessage(reply);

        addMessage("assistant", reply);

    }

    catch (error) {

        hideTyping();

        const errorMessage = "⚠ Unable to connect to SRG.ai server.";

        addAIMessage(errorMessage);

        console.error(error);

    }

    finally {

        isSending = false;

        sendBtn.disabled = false;

        messageInput.disabled = false;

        messageInput.focus();

        scrollToBottom();

    }

}

/*-------------------------------------------------------
User Message
-------------------------------------------------------*/

function addUserMessage(message) {

    const wrapper = document.createElement("div");

    wrapper.className = "message user";

    wrapper.innerHTML = `
        <div class="bubble">
            ${escapeHTML(message)}
        </div>
    `;

    chatArea.appendChild(wrapper);

    scrollToBottom();

}

/*-------------------------------------------------------
AI Message
-------------------------------------------------------*/

function addAIMessage(message) {

    const wrapper = document.createElement("div");

    wrapper.className = "message ai";

    wrapper.innerHTML = `
        <div class="bubble">
            ${escapeHTML(message)}
        </div>
    `;

    chatArea.appendChild(wrapper);

    scrollToBottom();

}

/*-------------------------------------------------------
Escape HTML
-------------------------------------------------------*/

function escapeHTML(text) {

    const div = document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}