$(document).ready(function() {
    function updateNightwaveTimers() {
        $('.nightwave-timer').each(function() {
            const now = new Date().getTime();
            const expiry = new Date($(this).data('expiry')).getTime();
            const timeLeft = expiry - now;

            if (timeLeft > 0) {
                const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

                $(this).text(`Expires in: ${days}d ${hours}h ${minutes}m ${seconds}s`);
            } else {
                $(this).text("Expired");
            }
        });
    }

    $.getJSON('https://api.warframestat.us/pc/nightwave', function(data) {
        let nightwaveHtml = '';
        data.activeChallenges.forEach(challenge => {
            nightwaveHtml += `
                <div class="cycle-card">
                    <h2>${challenge.title}</h2>
                    <div class="cycle-info">
                        <p>${challenge.desc}</p>
                        <p><span class="state">Reputation:</span> ${challenge.reputation}</p>
                        <p><span class="time nightwave-timer" data-expiry="${challenge.expiry}"></span></p>
                    </div>
                </div>
            `;
        });
        $('#nightwave-challenges').html(nightwaveHtml);
        updateNightwaveTimers();
        setInterval(updateNightwaveTimers, 1000);
    });
});