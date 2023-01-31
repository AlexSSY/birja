//swap Select functionality
function setup_swap_select(select_id, on_select_callback) {
    let select_node = $("#" + select_id);
    let select_btn = select_node.find(".swap__select-btn");
    let select_items = select_node.find(".swap__select-items");
    let select_item = select_node.find(".swap__select-item");
    let select_tag = select_node.find(".swap__select-btn");

    $(select_btn).on("click", function () {
        select_btn.toggleClass("swap__select-btn--open");
        select_items.toggleClass("swap__select-items--open");
    });

    $(select_item).on("click", function () {
        select_tag.text($(this).find(".swap__select-tag").text());
        select_btn.toggleClass("swap__select-btn--open");
        select_items.toggleClass("swap__select-items--open");

        if (on_select_callback) {
            on_select_callback($(this).find(".swap__select-tag").text());
        }
    });
}

var pairs = {}
pairs["BTC"] = ["USDT", "USDC", ];
pairs["LTC"] = ["BTC", "ETH", "USDT", "USDC", "BNB", ];
pairs["ETH"] = ["BTC", "USDT", "USDC", ];
pairs["TRX"] = ["BTC", "ETH", "USDT", "USDC", "BNB", "XRP", ];
pairs["USDC"] = ["USDT", "BNB", ];
pairs["BNB"] = ["BTC", "ETH", "USDT", "USDC", ];
pairs["BCH"] = ["BTC", "USDT", "USDC", "BNB", ];
pairs["DOGE"] = ["BTC", "USDT", "USDC", "BNB", ];
pairs["XMR"] = ["BTC", "ETH", "USDT", "BNB", ];
pairs["XLM"] = ["BTC", "ETH", "USDT", "USDC", "BNB", ];
pairs["XTZ"] = ["BTC", "ETH", "USDT", "BNB", ];
pairs["EOS"] = ["BTC", "ETH", "USDT", "USDC", "BNB", ];
pairs["SHIB"] = ["USDT", "DOGE", ];
pairs["LINK"] = ["BTC", "ETH", "USDT", "USDC", "BNB" ];
pairs["BTG"] = ["BTC", "ETH", "USDT", ];
pairs["ETC"] = ["BTC", "USDT", "USDC", "BNB", ];
pairs["XRP"] = ["BTC", "ETH", "USDT", "USDC", "BNB", ];


function filter_coins() {
    let symbol1 = $("#select_1").find(".swap__select-btn").text();

    $("#select_2").find(".swap__select-item").removeClass("swap__select-item--hidden");

    $("#select_2").find(".swap__select-item").each(function (index) {
        let tag = $(this).find(".swap__select-tag").text();
        if (!pairs[symbol1])
            return;
        if (!pairs[symbol1].includes(tag)) {
            $(this).addClass("swap__select-item--hidden");
        }
    });
}

var g_currentSwapPrice = 1.0;

function update_to_amount() {
    $("#select_2>.swap__input-container>input")
        .val(parseFloat($("#select_1>.swap__input-container>input").val()) * g_currentSwapPrice);
}

function update_from_amount() {
    $("#select_1>.swap__input-container>input")
        .val(parseFloat($("#select_2>.swap__input-container>input").val()) / g_currentSwapPrice);
}

function update_pair(data) {
    let symbol1 = $("#select_1").find(".swap__select-btn").text();
    let symbol2 = $("#select_2").find(".swap__select-btn").text();

    if (symbol1 == symbol2) {
        $(".swap__course").text(`1 ${symbol1} = 1 ${symbol2}`);
        return;
    }

    let pair = symbol1 + symbol2;

    fetch("https://www.binance.com/api/v3/ticker/price?symbol=" + pair)
        .then(data => data.json())
        .then(data => {
            $(".swap__course").text(`1 ${symbol1} ~ ${data.price} ${symbol2}`);
            g_currentSwapPrice = parseFloat(data.price);
            update_to_amount();
        })
        .catch(err => {

        });

    //update hidden inputs (from, to)
    $("#id_from_").val(symbol1);
    $("#id_to").val(symbol2);
}

function update_fullmoney(data) {
    fetch("/profile/balance")
        .then(res => res.json())
        .then(res => {
            let fullmoney = $(".swap__fullmoney");
            //find
            let amount = 0.0;
            for (let i = 0; i < res.balances.length; i++) {
                if (res.balances[i][0] == data) {
                    amount = parseFloat(res.balances[i][2]);
                }
            }
            fullmoney.text(`${amount} ${data}`);
        })
        .then(err => {

        });
}

setup_swap_select("select_1", (data) => {
    filter_coins();

    //set USDT coin for #select_2
    $("#select_2").find(".swap__select-btn").text("USDT");

    update_pair(data);
    update_fullmoney(data);
});

setup_swap_select("select_2", (data) => {
    update_pair(data);
});
//

$(".swap__fullmoney").on("click", function (e) {
    let value = $(this).text();
    value = value.split(" ")[0];
    value = parseFloat(value);
    $("#select_1").find("input[type=number]").val(value);
    $("#select_1>.swap__input-container>input").change();
    e.preventDefault();
})

$("#select_1>.swap__input-container>input").change(function () {
    update_to_amount();
});

$("#select_1>.swap__input-container>input").on("input", function () {
    update_to_amount();
});

$("#select_2>.swap__input-container>input").change(function () {
    update_from_amount();
});

$("#select_2>.swap__input-container>input").on("input", function () {
    update_from_amount();
});

function init() {
    update_pair();
    update_fullmoney($("#select_1").find(".swap__select-btn").text());
    filter_coins();
}

init();