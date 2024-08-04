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


$(document).ready(function() {
    $.getJSON('https://api.warframestat.us/pc/events', function(data) {
        let eventsHtml = '';
        data.forEach(event => {
            // Számítsuk ki a hátralévő időt
            const now = new Date();
            const expiry = new Date(event.expiry);
            const timeLeft = expiry - now;
            const daysLeft = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            const hoursLeft = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutesLeft = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            setInterval(() => updateTimer(" ", cycle-card), 1000);

            eventsHtml += `
                <div class="cycle-card">
                    <h2>${event.description}</h2>
                    <div class="cycle-info">
                        <p><span class="state">Status:</span> ${event.active ? 'Active' : 'Inactive'}</p>
                        <p><span class="time">Time left:</span> ${daysLeft}d ${hoursLeft}h ${minutesLeft}m</p>
                        <p><span class="state">Node:</span> ${event.node}</p>
                        <p><span class="state">Progress:</span> ${event.currentScore}/${event.maximumScore}</p>
                        ${event.rewards.length > 0 ? `
                            <p><span class="state">Rewards:</span></p>
                            <ul>
                                ${event.rewards.map(reward => `<li>${reward.asString}</li>`).join('')}
                            </ul>
                        ` : ''}
                        ${event.interimSteps.length > 0 ? `
                            <p><span class="state">Interim Steps:</span></p>
                            <ul>
                                ${event.interimSteps.map(step => `
                                    <li>Goal: ${step.goal} - Reward: ${step.reward.asString}</li>
                                `).join('')}
                            </ul>
                        ` : ''}
                    </div>
                </div>
            `;
        });
        $('#events-list').html(eventsHtml);
    });
});