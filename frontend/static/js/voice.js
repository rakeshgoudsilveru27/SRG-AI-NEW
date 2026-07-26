/*
=========================================================
SRG.ai
Voice Controller
=========================================================
*/

let voiceBtn;
let messageInput;

let recognition = null;
let isListening = false;

/*-------------------------------------------------------
Initialize
-------------------------------------------------------*/

export function initializeVoice() {

    voiceBtn = document.getElementById("voiceBtn");
    messageInput = document.getElementById("messageInput");

    if (!voiceBtn || !messageInput) return;

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        console.warn("Speech Recognition is not supported.");

        voiceBtn.disabled = true;

        voiceBtn.title = "Speech Recognition is not supported";

        return;

    }

    recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.interimResults = true;

    recognition.continuous = false;

    recognition.maxAlternatives = 1;

    recognition.onstart = handleStart;
    recognition.onend = handleEnd;
    recognition.onresult = handleResult;
    recognition.onerror = handleError;

    voiceBtn.addEventListener("click", toggleRecognition);

}

/*-------------------------------------------------------
Toggle Recognition
-------------------------------------------------------*/

function toggleRecognition() {

    if (!recognition) return;

    if (isListening) {

        stopListening();

    } else {

        startListening();

    }

}

/*-------------------------------------------------------
Start Listening
-------------------------------------------------------*/

export function startListening() {

    if (!recognition || isListening) return;

    try {

        recognition.start();

    }
    catch (error) {

        console.error(error);

    }

}

/*-------------------------------------------------------
Stop Listening
-------------------------------------------------------*/

export function stopListening() {

    if (!recognition || !isListening) return;

    recognition.stop();

}

/*-------------------------------------------------------
Recognition Started
-------------------------------------------------------*/

function handleStart() {

    isListening = true;

    voiceBtn.classList.add("recording");

    voiceBtn.setAttribute("aria-label", "Stop Voice Recording");

    console.log("🎤 Listening...");

}

/*-------------------------------------------------------
Recognition Stopped
-------------------------------------------------------*/

function handleEnd() {

    isListening = false;

    voiceBtn.classList.remove("recording");

    voiceBtn.setAttribute("aria-label", "Voice Input");

    console.log("🎤 Stopped");

}

/*-------------------------------------------------------
Speech Result
-------------------------------------------------------*/

function handleResult(event) {

    let transcript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {

        transcript += event.results[i][0].transcript;

    }

    transcript = transcript.trim();

    if (!transcript) return;

    if (messageInput.value.trim() === "") {

        messageInput.value = transcript;

    } else {

        messageInput.value += " " + transcript;

    }

    messageInput.dispatchEvent(new Event("input"));

    messageInput.focus();

}

/*-------------------------------------------------------
Recognition Error
-------------------------------------------------------*/

function handleError(event) {

    console.error("Speech Recognition:", event.error);

    isListening = false;

    if (voiceBtn) {

        voiceBtn.classList.remove("recording");

        voiceBtn.setAttribute("aria-label", "Voice Input");

    }

}

/*-------------------------------------------------------
Set Recognition Language
-------------------------------------------------------*/

export function setVoiceLanguage(language) {

    if (!recognition) return;

    recognition.lang = language;

}

/*-------------------------------------------------------
Listening Status
-------------------------------------------------------*/

export function isVoiceListening() {

    return isListening;

}