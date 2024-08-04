$(document).ready(function() {
    function updateEventTimes() {
        $('.time-left').each(function() {
            const expiry = new Date($(this).data('expiry'));
            const now = new Date();
            const timeLeft = expiry - now;

            if (timeLeft > 0) {
                const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

                $(this).text(`${days}d ${hours}h ${minutes}m ${seconds}s`);
            } else {
                $(this).text('Expired');
            }
        });
    }

    function loadEvents() {
        $.getJSON('https://api.warframestat.us/pc/events', function(data) {
            let eventsHtml = '';
            data.forEach(event => {
                eventsHtml += `
                    <div class="cycle-card">
                        <h2>${event.description}</h2>
                        <div class="cycle-info">
                            <p><span class="state">Status:</span> ${event.active ? 'Active' : 'Inactive'}</p>
                            <p><span class="state">Time left:</span> <span class="time-left" data-expiry="${event.expiry}"></span></p>
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
            updateEventTimes();
        });
    }

    loadEvents();
    setInterval(updateEventTimes, 1000);  // Frissítés másodpercenként
    setInterval(loadEvents, 60000);  // Teljes újratöltés percenként
});