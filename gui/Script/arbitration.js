$(document).ready(function() {
    function updateArbitrationTimer() {
        const now = new Date().getTime();
        const expiry = new Date($('#arbitration-timer').data('expiry')).getTime();
        const timeLeft = expiry - now;

        if (timeLeft > 0) {
            const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            $('#arbitration-timer').text(`Expires in: ${hours}h ${minutes}m ${seconds}s`);
        } else {
            $('#arbitration-timer').text("Expired");
        }
    }

    $.getJSON('https://api.warframestat.us/pc/arbitration', function(data) {
        let arbitrationHtml = `
            <div class="cycle-card">
                <h2>Arbitration Mission</h2>
                <div class="cycle-info">
                    <p><span class="state">Node:</span> ${data.node}</p>
                    <p><span class="state">Enemy:</span> ${data.enemy}</p>
                    <p><span class="state">Type:</span> ${data.type}</p>
                    <p><span class="time" id="arbitration-timer" data-expiry="${data.expiry}"></span></p>
                </div>
            </div>
        `;
        $('#arbitration-info').html(arbitrationHtml);
        updateArbitrationTimer();
        setInterval(updateArbitrationTimer, 1000);
    });
});