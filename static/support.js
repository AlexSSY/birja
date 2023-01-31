$(".support__textarea").on("input", function () {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";

    if (this.scrollHeight >= 320) {
        this.style.height = "320px";
    }
});

//Update Messages

function print_send_msg(data) {
    $(".support__middle").append(
        `<div class="support__row">
                            <!-- Submitted -->
                            <div class="support__col-6"></div>
                            <div class="support__col-6">
                                <div class="support__submit">
                                    <p class="support__message">${data.message}</p>
                                    <div class="support__message-info">
                                        <p class="support__message-time">${data.time}</p>
                                        <div class="support__message-profile">
                                            <p class="support__message-name">You</p>
                                            <div class="support__profile-photo-container">
                                                <img class="support__profile-photo" src="${get_user_photo_url()}">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`
    );
}

function print_recv_msg(data) {
    $(".support__middle").append(
        `<div class="support__row">
                            <!-- Received -->
                            <div class="support__col-6">
                                <div class="support__submit">
                                    <p class="support__message">${data.message}</p>
                                    <div class="support__message-info support__message-info--reverse">
                                        <p class="support__message-time">${data.time}</p>
                                        <div class="support__message-profile">
                                            <p class="support__message-name">Support worker</p>
                                            <div class="support__profile-photo-container">
                                                <img class="support__profile-photo"
                                                    src="${get_static_url('images/support.png')}">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="support__col-6"></div>
                        </div>`
    );
}

function get_and_display_messages() {
    fetch("/support/list")
        .then(data => data.json())
        .then(data => {

            var messages = data.messages;

            //clear
            $(".support__middle").empty();

            for (let i = 0; i < messages.length; i++) {
                var message = messages[i];

                if (message.type === "recv") {
                    print_recv_msg(message);
                } else if (message.type === "send") {
                    print_send_msg(message);
                }
            }

            $(".support__middle").animate({ scrollTop: $(".support__middle").get(0).scrollHeight }, "fast");

        })
        .catch(err => console.log(err));
}

get_and_display_messages();

setInterval(get_and_display_messages, 5000);

//