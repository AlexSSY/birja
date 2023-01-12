function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

function loadTheme() {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-dark');
        $(".theme-switcher__button").removeClass("theme-switcher__button--moon").addClass("theme-switcher__button--sun");
        for (let i = 0; i < g_ThemeSwitchQueue.length; i++) {
            g_ThemeSwitchQueue[i]("dark");
        }
    } else {
        setTheme('theme-light');
        $(".theme-switcher__button").removeClass("theme-switcher__button--sun").addClass("theme-switcher__button--moon");
        for (let i = 0; i < g_ThemeSwitchQueue.length; i++) {
            g_ThemeSwitchQueue[i]("light");
        }
    }
}

$(".theme-switcher__button").on("click", function () {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-light');
        $(this).removeClass("theme-switcher__button--sun").addClass("theme-switcher__button--moon");
        for (let i = 0; i < g_ThemeSwitchQueue.length; i++) {
            g_ThemeSwitchQueue[i]("light");
        }
    } else {
        setTheme('theme-dark');
        $(this).removeClass("theme-switcher__button--moon").addClass("theme-switcher__button--sun");
        for (let i = 0; i < g_ThemeSwitchQueue.length; i++) {
            g_ThemeSwitchQueue[i]("dark");
        }
    }
})

 // Immediately invoked function to set the theme on initial load
loadTheme();