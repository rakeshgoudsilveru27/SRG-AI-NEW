/*
=========================================================
SRG.ai
Theme Controller
=========================================================
*/

let themeBtn;

const STORAGE_KEY = "srg_theme";

/*-------------------------------------------------------
Initialize Theme
-------------------------------------------------------*/

export function initializeTheme() {

    themeBtn = document.getElementById("themeBtn");

    loadTheme();

    if (themeBtn) {

        themeBtn.addEventListener("click", toggleTheme);

    }

}

/*-------------------------------------------------------
Toggle Theme
-------------------------------------------------------*/

function toggleTheme() {

    const body = document.body;

    const isDark = !body.classList.contains("dark");

    body.classList.toggle("dark", isDark);

    updateThemeIcon(isDark);

    localStorage.setItem(
        STORAGE_KEY,
        isDark ? "dark" : "light"
    );

}

/*-------------------------------------------------------
Load Saved Theme
-------------------------------------------------------*/

function loadTheme() {

    let savedTheme = null;

    try {

        savedTheme = localStorage.getItem(STORAGE_KEY);

    }
    catch (error) {

        console.warn("Unable to access localStorage.", error);

    }

    const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;

    const useDark = savedTheme
        ? savedTheme === "dark"
        : prefersDark;

    document.body.classList.toggle("dark", useDark);

    updateThemeIcon(useDark);

}

/*-------------------------------------------------------
Update Theme Icon
-------------------------------------------------------*/

function updateThemeIcon(isDark) {

    if (!themeBtn) return;

    const icon = themeBtn.querySelector("i");

    if (!icon) return;

    icon.className = isDark
        ? "fa-solid fa-sun"
        : "fa-solid fa-moon";

    themeBtn.setAttribute(
        "aria-label",
        isDark ? "Switch to Light Theme"
               : "Switch to Dark Theme"
    );

    themeBtn.title = isDark
        ? "Light Theme"
        : "Dark Theme";

}

/*-------------------------------------------------------
Get Current Theme
-------------------------------------------------------*/

export function getCurrentTheme() {

    return document.body.classList.contains("dark")
        ? "dark"
        : "light";

}

/*-------------------------------------------------------
Set Theme
-------------------------------------------------------*/

export function setTheme(theme) {

    if (theme !== "dark" && theme !== "light") return;

    const isDark = theme === "dark";

    document.body.classList.toggle("dark", isDark);

    updateThemeIcon(isDark);

    localStorage.setItem(STORAGE_KEY, theme);

}