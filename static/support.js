$("#message").on("input", function () {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";

    if (this.scrollHeight >= 320) {
        this.style.height = "320px";
    }
});