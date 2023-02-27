import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';


let appDesc = {
    mounted() {
        this.retrieve();
    },
    data() {
        return {
            loadig: true,
            items: [],
        }
    },
    methods: {
        retrieve() {
            this.loading = true;
            let _this = this;

            let url = 'http://' + window.location.host + '/api/v1/nft/';

            axios.get(url)
                .then(function (response) {
                    _this.items = response.data;
                })
                .catch(function (response) {
                    console.log(response.data);
                })
                .finally(function () {
                    _this.loadig = false;
                });
        },
        getAverageRGB(imgEl) {

            var blockSize = 5, // only visit every 5 pixels
                defaultRGB = { r: 0, g: 0, b: 0 }, // for non-supporting envs
                canvas = document.createElement('canvas'),
                context = canvas.getContext && canvas.getContext('2d'),
                data, width, height,
                i = -4,
                length,
                rgb = { r: 0, g: 0, b: 0 },
                count = 0;

            if (!context) {
                return defaultRGB;
            }

            height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height;
            width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width;

            context.drawImage(imgEl, 0, 0);

            try {
                data = context.getImageData(0, 0, width, height);
            } catch (e) {
                /* security error, img on diff domain */
                return defaultRGB;
            }

            length = data.data.length;

            while ((i += blockSize * 4) < length) {
                ++count;
                rgb.r += data.data[i];
                rgb.g += data.data[i + 1];
                rgb.b += data.data[i + 2];
            }

            // ~~ used to floor values
            rgb.r = ~~(rgb.r / count);
            rgb.g = ~~(rgb.g / count);
            rgb.b = ~~(rgb.b / count);

            return rgb;

        },
        nft_ref(el) {
            const picture = el.getElementsByClassName('nft__picture')[0];
            let _el = el;
            let _getAverageRGB = this.getAverageRGB;
            picture.onload = function (event) {
                let c = _getAverageRGB(event.currentTarget);
                _el.style.background = `rgb(${c.r},${c.g},${c.b})`;
            }
        },
        click(event) {
            alert.show(alert.messageType.error,
                "You have no funds to buy nft's, please <a href=\"/profile/deposit\">deposit</a> or enter bonus code", 'NFT');
        },
        preview(img_url) {
            nftpreview.show(img_url);
        }
    }
};


document.app = createApp(appDesc).mount('#app_nft');


console.info(
    'nft.js loaded succesfully'
);

