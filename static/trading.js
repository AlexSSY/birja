const log = console.log;
const chart_DOM_element = $("#chart")[0];
const charts = LightweightCharts;

const chart_properties = {
    width: 0,
    height: 450,
    layout: {
        backgroundColor: '#001D1F',
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

const chart = charts.createChart(chart_DOM_element, chart_properties);
const canlde_series = chart.addCandlestickSeries();

//Get history data///////////////////////////////////
fetch("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000")
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
        canlde_series.setData(cdata);
    })
    .catch(err => log(err));
/////////////////////////////

//Stream data directly//////////

ws_binance_chart = new WebSocket('wss://stream.binance.com:9443/ws/' + 'btcusdt' + '@kline_1m');
ws_binance_chart.onopen = function () { }

last_price = 0.0

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

    if (last_price < json_result_data.close) {
        $(".trading__header-last-price-data-avg")
            .removeClass("trading__header-last-price-data-avg--red")
            .addClass("trading__header-last-price-data-avg--green");
    } else {
        $(".trading__header-last-price-data-avg")
            .removeClass("trading__header-last-price-data-avg--green")
            .addClass("trading__header-last-price-data-avg--red");
    }

    last_price = json_result_data.close;

    $(".trading__header-last-price-data-avg").text(last_price.toFixed(2).toString());
}

/////////////////////////////////

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

    fetch("https://api.binance.com/api/v1/depth?symbol=BTCUSDT&limit=20")
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
                red_tadle_td_list.get(2).innerText = d_asks_3.toString();

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
                green_tadle_td_list.get(2).innerText = d_bids_3.toString();
            }
        }).catch(error => {
            log(error);
        });

}

setInterval(ui_order_book_update, 1000);

////////////////////////////////