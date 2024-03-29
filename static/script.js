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

//Buttons

$(".deposit__token").on("click", function () {
    $(".deposit__token.active").toggleClass("active");
    $(this).toggleClass("active");
    $(".deposit__tokens").removeClass("deposit__tokens--show");
});

$(".tabs__buttons_button").on("click", function () {
    $(".tabs__buttons_button.selected").toggleClass("selected");
    $(this).toggleClass("selected");
});

$(".deposit__wallet-button-show").on("click", function () {
    $(".deposit__tokens").toggleClass("deposit__tokens--show");
});

/////////////////

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

//Profile expand

$("#profile_link").on("click", function (event) {
    $(".header__profile-expanded").toggleClass("hidden");
    event.preventDefault();
});

/////////////////////////

$("select").niceSelect();

// $(".select").on("click", function () {
//     $(this).toggleClass("active");
// });

function select(stake_id, select_item, class_name) {
    const stake_element = $("#" + stake_id);
    const select_element = $(stake_element).find(".select");

    $(stake_element)
        .find(".stake__amount_crypto")
        .text(class_name.toUpperCase());

    $(select_element)
        .find(".select__span")
        .text($(select_item).text());

    $(select_element)
        .find(".select__span")
        .removeClass()
        .addClass("select__span")
        .addClass(class_name);
}


// MAX Button on invest
$(".stake__amount_button").on("click", function () {
    let parent = $(this).parent();
    let coin_tag = $(parent).find(".stake__amount_crypto").text();
    if (coin_tag == "BTC") {
        $(parent).find("input").val(btc);
    } else if (coin_tag == "LTC") {
        $(parent).find("input").val(ltc);
    } else {
        $(parent).find("input").val(eth);
    }
});

//Balance/////////////////////////

function update_balance() {
    if (!isAuthenticated)
        return;
        
    fetch("/profile/balance")
        .then(res => res.json())
        .then(data => {
            total_balance = parseFloat(data.total_balance).toFixed(2);
            $("#wallet_top").text(`${total_balance} USD`);
            $("#wallet_middle").text(`${total_balance} USD`);
            $("#wallet_page").text(`${total_balance} USD`);

            //Equivalents
            for (let i = 0; i < data.balances.length; i++) {
                course = parseFloat(data.balances[i][1]);
                amount = parseFloat(data.balances[i][2]);
                result = (course * amount).toFixed(2);
                $(`#eq_${data.balances[i][0]}`).text(`${result}`);
                $(`#amount_${data.balances[i][0]}`).text(`${amount.toFixed(8)}`);
                $(`#price_${data.balances[i][0]}`).val(course);
                $(`#total_${data.balances[i][0]}`).val(amount);
            }
        })
        .catch(error => {

        });
}
update_balance();

setInterval(update_balance, 5000);
//////////////////////////////////

//Tablet buttons

$(".wallet__menu-tablet").on("click", function () {
    $(".wallet__menu").toggleClass("wallet__menu--open");
});

/////////////////////////////////

//alert

$(".alert__close").on("click", function () {
    $(".alert-bg").addClass("alert-bg--hidden");
    $(".alert").addClass("alert--hidden");
});

$(".alert__button").on("click", function () {
    $(".alert-bg").addClass("alert-bg--hidden");
    $(".alert").addClass("alert--hidden");
});

function showAlert(message) {
    $(".alert-bg").removeClass("alert-bg--hidden");
    $(".alert").removeClass("alert--hidden");
    $(".alert__text").text(message);
}

////////////////////////////////

//header menu
$(".header__nav-tablet").on("click", function () {
    // $(".header__nav>ul").toggleClass("header__nav--show");
    $(".header__profile-expanded").toggleClass("hidden");
});
/////////////