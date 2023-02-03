import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

var activeSelect = null;

const print_error = console.error;
const log = console.log;

let appDesc = {
    mounted: function () {
        this.updateBalance();
        let _this = this;
        setInterval(() => {
            let price = parseFloat($(`#price_${_this.coin.toUpperCase()}`).val());
            _this.profit_usd = (_this.profit * price).toFixed(2);
            _this.amount_usd = (_this.amount * price).toFixed(2);
        }, 1000);
    },
    data() {
        return {
            selectNode: null,
            toggled: false,
            loading: true,
            coin: 'btc',
            stake: null,
            available: {
                btc: 0,
                ltc: 0,
                eth: 0,
            },
            current: 0,
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
            this.profit = this.stake.amount * this.percent;
            this.coin = data.token_tag;
        },
        updateBalance: function (callback=null) {
            this.loading = true
            let _this = this;
            axios.post('http://' + window.location.host + '/profile/getcoins', {
                coins: [
                    'btc', 'ltc', 'eth',
                ],
            }, {
                headers: {
                    'X-CSRFToken': csrftoken,
                }
            })
                .then((response) => {
                    _this.available.btc = response.data.BTC;
                    _this.available.ltc = response.data.LTC;
                    _this.available.eth = response.data.ETH;
                    if (callback)
                        callback();
                })
                .catch((error) => {
                    alert.show(alert.messageType.error, error, 'Stake');
                })
                .finally(() => {
                    _this.loading = false;
                });
        },
        update: function () {
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/?search=${this.prefix}`;
            axios.get(url)
                .then((response) => {
                    if (response.data.length > 0) {
                        this.fillData(response.data[0]);
                    }
                })
                .catch((error) => {
                    if (error.response.data.amount)
                        alert.show(alert.messageType.error, error.response.data.amount, 'Stake');
                    else
                        alert.show(alert.messageType.error, error, 'Stake');
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        selectItemClick: function (event) {
            let coinNode = $(event.target).find(".coin-tag");

            $(this.selectNode).find('.select__span').removeClass(this.coin);
            this.coin = coinNode.text().toLowerCase();
            $(this.selectNode).find('.select__span').addClass(this.coin);

            $(this.selectNode).find('.select__span')
                .text(`${this.coin.toUpperCase()} - ${this.available[this.coin]}`);
            $(this.selectNode).find(".stake__amount_crypto").text(this.coin.toUpperCase());

            this.toggled = false;
        },
        uiToggleSelect: function (event) {
            this.toggled = !this.toggled;
            if (this.toggled)
                this.updateBalance();
        },
        getSelectSpanClass: function () {
            return this.coin;
        },
        uiMaxButton: function () {
            let _this = this;
            this.updateBalance(() => {
                _this.current = this.available[_this.coin];
            });
        },
        uiStakeButton: function () {
            let _this = this;
            this.loading = true;
            let amount = this.current;
            if (amount <= 0.0) {
                alert.show(alert.messageType.error, 'Amount must be higher than zero', 'Stake');
                this.loading = false;
                return;
            }
            let url = `http://${window.location.host}/api/v1/stake/`;

            let data = {
                stake_period: this.prefix,
                token_tag: this.coin,
                amount: amount,
            };

            let headers = {
                'X-CSRFToken': csrftoken,
            };

            axios.post(url, data, {
                headers: headers,
            })
                .then(function (response) {
                    $(`#total_${_this.coin.toUpperCase()}`).val(_this[_this.coin] -= response.data.amount);
                    _this.fillData(response.data);
                    this.updateBalance();
                })
                .catch(function (error) {
                    if (error.response.data)
                        alert.show(alert.messageType.error, error.response.data.amount, 'Stake');
                    else
                        alert.show(alert.messageType.error, error, 'Stake');
                })
                .finally(function () {
                    _this.loading = false;
                });
        },
        uiRestakeButton: function () {
            let _this = this;
            this.loading = true;
            let amount = this.current;
            if (amount <= 0.0) {
                alert.show(alert.messageType.error, 'Amount must be higher than zero', 'Stake');
                this.loading = false;
                return;
            }
            amount = this.amount + this.current;;
            let url = `http://${window.location.host}/api/v1/stake/${this.stake.id}/`;

            let data = {
                amount: amount,
                token_tag: this.coin,
            };

            let headers = {
                'X-CSRFToken': csrftoken,
            }

            axios.patch(url, data, {
                headers: headers,
            })
                .then((response) => {
                    $(`#total_${_this.coin.toUpperCase()}`).val(_this[_this.coin] -= response.data.amount);
                    _this.fillData(response.data);
                    this.updateBalance();
                })
                .catch((error) => {
                    if (error.response.data)
                        alert.show(alert.messageType.error, error.response.data.amount, 'Stake');
                    else
                        alert.show(alert.messageType.error, error, 'Stake');
                })
                .finally(() => {
                    _this.loading = false;
                });
        },
        uiUnstakeButton: function () {
            let _this = this;
            this.loading = true;
            let url = `http://${window.location.host}/api/v1/stake/${this.stake.id}/`;

            let headers = {
                'X-CSRFToken': csrftoken,
            };

            axios.delete(url, {
                headers: headers,
            })
                .then(() => {
                    $(`#total_${_this.coin.toUpperCase()}`).val(_this[_this.coin] += _this.amount);
                    _this.coin = 'btc';
                    _this.amount = 0.0;
                    _this.profit = 0.0;
                    _this.amount_usd = 0.0;
                    _this.profit_usd = 0.0;
                    _this.stake = null;
                    this.updateBalance();
                })
                .catch((error) => {
                    if (error.response.data.amount)
                        alert.show(alert.messageType.error, error.response.data.amount, 'Stake');
                    else
                        alert.show(alert.messageType.error, error, 'Stake');
                })
                .finally(() => {
                    _this.loading = false;
                });
        },
    },
}

document.oneWeekApp = createApp({...appDesc}).mount('#stake_0');
document.twoWeekApp = createApp({ ...appDesc }).mount('#stake_1');
document.oneMounthApp = createApp({...appDesc}).mount('#stake_2');
document.twoMounthApp = createApp({...appDesc}).mount('#stake_3');

document.oneWeekApp.percent = 0.01;
document.oneWeekApp.prefix = 'OW';
document.twoWeekApp.percent = 0.025;
document.twoWeekApp.prefix = 'TW';
document.oneMounthApp.percent = 0.07;
document.oneMounthApp.prefix = 'OM';
document.twoMounthApp.percent = 0.16;
document.twoMounthApp.prefix = 'TM';