$("#id_message").on("input", function () {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";

    if (this.scrollHeight >= 320) {
        this.style.height = "320px";
    }
});

//Update Messages

function print_send_msg(data) {
    $("#messages").append(
        `<div class="support__row">
                        <!-- Submitted -->
                        <div class="support__col-12">
                            <div class="support__submit support__submit--send">
                                <div class="support__message-info">
                                    <div class="support__message-profile">
                                        <div class="support__profile-photo-container">
                                            <img class="support__profile-photo" src="${get_user_photo_url()}">
                                        </div>
                                        <p class="support__message-name">You</p>
                                    </div>
                                    <p class="support__message-time">${data.time}</p>
                                </div>
                                <p class="support__message">${data.message}</p>
                            </div>
                        </div>
                    </div>`
    );
}

function print_recv_msg(data) {
    $("#messages").append(
        `<div class="support__row">
                        <!-- Submitted -->
                        <div class="support__col-12">
                            <div class="support__submit">
                                <div class="support__message-info">
                                    <div class="support__message-profile">
                                        <div class="support__profile-photo-container">
                                            <img class="support__profile-photo" src="${get_user_photo_url()}">
                                        </div>
                                        <p class="support__message-name">${get_user_email()}</p>
                                    </div>
                                    <p class="support__message-time">${data.time}</p>
                                </div>
                                <p class="support__message">${data.message}</p>
                            </div>
                        </div>
                    </div>`
    );
}

function update_messages() {

    fetch("/support/list/" + get_user_id())
        .then(data => data.json())
        .then(data => {

            var messages = data.messages;

            //clear
            $("#messages").empty();

            for (let i = 0; i < messages.length; i++) {
                var message = messages[i];

                if (message.type === "recv") {
                    print_recv_msg(message);
                } else if (message.type === "send") {
                    print_send_msg(message);
                }
            }

            $("#messages").animate({ scrollTop: $("#messages").get(0).scrollHeight }, "fast");

        })
        .catch(err => console.log(err));
}

update_messages();

setInterval(update_messages, 5000);

//