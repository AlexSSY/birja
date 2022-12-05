const log = console.log;
const chart_DOM_element = $("#chart")[0];
const charts = LightweightCharts;

const chart_properties = {
    width: 0,
    height: 400,
    layout: {
        backgroundColor: '#000000',
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
fetch("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1s&limit=1000")
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
ws_binance_chart = new WebSocket('wss://stream.binance.com:9443/ws/' + 'btcusdt' + '@kline_1s');
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
}
/////////////////////////////////