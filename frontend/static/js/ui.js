/*
=========================================================
SRG.ai
UI Controller
=========================================================
*/

let sidebar;
let sidebarOverlay;
let menuBtn;

let loadingScreen;

let messageInput;

let welcomeScreen;

let typingIndicator;

let chatArea;

/*-------------------------------------------------------
Initialize UI
-------------------------------------------------------*/

export function initializeUI() {

    sidebar = document.querySelector(".sidebar");
    sidebarOverlay = document.getElementById("sidebarOverlay");
    menuBtn = document.getElementById("menuBtn");

    loadingScreen = document.getElementById("loadingScreen");

    messageInput = document.getElementById("messageInput");

    welcomeScreen = document.getElementById("welcomeScreen");

    typingIndicator = document.getElementById("typing");

    chatArea = document.getElementById("chatArea");

    initializeLoading();

    initializeSidebar();

    initializeTextarea();

}

/*-------------------------------------------------------
Loading Screen
-------------------------------------------------------*/

function initializeLoading() {

    window.addEventListener("load", () => {

        if (!loadingScreen) return;

        setTimeout(() => {

            loadingScreen.style.opacity = "0";

            setTimeout(() => {

                loadingScreen.style.display = "none";

            }, 300);

        }, 500);

    });

}

/*-------------------------------------------------------
Sidebar
-------------------------------------------------------*/

function initializeSidebar() {

    if (!menuBtn || !sidebar || !sidebarOverlay) return;

    menuBtn.addEventListener("click", () => {

        sidebar.classList.toggle("active");

        sidebarOverlay.classList.toggle("active");

    });

    sidebarOverlay.addEventListener("click", () => {

        sidebar.classList.remove("active");

        sidebarOverlay.classList.remove("active");

    });

}

/*-------------------------------------------------------
Textarea Auto Resize
-------------------------------------------------------*/

function initializeTextarea() {

    if (!messageInput) return;

    messageInput.addEventListener("input", () => {

        messageInput.style.height = "auto";

        messageInput.style.height =
            messageInput.scrollHeight + "px";

    });

}

/*-------------------------------------------------------
Welcome Screen
-------------------------------------------------------*/

export function showWelcome() {

    if (!welcomeScreen) return;

    welcomeScreen.style.display = "flex";

}

export function hideWelcome() {

    if (!welcomeScreen) return;

    welcomeScreen.style.display = "none";

}

/*-------------------------------------------------------
Typing Indicator
-------------------------------------------------------*/

export function showTyping() {

    if (!typingIndicator) return;

    typingIndicator.style.display = "flex";

    scrollToBottom();

}

export function hideTyping() {

    if (!typingIndicator) return;

    typingIndicator.style.display = "none";

}

/*-------------------------------------------------------
Scroll Chat
-------------------------------------------------------*/

export function scrollToBottom() {

    if (!chatArea) return;

    requestAnimationFrame(() => {

        chatArea.scrollTo({

            top: chatArea.scrollHeight,

            behavior: "smooth"

        });

    });

}

/*-------------------------------------------------------
Sidebar Controls
-------------------------------------------------------*/

export function openSidebar() {

    if (!sidebar || !sidebarOverlay) return;

    sidebar.classList.add("active");

    sidebarOverlay.classList.add("active");

}

export function closeSidebar() {

    if (!sidebar || !sidebarOverlay) return;

    sidebar.classList.remove("active");

    sidebarOverlay.classList.remove("active");

}

export function toggleSidebar() {

    if (!sidebar || !sidebarOverlay) return;

    sidebar.classList.toggle("active");

    sidebarOverlay.classList.toggle("active");

}

/*-------------------------------------------------------
Toast
-------------------------------------------------------*/

export function showToast(message) {

    let toast = document.getElementById("toast");

    if (!toast) {

        toast = document.createElement("div");

        toast.id = "toast";

        toast.className = "toast";

        document.body.appendChild(toast);

    }

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(toast.timer);

    toast.timer = setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}