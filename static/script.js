// $(".deposit__token").on("click", function () {
//     const qrcode = $(this).find("#qrcode").val();
//     const address = $(this).find("#address").val();
//     const icon = $(this).find(".deposit__token-icon").attr("src");
//     const name = $(this).find(".deposit__token-name").text().trim();
//     const tag = $(this).find("#tag").text().trim();
//     const amount = $(this).find("#amount").text().trim();

//     $("#crypto-icon").attr("src", icon);
//     $("#crypto-qr").attr("src", qrcode);
//     $("#crypto-name").text(`${tag} ${name}`);
//     $("#crypto-amount").text(amount);
//     $("#qr").text(address);

//     $(".deposit__token.active").toggleClass("active");
//     $(this).toggleClass("active");
// });

// elements = $.find(".deposit__token");

// if (elements.length > 0) {
//     $(elements[0]).trigger("click");
// }

$(".deposit__wallet-body-bottom-conainer-button").on("click", function () {
    const text = $("#qr").text();
    navigator.clipboard.writeText(text);
});

function switch_tab(tab_id, tabs_class_name) {
    $(`.${tabs_class_name}`).addClass("inactive");
    $(`#${tab_id}`).removeClass("inactive");
}

$(".deposit__token").on("click", function () {
    $(".deposit__token.active").toggleClass("active");
    $(this).toggleClass("active");
});

elements = $.find(".deposit__token");

if (elements.length > 0) {
    $(elements[0]).trigger("click");
}

//search functionality

$("#search").on("input", function () {
    const text = $(this).val();

    $(".wallet__tokens-item").each(function (index) {
        let query = text.toLowerCase();
        let source = $(this).find(".wallet_tokens-item-name").text().toLowerCase();
        let result1 = source.includes(query);
        source = $(this).find(".wallet__rokens-body-tag").text().toLowerCase();
        let result2 = source.includes(query);
        if (!result1 && !result2) {
            $(this).addClass("hidden");
        } else {
            $(this).removeClass("hidden");

        }
    });
});

//////////////////////

//Hide zero balances

$(".wallet__controls-checkbox").on("click", function () {
    if ($(this).is(":checked")) {
        $(".wallet__tokens-item").each(function (index) {
            let balance = $(this).find(".wallet__tokens-item-amount").text();
            balance = parseFloat(balance.replace(",", "."));
            if (balance <= 0.0) {
                $(this).addClass("hidden");
            } else {
                $(this).removeClass("hidden");

            }
        });
    } else {
        $(".wallet__tokens-item").removeClass("hidden");
    }
});

////////////////////////////