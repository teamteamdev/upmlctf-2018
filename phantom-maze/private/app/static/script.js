addEventListener('DOMContentLoaded', () => {
    const getCurrentLocation = () => {
        return window.location.pathname.split("/maze/")[1];
    };

    const getNextLocation = (current) => {
        let data = new FormData();
        data.append('id', getCurrentLocation());
        const pars = { method: 'POST', body: data };
        fetch('/next', pars).then((r) => {
            return r.text();
        }).then((r) => {
            document.getElementsByTagName('a')[0].href = r;
        })
    };

    getNextLocation(getCurrentLocation());
});
