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
    });

    $(".p2p2_2buttons-right").on("click", function () {
        $(".p2p2_2buttons-left").removeClass("p2p2_2buttons-left--active");
        $(".p2p2_2buttons-right").addClass("p2p2_2buttons-right--active");
    });
}
left_right_toggler();
//

//p2p Select functionality
function setup_p2p_select(select_id) {
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
    });
}

setup_p2p_select("select_1");
setup_p2p_select("select_2");
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
        });
    };
}(jQuery));

$("#payment_methods").select();
//