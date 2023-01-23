const log = console.log;
const chart_DOM_element = $("#chart")[0];
const charts = LightweightCharts;


let chart_properties = {
    width: 0,
    height: 450,
    layout: {
        backgroundColor: 'rgba(22, 26, 30, 1)',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.2)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.2)',
        },
    },
    timeScale: {
        timeVisible: true,
        secondVisible: false,
    },
}

let chart = charts.createChart(chart_DOM_element, chart_properties);
let canlde_series = chart.addCandlestickSeries();

function changeTheme(theme) {
    if (theme === "light") {
        chart.applyOptions(
            {
                layout: {
                    backgroundColor: "#efefef",
                    textColor: "#000",
                }
            }
        );
    } else if (theme === "dark") {
        chart.applyOptions(
            {
                layout: {
                    backgroundColor: "#161a1e",
                    textColor: "#fff",
                }
            }
        );
    }
}

g_ThemeSwitchQueue.push(changeTheme);

var oldRect = null;

new ResizeObserver(entries => {
    if (entries.length === 0 || entries[0].target !== $(".orders").get(0)) { return; }
    const newRect = entries[0].contentRect;
    //if (oldRect && oldRect.width > newRect.width) {
    //    chart.applyOptions({ width: newRect.width });
    //}
    oldRect = newRect;
}).observe($(".orders").get(0));

function numberWithSpaces(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ", ");
    return parts.join(".");
}

last_price = 0.0;

function ui_update_close_price(close_price) {
    if (last_price < close_price) {
        $(".trading__header-last-price-data-avg")
            .removeClass("trading__header-last-price-data-avg--red")
            .addClass("trading__header-last-price-data-avg--green");

        $(".trading__currents-major-text")
            .removeClass("trading__currents-major-text--red")
            .addClass("trading__currents-major-text--green");
    } else {
        $(".trading__header-last-price-data-avg")
            .removeClass("trading__header-last-price-data-avg--green")
            .addClass("trading__header-last-price-data-avg--red");

        $(".trading__currents-major-text")
            .removeClass("trading__currents-major-text--green")
            .addClass("trading__currents-major-text--red");
    }

    last_price = close_price;

    $(".trading__header-last-price-data-avg").text(numberWithSpaces(last_price.toFixed(2)));
    $(".trading__currents-major-text").text(numberWithSpaces(last_price.toFixed(2)));
    $(document).prop('title', numberWithSpaces(last_price.toFixed(2)) + " | " + g_pair + " | Tera Trade");
}

//Get history data///////////////
function get_history_data() {
    fetch("https://api.binance.com/api/v3/klines?symbol=" + g_pair + "&interval=1m&limit=1000")
        .then(res => res.json())
        .then(data => {
            const cdata = data.map(d => {
                return {
                    time: d[0] / 1000,
                    open: parseFloat(d[1]),
                    high: parseFloat(d[2]),
                    low: parseFloat(d[3]),
                    close: parseFloat(d[4]),
                }
            });

            const last_candle = cdata[cdata.length - 1];
            ui_update_close_price(last_candle.close);
            canlde_series.setData(cdata);
        })
        .catch(err => log(err));
}
get_history_data();
//Stream data directly///////////

ws_binance_chart = new WebSocket('wss://stream.binance.com:9443/ws/' + g_pair.toLowerCase() + '@kline_1m');
ws_binance_chart.onopen = function () { }

ws_binance_chart.onmessage = function (onmessage) {
    const json_data = JSON.parse(onmessage.data);
    const json_data_pair = json_data.k;
    const json_result_data = {
        time: json_data_pair.t / 1000,
        open: parseFloat(json_data_pair.o),
        high: parseFloat(json_data_pair.h),
        low: parseFloat(json_data_pair.l),
        close: parseFloat(json_data_pair.c),
    }
    canlde_series.update(json_result_data);

    //update last price
    ui_update_close_price(json_result_data.close);
}

//Update order book///////////////

$("#red_orders").empty();
$("#green_orders").empty();

for (let i = 0; i < 20; i++) {
    const order_table_tr = $('<tr class="trading__table-tr"></tr>');

    $('<td class="trading__table-tr-bar trading__table-tr-bar--red" colspan="3"></td>')
        .appendTo(order_table_tr);

    $('<td class="trading__table-td trading__table-td--red"></td>')
        .text("18,551.27")
        .appendTo(order_table_tr);

    $('<td class="trading__table-td"></td>')
        .text("0.193162")
        .appendTo(order_table_tr);

    $('<td class="trading__table-td"></td>')
        .text("204,551.27")
        .appendTo(order_table_tr);

    $("#red_orders").append(order_table_tr);
}

