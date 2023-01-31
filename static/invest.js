import { createApp } from 'vue';

var activeSelect = null;

const print_error = console.error;
const log = console.log;

document.oneWeekApp = createApp({
    mounted: function () {
        this.btc = btc;
        this.ltc = ltc;
        this.eth = eth;
    },
    data() {
        return {
            loading: true,
            btc: 0,
            ltc: 0,
            eth: 0,
            coin: 'btc',
            stake: null,
            amount: 0.0.toFixed(4),
            amount_usd: 0.0.toFixed(2),
            profit: 0.0.toFixed(4),
            profit_usd: 0.0.toFixed(2),
        }
    },
    created: function () {
        this.update();
    },
    methods: {
        fillData: function (data) {
            this.stake = data;
            this.amount = this.stake.amount;
            this.profit = this.stake.amount * 0.091;
            this.coin = data.token_tag;
        },
        update: function () {
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/?search=OW`;
            fetch(url)
                .then((response) => response.json())
                .then((data) => {
                    if (data.length > 0) {
                        this.fillData(data[0]);
                    }
                })
                .catch((error) => {
                    print_error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        selectItemClick: function (coin_tag) {
            $("#select_0>.select__span").removeClass(this.coin);
            this.coin = coin_tag;
            $("#select_0>.select__span").addClass(this.coin);
            $("#select_0>.select__span").text(`${this.coin.toUpperCase()} - ${this[this.coin]}`);
            $("#stake_0").find(".stake__amount_crypto").text(this.coin.toUpperCase());
        },
        uiToggleSelect: function () {
            if (activeSelect) {
                $(activeSelect).removeClass("active");
                activeSelect = $("#select_0");
            }
            $("#select_0").toggleClass("active");
        },
        uiMaxButton: function () {
            $("#stake_0").find("input[type=number]").val(this[this.coin]);
        },
        uiStakeButton: function () {
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/`;
            let amount = parseFloat($('#stake_0').find('input[type=number]').val());
            fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    "stake_period": 'OW',
                    "token_tag": this.coin,
                    "amount": amount,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    this.fillData(data);
                })
                .catch((error) => {
                    print_error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        uiRestakeButton: function () {
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/${this.stake.id}/`;
            let amount = parseFloat($('#stake_0').find('input[type=number]').val()) + this.amount;
            fetch(url, {
                method: 'PATCH',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    "amount": amount,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    this.fillData(data);
                })
                .catch((error) => {
                    print_error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        uiUnstakeButton: function () {
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/${this.stake.id}/`;
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
                .then(() => {
                    this.coin = 'btc';
                    this.amount = 0.0;
                    this.profit = 0.0;
                    this.amount_usd = 0.0;
                    this.profit_usd = 0.0;
                    this.stake = null;
                })
                .catch((error) => {
                    print_error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
    },
}).mount('#stake_0');

setInterval(function () {
    //let price = parseFloat($("#price_BTC").val());
    fetch('http://' + window.location.host + '/profile/course')
        .then((response) => response.json())
        .then((data) => {
            let coin = document.oneWeekApp.coin;
            document.oneWeekApp.profit_usd = parseFloat(document.oneWeekApp.profit * data[coin]).toFixed(2);
            document.oneWeekApp.amount_usd = parseFloat(document.oneWeekApp.amount * data[coin]).toFixed(2);
        })
        .catch((e) => {
            print_error(e);
        });
}, 8000);