/*

=========================================================

SRG.ai

History Controller (Version 3)

Part 1

=========================================================

*/

const STORAGE_KEY = "srg_chat_history";

let newChatBtn;
let historyContainer;
let searchInput;

let chats = [];
let currentChat = null;

/*-------------------------------------------------------
Initialize
-------------------------------------------------------*/

export function initializeHistory() {

    newChatBtn = document.getElementById("newChatBtn");
    historyContainer = document.getElementById("chatHistory");
    searchInput = document.getElementById("searchChats");

    loadChats();

    if (chats.length === 0) {

    createNewChat();

} else {

    chats.sort((a, b) => {

        if (a.pinned === b.pinned) {

            return b.id - a.id;

        }

        return Number(b.pinned) - Number(a.pinned);

    });

    currentChat = chats[0];

}

    renderChats();

    if (newChatBtn) {

        newChatBtn.addEventListener("click", createNewChat);

    }

    if (searchInput) {

        searchInput.addEventListener("input", searchChats);

    }

    document.addEventListener("click", closeAllMenus);

}

/*-------------------------------------------------------
Create New Chat
-------------------------------------------------------*/

function createNewChat() {

    currentChat = {

        id: Date.now(),

        title: "New Chat",

        created: new Date().toLocaleString(),

        pinned: false,

        messages: []

    };

    chats.unshift(currentChat);

    saveChats();

    renderChats();

    clearChatWindow();

}

/*-------------------------------------------------------
Clear Chat Window
-------------------------------------------------------*/

function clearChatWindow() {

    const area = document.getElementById("chatArea");

    if (area) {

        area.innerHTML = "";

    }

    const welcome = document.getElementById("welcomeScreen");

    if (welcome) {

        welcome.style.display = "flex";

    }

}

/*-------------------------------------------------------
Load Chats
-------------------------------------------------------*/

function loadChats() {

    try {

        const data = localStorage.getItem(STORAGE_KEY);

        chats = data ? JSON.parse(data) : [];

        chats.forEach(chat => {

            if (chat.pinned === undefined) {

                chat.pinned = false;

            }

            if (!chat.messages) {

                chat.messages = [];

            }

        });

    }

    catch (err) {

        console.error(err);

        chats = [];

    }

}

/*-------------------------------------------------------
Save Chats
-------------------------------------------------------*/

function saveChats() {

    localStorage.setItem(

        STORAGE_KEY,

        JSON.stringify(chats)

    );

}

/*-------------------------------------------------------
Render Chats
-------------------------------------------------------*/

function renderChats(list = chats) {

    if (!historyContainer) return;

    historyContainer.innerHTML = "";

    list.sort((a, b) => {

        if (a.pinned === b.pinned) {

            return b.id - a.id;

        }

        return Number(b.pinned) - Number(a.pinned);

    });

    list.forEach(chat => {

        const item = document.createElement("div");

        item.className = "chat-item";

        if (currentChat && currentChat.id === chat.id) {

            item.classList.add("active");

        }

        item.innerHTML = `

<div class="chat-left">

<i class="fa-solid fa-message"></i>

<span class="chat-title">

${chat.pinned ? "📌 " : ""}${chat.title}

</span>

</div>

<div class="chat-right">

<button class="chat-menu-btn">

<i class="fa-solid fa-ellipsis"></i>

</button>

</div>

`;

        const menu = document.createElement("div");

        menu.className = "history-menu";

        menu.innerHTML = `

<button class="rename-chat">

✏ Rename

</button>

<button class="pin-chat">

${chat.pinned ? "📍 Unpin" : "📌 Pin"}

</button>

<button class="share-chat">

📤 Share

</button>

<button class="delete-chat">

🗑 Delete

</button>

`;

        item.appendChild(menu);

        menu.addEventListener("click", (e) => {

            e.stopPropagation();

        });


        const menuBtn = item.querySelector(".chat-menu-btn");

        menuBtn.addEventListener("click", (e) => {

            e.stopPropagation();

            closeAllMenus();

            menu.classList.toggle("show");

        });

        const renameBtn = menu.querySelector(".rename-chat");
        const pinBtn = menu.querySelector(".pin-chat");
        const shareBtn = menu.querySelector(".share-chat");
        const deleteBtn = menu.querySelector(".delete-chat");

        renameBtn.addEventListener("click", (e) => {

            e.stopPropagation();

            menu.classList.remove("show");

            renameChat(chat);

        });

        pinBtn.addEventListener("click", (e) => {

            e.stopPropagation();

            menu.classList.remove("show");

            chat.pinned = !chat.pinned;

chats.sort((a, b) => {

    if (a.pinned === b.pinned) {

        return b.id - a.id;

    }

    return Number(b.pinned) - Number(a.pinned);

});

saveChats();

renderChats();

        });

            shareBtn.addEventListener("click", (e) => {

    e.stopPropagation();

    menu.classList.remove("show");

    const text = chat.messages
        .map(msg => `${msg.role}: ${msg.content}`)
        .join("\n\n");

    navigator.clipboard.writeText(text)
        .then(() => {

            alert("Chat copied.");

        })
        .catch(err => {

            console.error(err);

            alert("Unable to copy chat.");

        });

});
        deleteBtn.addEventListener("click", (e) => {

            e.stopPropagation();

            menu.classList.remove("show");

            if (confirm("Delete this chat?")) {

                deleteChat(chat.id);

            }

        });

        item.addEventListener("click", () => {

            currentChat = chat;

            renderChats();

            loadChat(chat);

        });

        historyContainer.appendChild(item);

    });

}

