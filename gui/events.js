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