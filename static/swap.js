//swap Select functionality
function setup_swap_select(select_id) {
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
        select_tag.text($(this).text());
        select_btn.toggleClass("swap__select-btn--open");
        select_items.toggleClass("swap__select-items--open");
    });
}

setup_swap_select("select_1");
setup_swap_select("select_2");
//