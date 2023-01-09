function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

function loadTheme() {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-dark');
        $(".theme-switcher__button").removeClass("theme-switcher__button--moon").addClass("theme-switcher__button--sun");
    } else {
        setTheme('theme-light');
        $(".theme-switcher__button").removeClass("theme-switcher__button--sun").addClass("theme-switcher__button--moon");
    }
}

$(".theme-switcher__button").on("click", function () {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-light');
        $(this).removeClass("theme-switcher__button--sun").addClass("theme-switcher__button--moon");
    } else {
        setTheme('theme-dark');
        $(this).removeClass("theme-switcher__button--moon").addClass("theme-switcher__button--sun");
    }
})

 // Immediately invoked function to set the theme on initial load
loadTheme();