$(document).ready(function() {
    function updateFissureTimers() {
        $('.fissure-timer').each(function() {
            const now = new Date().getTime();
            const expiry = new Date($(this).data('expiry')).getTime();
            const timeLeft = expiry - now;

            if (timeLeft > 0) {
                const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

                $(this).text(`Expires in: ${hours}h ${minutes}m ${seconds}s`);
            } else {
                $(this).text("Expired");
            }
        });
    }

    $.getJSON('https://api.warframestat.us/pc/fissures', function(data) {
        let fissuresHtml = '';
        data.forEach(fissure => {
            fissuresHtml += `
                <div class="cycle-card">
                    <h2>${fissure.tier} ${fissure.missionType}</h2>
                    <div class="cycle-info">
                        <p><span class="state">Node:</span> ${fissure.node}</p>
                        <p><span class="time fissure-timer" data-expiry="${fissure.expiry}"></span></p>
                    </div>
                </div>
            `;
        });
        $('#fissures-list').html(fissuresHtml);
        updateFissureTimers();
        setInterval(updateFissureTimers, 1000);
    });
});