$(document).ready(function() {
    $.getJSON('https://api.warframestat.us/pc/events', function(data) {
        let eventsHtml = '';
        data.forEach(event => {
            eventsHtml += `
                <div class="cycle-card">
                    <h2>${event.description}</h2>
                    <div class="cycle-info">
                        <p><span class="state">Status:</span> ${event.active ? 'Active' : 'Inactive'}</p>
                        <p><span class="time">Time left:</span> ${event.eta}</p>
                    </div>
                </div>
            `;
        });
        $('#events-list').html(eventsHtml);
    });
});