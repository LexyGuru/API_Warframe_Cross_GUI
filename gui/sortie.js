$(document).ready(function() {
    function updateSortieTimer() {
        const now = new Date().getTime();
        const expiry = new Date($('#sortie-timer').data('expiry')).getTime();
        const timeLeft = expiry - now;

        if (timeLeft > 0) {
            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            $('#sortie-timer').text(`Expires in: ${hours}h ${minutes}m ${seconds}s`);
        } else {
            $('#sortie-timer').text("Expired");
        }
    }

    function cleanNodeName(nodeName) {
        // Remove text in parentheses and trim
        return nodeName.replace(/\(.*?\)/g, '').trim();
    }

    $.getJSON('https://api.warframestat.us/pc/sortie?language=en', function(data) {
        let sortieHtml = `
            <div class="cycle-card">
                <h2>${data.boss}</h2>
                <div class="cycle-info">
                    <p><span class="state">Faction:</span> ${data.faction}</p>
                    <p><span class="time" id="sortie-timer" data-expiry="${data.expiry}"></span></p>
                </div>
            </div>
        `;
        data.variants.forEach((variant, index) => {
            sortieHtml += `
                <div class="cycle-card">
                    <h2>Mission ${index + 1}</h2>
                    <div class="cycle-info">
                        <p><span class="state">Type:</span> ${variant.missionType}</p>
                        <p><span class="state">Modifier:</span> ${variant.modifier}</p>
                        <p><span class="state">Node:</span> ${cleanNodeName(variant.node)}</p>
                    </div>
                </div>
            `;
        });
        $('#sortie-info').html(sortieHtml);
        updateSortieTimer();
        setInterval(updateSortieTimer, 1000);
    });
});