for (let i = 0; i < 20; i++) {
    const order_table_tr = $('<tr class="trading__table-tr"></tr>');

    $('<td class="trading__table-tr-bar trading__table-tr-bar--green" colspan="3"></td>')
        .appendTo(order_table_tr);

    $('<td class="trading__table-td trading__table-td--green"></td>')
        .text("18,551.27")
        .appendTo(order_table_tr);

    $('<td class="trading__table-td"></td>')
        .text("0.193162")
        .appendTo(order_table_tr);

    $('<td class="trading__table-td"></td>')
        .text("204,551.27")
        .appendTo(order_table_tr);

    $("#green_orders").append(order_table_tr);
}

function ui_order_book_update() {

    fetch("https://api.binance.com/api/v1/depth?symbol=" + g_pair + "&limit=20")
        .then(res => {
            return res.json();
        })
        .then(data => {
            const red_table = document.getElementById("table_red");
            const green_table = document.getElementById("table_green");
            const red_table_tr_list = $(red_table).find(".trading__table-tr");
            const green_table_tr_list = $(green_table).find(".trading__table-tr");

            for (let i = 0; i < 20; i++) {
                //asks
                const asks = data.asks;
                const d_asks_0 = parseFloat(asks[i][0]);
                const d_asks_1 = parseFloat(asks[i][1]);
                const d_asks_3 = (d_asks_0 * d_asks_1).toFixed(2);

                const red_tadle_td_list = $(red_table_tr_list.get(i + 1))
                    .find(".trading__table-td");

                let red_bar_node = $(red_table_tr_list.get(i + 1))
                    .find(".trading__table-tr-bar");
                $(red_bar_node).css("width", Math.min(d_asks_1 * 100.0, 100.0).toString() + "%");
                $(red_bar_node).css("left", (100.0 - Math.min(d_asks_1 * 100.0, 100.0)).toString() + "%");

                red_tadle_td_list.get(0).innerText = d_asks_0.toString();
                red_tadle_td_list.get(1).innerText = d_asks_1.toString();
                red_tadle_td_list.get(2).innerText = numberWithSpaces(d_asks_3);

                //bids
                const bids = data.bids;
                const d_bids_0 = parseFloat(bids[i][0]);
                const d_bids_1 = parseFloat(bids[i][1]);
                const d_bids_3 = (d_bids_0 * d_bids_1).toFixed(2);

                const green_tadle_td_list = $(green_table_tr_list.get(i))
                    .find(".trading__table-td");

                let green_bar_node = $(green_table_tr_list.get(i))
                    .find(".trading__table-tr-bar");
                $(green_bar_node).css("width", Math.min(d_bids_1 * 100.0, 100.0).toString() + "%");
                $(green_bar_node).css("left", (100.0 - Math.min(d_bids_1 * 100.0, 100.0)).toString() + "%");

                green_tadle_td_list.get(0).innerText = d_bids_0.toString();
                green_tadle_td_list.get(1).innerText = d_bids_1.toString();
                green_tadle_td_list.get(2).innerText = numberWithSpaces(d_bids_3);
            }
        }).catch(error => {
            log(error);
        });

}

ui_order_book_update();
setInterval(ui_order_book_update, 1000);

//Update data for last 24 hours////

