function getRarity(chance) {
    if (chance < 5) return "Rare";
    if (chance < 15) return "Uncommon";
    return "Common";
}

function searchDrops() {
    const searchTerm = $("#search-input").val();
    if (searchTerm.length < 3) {
        $("#results").html("<p>Kérjük, adjon meg legalább 3 karaktert a kereséshez.</p>");
        return;
    }

    $.getJSON(`https://api.warframestat.us/drops/search/${searchTerm}`, function(data) {
        if (data.length === 0) {
            $("#results").html("<p>Nincs találat a keresett elemre.</p>");
        } else {
            let resultsHtml = "";
            data.forEach(item => {
                let rarity = getRarity(item.chance);
                resultsHtml += `
                    <div class="result-card">
                        <div class="result-info">
                            <div class="result-title">${item.item}</div>
                            <div class="result-location">Hely: ${item.place}</div>
                        </div>
                        <div class="result-chance">Esély: ${item.chance}%</div>
                        <span class="rarity ${rarity.toLowerCase()}">${rarity}</span>
                    </div>
                `;
            });
            $("#results").html(resultsHtml);
        }
    }).fail(function() {
        $("#results").html("<p>Hiba történt a keresés során. Kérjük, próbálja újra később.</p>");
    });
}

$(document).ready(function() {
    $("#search-input").on('keyup', function(e) {
        if (e.key === 'Enter') {
            searchDrops();
        }
    });
});