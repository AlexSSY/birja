function switch_setup(checkbox_id) {
    let checkbox_node = $(`#${checkbox_id}`);
    $(checkbox_node).css("display", "none");
    let parent_node = $(checkbox_node).parent();
    let switch_node = $('<div class="switch"></div>');
    let switch_circle_node = $('<div class="switch__circle"></div>');
    switch_node.append(switch_circle_node);
    $(parent_node).append(switch_node);

    $(switch_node).on("click", function () {
        $(switch_node).toggleClass("switch--checked", 1000);
        $(switch_circle_node).toggleClass("switch__circle--checked", 1000);
        $(checkbox_node).attr("checked", !$(checkbox_node).attr("checked"));
    })
}

switch_setup("verified");
switch_setup("active");


//Left-Right toggler
function left_right_toggler() {
    $(".p2p2_2buttons-left").on("click", function () {
        $(".p2p2_2buttons-left").addClass("p2p2_2buttons-left--active");
        $(".p2p2_2buttons-right").removeClass("p2p2_2buttons-right--active");
        p2p_state.trade_type = 'BUY';
        document.p2pApp.update(1);
    });

    $(".p2p2_2buttons-right").on("click", function () {
        $(".p2p2_2buttons-left").removeClass("p2p2_2buttons-left--active");
        $(".p2p2_2buttons-right").addClass("p2p2_2buttons-right--active");
        p2p_state.trade_type = 'SELL';
        document.p2pApp.update(1);
    });
}
left_right_toggler();
//

//p2p Select functionality
function setup_p2p_select(select_id, callback = null) {
    let select_node = $("#" + select_id);
    let select_btn = select_node.find(".p2p__select-btn");
    let select_items = select_node.find(".p2p__select-items");
    let select_item = select_node.find(".p2p__select-item");
    let select_tag = select_node.find(".p2p__select-btn");

    $(select_btn).on("click", function () {
        select_btn.toggleClass("p2p__select-btn--open");
        select_items.toggleClass("p2p__select-items--open");
    });

    $(select_item).on("click", function () {
        select_tag.text($(this).find(".p2p__select-item-tag").text());
        select_btn.toggleClass("p2p__select-btn--open");
        select_items.toggleClass("p2p__select-items--open");
        if (callback)
            callback(select_tag.text());
    });
}

setup_p2p_select("select_1", (text) => {
    p2p_state.token = text;
    document.p2pApp.update(1);
});
setup_p2p_select("select_2", (text) => {
    p2p_state.fiat = text;
    document.p2pApp.update(1);
});
//

//my select
(function ($) {
    $.fn.select = function (options) {
        var settings = $.extend({
            name: "My Select",
        }, options);

        let arrow = this.find(".p2p__select-arrow");
        let items = this.find(".p2p__select-items");
        let item = this.find(".p2p__select-item");
        let text = this.find(".p2p__select-text");

        this.on("click", function () {
            arrow.toggleClass("p2p__select-arrow--open");
            items.toggleClass("p2p__select-items--open");
        });

        item.on("click", function () {
            text.text($(this).text());
            document.p2pApp.update(document.p2pApp.page);
        });
    };
}(jQuery));

$("#payment_methods").select();
//

$(".p2p__more").on("click", function () {
    showAlert("you must deposit over 1 000 USD");
});


//Binance P2P
function get_p2p_binance(page_size = 10) {

    let url = window.location.origin + '/profile/p2p/10';

    fetch(url, {
        method: 'GET',
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.log(error);
        });
}

import { createApp } from 'vue';

// Vue.filter('toCurrency', function (value) {
//     if (typeof value !== "number") {
//         return value;
//     }
//     var formatter = new Intl.NumberFormat('en-US', {
//         style: 'currency',
//         currency: 'USD'
//     });
//     return formatter.format(value);
// });

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

document.p2pApp = createApp({
    mounted: function () {
        this.initialized = true;
    },
    data() {
        return {
            initialized: false,
            p2ps: null,
            page: 1,
            maxPages: 0,
            loading: false,
            trade_type: 'SELL',
        }
    },
    created() {
        this.perPage = 10;
        this.page = 1;
        this.update(1);
    },
    methods: {
        update(newPage) {
            this.loading = true;
            let url = `${window.location.origin}/profile/p2p/${this.perPage}/${newPage}/${p2p_state.get_part_url()}`;
            fetch(url, {
                method: 'GET',
            })
                .then((response) => response.json())
                .then((data) => {
                    var result = data.data;

                    this.maxPages = Math.round(data.total / this.perPage);

                    for (let i = 0; i < result.length; i++) {
                        result[i].first_letter = result[i].advertiser.nickName[0];
                        result[i].adv.dynamicMaxSingleTransAmount =
                            numberWithCommas(result[i].adv.dynamicMaxSingleTransAmount);
                    }
                    this.page = newPage;
                    this.trade_type = p2p_state.trade_type;
                    this.p2ps = result;
                })
                .catch((error) => {
                    console.log(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        toPage(pageNum, event = null) {
            this.update(pageNum);

            if (event)
                event.preventDefault();
        },
    },
}).mount('#app');
//