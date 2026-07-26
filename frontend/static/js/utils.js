/*
=========================================================
SRG.ai
Utility Functions
=========================================================
*/

/*-------------------------------------------------------
Generate Unique ID
-------------------------------------------------------*/
export function generateId() {

    return crypto.randomUUID();

}

/*-------------------------------------------------------
Current Timestamp
-------------------------------------------------------*/
export function getTimestamp() {

    return new Date().toLocaleString();

}

/*-------------------------------------------------------
Current Time
-------------------------------------------------------*/
export function getCurrentTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",
        minute: "2-digit"

    });

}

/*-------------------------------------------------------
Escape HTML
-------------------------------------------------------*/
export function escapeHTML(text) {

    const div = document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}

/*-------------------------------------------------------
Debounce
-------------------------------------------------------*/
export function debounce(callback, delay = 300) {

    let timer;

    return (...args) => {

        clearTimeout(timer);

        timer = setTimeout(() => {

            callback(...args);

        }, delay);

    };

}

/*-------------------------------------------------------
Throttle
-------------------------------------------------------*/
export function throttle(callback, limit = 250) {

    let waiting = false;

    return (...args) => {

        if (waiting) return;

        callback(...args);

        waiting = true;

        setTimeout(() => {

            waiting = false;

        }, limit);

    };

}

/*-------------------------------------------------------
Copy Text
-------------------------------------------------------*/
export async function copyText(text) {

    try {

        await navigator.clipboard.writeText(text);

        return true;

    }

    catch {

        return false;

    }

}

/*-------------------------------------------------------
Download JSON
-------------------------------------------------------*/
export function downloadJSON(filename, data) {

    const blob = new Blob(

        [JSON.stringify(data, null, 2)],

        {

            type: "application/json"

        }

    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = filename;

    a.click();

    URL.revokeObjectURL(url);

}

/*-------------------------------------------------------
Read File
-------------------------------------------------------*/
export function readFile(file) {

    return new Promise((resolve, reject) => {

        const reader = new FileReader();

        reader.onload = () => resolve(reader.result);

        reader.onerror = reject;

        reader.readAsDataURL(file);

    });

}

/*-------------------------------------------------------
Format File Size
-------------------------------------------------------*/
export function formatFileSize(bytes) {

    if (bytes < 1024)

        return bytes + " B";

    if (bytes < 1024 * 1024)

        return (bytes / 1024).toFixed(1) + " KB";

    return (bytes / 1024 / 1024).toFixed(2) + " MB";

}

/*-------------------------------------------------------
Sleep
-------------------------------------------------------*/
export function sleep(ms) {

    return new Promise(resolve =>

        setTimeout(resolve, ms)

    );

}

/*-------------------------------------------------------
Random Number
-------------------------------------------------------*/
export function random(min, max) {

    return Math.floor(

        Math.random() * (max - min + 1)

    ) + min;

}

/*-------------------------------------------------------
Is Image
-------------------------------------------------------*/
export function isImage(file) {

    return file.type.startsWith("image/");

}

/*-------------------------------------------------------
Is Empty
-------------------------------------------------------*/
export function isEmpty(value) {

    return value === null ||

           value === undefined ||

           value === "";

}