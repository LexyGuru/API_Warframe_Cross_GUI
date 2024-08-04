function updateCycles() {
    function updateTimer(elementId, expiryTime) {
        const now = new Date().getTime();
        const timeLeft = expiryTime - now;

        if (timeLeft > 0) {
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            $(`#${elementId}`).text(`${hours}h ${minutes}m ${seconds}s`);
        } else {
            $(`#${elementId}`).text("Frissítés...");
            fetchCycleData();
        }
    }

    function fetchCycleData() {
        $.getJSON("https://api.warframestat.us/pc/cetusCycle", function(data) {
            $("#cetus-state").text(data.state);
            const cetusExpiry = new Date(data.expiry).getTime();
            setInterval(() => updateTimer("cetus-time", cetusExpiry), 1000);
        });

        $.getJSON("https://api.warframestat.us/pc/vallisCycle", function(data) {
            $("#vallis-state").text(data.state);
            const vallisExpiry = new Date(data.expiry).getTime();
            setInterval(() => updateTimer("vallis-time", vallisExpiry), 1000);
        });

        $.getJSON("https://api.warframestat.us/pc/cambionCycle", function(data) {
            $("#cambion-state").text(data.active);
            const cambionExpiry = new Date(data.expiry).getTime();
            setInterval(() => updateTimer("cambion-time", cambionExpiry), 1000);
        });
    }

    fetchCycleData();
}

$(document).ready(updateCycles);