/*-------------------------------------------------------
Close Menus
-------------------------------------------------------*/

function closeAllMenus() {

    document.querySelectorAll(".history-menu")

        .forEach(menu => {

            menu.classList.remove("show");

        });

}

/*-------------------------------------------------------
Load Chat
-------------------------------------------------------*/

function loadChat(chat) {

    const chatArea = document.getElementById("chatArea");
    const welcome = document.getElementById("welcomeScreen");

    if (!chatArea) return;

    chatArea.innerHTML = "";

    if (welcome) {

        welcome.style.display = "none";

    }

    chat.messages.forEach(msg => {

        const wrapper = document.createElement("div");

        wrapper.className =
            msg.role === "user"
                ? "message user"
                : "message ai";

        wrapper.innerHTML = `

<div class="bubble">

${escapeHTML(msg.content)}

</div>

`;

        chatArea.appendChild(wrapper);

    });

    chatArea.scrollTop = chatArea.scrollHeight;

}

/*-------------------------------------------------------
Search Chats
-------------------------------------------------------*/

function searchChats() {

    const query = searchInput.value
        .trim()
        .toLowerCase();

    if (query === "") {

        renderChats();

        return;

    }

    const filtered = chats.filter(chat => {

        if (chat.title.toLowerCase().includes(query)) {

            return true;

        }

        return chat.messages.some(msg =>
            (msg.content || "")
    .toLowerCase()
    .includes(query)
        );

    });

    renderChats(filtered);

}

/*-------------------------------------------------------
Add Message
-------------------------------------------------------*/

export function addMessage(role, content) {

    if (!currentChat) {

        createNewChat();

    }

    currentChat.messages.push({

        role,
        content,
        time: new Date().toLocaleTimeString()

    });

    if (

        currentChat.title === "New Chat" &&
        role === "user"

    ) {

        let title = content
    .replace(/\s+/g, " ")
    .trim();

if (title.length > 40) {

    title = title.slice(0, 40).trim() + "...";

}

        currentChat.title = title;

    }

    saveChats();

    renderChats();

}

/*-------------------------------------------------------
Current Chat
-------------------------------------------------------*/

export function getCurrentChat() {

    return currentChat;

}

/*-------------------------------------------------------
Rename Chat
-------------------------------------------------------*/

function renameChat(chat) {

    const title = prompt(

        "Rename Chat",

        chat.title

    );

    if (title === null) return;

    if (title.trim() === "") return;

    chat.title = title.trim();

    saveChats();

    renderChats();

}

/*-------------------------------------------------------
Delete Chat
-------------------------------------------------------*/

function deleteChat(id) {

    chats = chats.filter(chat => chat.id !== id);

    if (

        currentChat &&
        currentChat.id === id

    ) {

        if (chats.length > 0) {

            currentChat = chats[0];

            saveChats();

            renderChats();

            loadChat(currentChat);

            return;

        }

        else {

            currentChat = null;

createNewChat();

return;

        }

    }

    saveChats();

renderChats();

if (currentChat) {

    loadChat(currentChat);

} else {

    clearChatWindow();

}

}

/*-------------------------------------------------------
Delete Current Chat
-------------------------------------------------------*/

export function deleteCurrentChat() {

    if (!currentChat) return;

    deleteChat(currentChat.id);

}

/*-------------------------------------------------------
Clear History
-------------------------------------------------------*/

export function clearHistory() {

    chats = [];

    currentChat = null;

    localStorage.removeItem(STORAGE_KEY);

    createNewChat();

}

/*-------------------------------------------------------
Escape HTML
-------------------------------------------------------*/

function escapeHTML(text) {

    const div = document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}

export function getAllChats() {

    return chats;

}

export function exportCurrentChat() {

    return JSON.stringify(currentChat, null, 2);

}