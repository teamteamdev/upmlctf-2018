$(document).ready(() => {
    const getCurrentLocation = () => {
        return window.location.pathname.split("/maze/")[1];
    };

    const getNextLocation = (current) => {
        const url = "../next";
        $.post(url, { id: current }, (data) => {
            $('a').attr("href", data);
        });
    };

    getNextLocation(getCurrentLocation());
});