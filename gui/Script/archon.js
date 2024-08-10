$(document).ready(function() {
    function updateArchonTimer() {
        const now = new Date().getTime();
        const expiry = new Date($('#archon-timer').data('expiry')).getTime();
        const timeLeft = expiry - now;

        if (timeLeft > 0) {
            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            $('#archon-timer').text(`Expires in: ${hours}h ${minutes}m ${seconds}s`);
        } else {
            $('#archon-timer').text("Expired");
        }
    }

    function cleanNodeName(nodeName) {
        // Remove text in parentheses and trim
        return nodeName.replace(/\(.*?\)/g, '').trim();
    }

    $.getJSON('https://api.warframestat.us/pc/archonHunt?language=en', function(data) {
        let archonHtml = `
            <div class="cycle-card">
                <h2>${data.boss}</h2>
                <div class="cycle-info">
                    <p><span class="state">Faction:</span> ${data.faction}</p>
                    <p><span class="time" id="archon-timer" data-expiry="${data.expiry}"></span></p>
                </div>
            </div>
        `;
        data.missions.forEach((mission, index) => {
            archonHtml += `
                <div class="cycle-card">
                    <h2>Mission ${index + 1}</h2>
                    <div class="cycle-info">
                        <p><span class="state">Type:</span> ${mission.typeKey}</p>
                        <p><span class="state">Node:</span> ${cleanNodeName(mission.nodeKey)}</p>
                    </div>
                </div>
            `;
        });
        $('#archon-info').html(archonHtml);
        setInterval(updateArchonTimer, 1000);
    });
});