function ui_last24h_update() {

    fetch("https://api.binance.com/api/v1/ticker/24hr?symbol=" + g_pair)
        .then(res => res.json())
        .then(data => {
            // last 24 hours in percent price change
            const last24h_percent = parseFloat(data.priceChangePercent)
                .toFixed(2);
            let l24hp = last24h_percent.toString();

            if (last24h_percent < 0) {
                $(".trading__header-24h-change-percent")
                    .addClass("trading__header-24h-change-percent--red");
            } else {
                $(".trading__header-24h-change-percent")
                    .removeClass("trading__header-24h-change-percent--red");
                l24hp = "+" + l24hp;
            }

            $(".trading__header-24h-change-percent").text(l24hp + " %");

            // last 24 hours most hig price
            const last24h_high = parseFloat(data.highPrice)
                .toFixed(2);
            const l24hh = numberWithSpaces(last24h_high);

            $(".trading__header-24h-high-value").text(l24hh);

            // last 24 hours most low price
            const last24h_low = parseFloat(data.lowPrice)
                .toFixed(2);
            const l24hl = numberWithSpaces(last24h_low);

            $(".trading__header-24h-low-value").text(l24hl);

            // last 24 hours volume USDT
            const last24h_volume = (parseFloat(data.volume)
                * parseFloat(data.weightedAvgPrice))
                .toFixed(2);
            const l24hv = numberWithSpaces(last24h_volume) + " " + g_symbol_dest;

            const eq_usd = numberWithSpaces(parseFloat(data.weightedAvgPrice).toFixed(2));

            $(".trading__header-24h-volume-value").text(l24hv);
            $("#vol_crypto_0").text(
                numberWithSpaces(parseFloat(data.volume).toFixed(2).toString()) + " " + g_symbol_dest
            );
            $("#vol_crypto_1").text(l24hv);
            $("#top_eq").text("$" + eq_usd);
            $("#left_eq").text("$" + eq_usd);

        }).catch(error => {
            log(error);
        });

}

ui_last24h_update();
setInterval(ui_last24h_update, 1000);

//Update data for pairs

function ui_pairs_update() {
    const pair_node_list = $(".trading__pairs-tbody").find(".trading__pairs-tr");

    $(pair_node_list).each(function (index) {
        const pair_symbol = $(this).attr("data-symbol");
        const pairs_td_list = $(this).find("td");
        fetch("https://api.binance.com/api/v1/ticker/24hr?symbol=" + pair_symbol)
            .then(res => res.json())
            .then(data => {
                // last 24 hours in percent price change
                const last24h_percent = parseFloat(data.priceChangePercent)
                    .toFixed(2);
                let l24hp = last24h_percent.toString();

                if (last24h_percent < 0) {
                    $(pairs_td_list[2])
                        .addClass("trading__pairs-td--red")
                        .removeClass("trading__pairs-td--green");
                } else {
                    $(pairs_td_list[2])
                        .removeClass("trading__pairs-td--red")
                        .addClass("trading__pairs-td--green");
                    l24hp = "+" + l24hp;
                }

                $(pairs_td_list[2]).text(l24hp + " %");

                // last 24 hours price
                const last24h_high = parseFloat(data.lastPrice)
                    .toFixed(2);
                const l24hh = numberWithSpaces(last24h_high);

                $(pairs_td_list[1]).text(l24hh);
            }).catch(error => {
                log(error);
            })
    });
}

ui_pairs_update();
setInterval(ui_pairs_update, 5000);

//Pairs ui filtering

$("#pairs_search").on("input", function () {
    const text = $(this).val();

    $(".trading__pairs-tbody>.trading__pairs-tr").each(function (index) {
        let query = text.toLowerCase();
        let source = $(this).find(".trading__pairs-td").text().toLowerCase();
        if (!source.includes(query)) {
            $(this).addClass("trading__pairs-tr--hidden");
        } else {
            $(this).removeClass("trading__pairs-tr--hidden");

        }
    });
});

//tabs

$("#trading_tabs>.orders__tabs-buttons>.orders__tab-button").on("click", function () {
    var data_target = $(this).attr("data-target");

    //update active class for buttons
    $("#trading_tabs>.orders__tabs-buttons>.orders__tab-button").removeClass("orders__tab-button--active");
    $(this).addClass("orders__tab-button--active");

    //update active class for tabs
    $("#trading_tabs>.orders__tab").removeClass("orders__tab--active");
    $(`#${data_target}`).addClass("orders__tab--active");
});

$("#history_tabs>.orders__tabs-buttons>.orders__tab-button").on("click", function () {
    var data_target = $(this).attr("data-target");

    //update active class for buttons
    $("#history_tabs>.orders__tabs-buttons>.orders__tab-button").removeClass("orders__tab-button--active");
    $(this).addClass("orders__tab-button--active");

    //update active class for tabs
    $("#history_tabs>.orders__tab").removeClass("orders__tab--active");
    $(`#${data_target}`).addClass("orders__tab--active");
});

//Chat

updateChat = function () {
    fetch("/chat")
        .then(data => data.text())
        .then(data => {
            $(".trading__chat-body").html(data);
            $(".trading__chat-body").get(0).scrollTo(0, $(".trading__chat-body").get(0).scrollHeight);
        });
}

updateChat();

setInterval(updateChat, 15000);