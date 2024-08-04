$(document).ready(function() {
    function updateBaroTimer() {
        const now = new Date().getTime();
        const arrival = new Date($('#baro-timer').data('arrival')).getTime();
        const departure = new Date($('#baro-timer').data('departure')).getTime();

        let timeLeft;
        let status;
        if (now < arrival) {
            timeLeft = arrival - now;
            status = "Arrives in";
        } else if (now < departure) {
            timeLeft = departure - now;
            status = "Leaves in";
        } else {
            $('#baro-timer').text("Baro Ki'Teer has left");
            return;
        }

        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        $('#baro-timer').text(`${status}: ${days}d ${hours}h ${minutes}m ${seconds}s`);
    }

    $.getJSON('https://api.warframestat.us/pc/voidTrader', function(data) {
        let baroHtml = `
            <div class="cycle-card">
                <h2>Baro Ki'Teer Status</h2>
                <div class="cycle-info">
                    <p><span class="state">Location:</span> ${data.location}</p>
                    <p><span class="state">Status:</span> ${data.active ? 'Present' : 'Absent'}</p>
                    <p><span class="time" id="baro-timer" data-arrival="${data.activation}" data-departure="${data.expiry}"></span></p>
                </div>
            </div>
        `;
        if (data.inventory && data.inventory.length > 0) {
            baroHtml += `
                <div class="cycle-card">
                    <h2>Inventory</h2>
                    <div class="cycle-info">
                        <ul>
                            ${data.inventory.map(item => `<li>${item.item} (${item.ducats} Ducats, ${item.credits} Credits)</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }
        $('#baro-info').html(baroHtml);
        updateBaroTimer();
        setInterval(updateBaroTimer, 1000);
    });
});