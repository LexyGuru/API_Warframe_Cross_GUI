function getRarity(chance) {
    if (chance < 5) return "Rare";
    if (chance < 15) return "Uncommon";
    return "Common";
}

function searchDrops() {
    console.log("Search function called");
    const searchTerm = $("#search-input").val();
    if (searchTerm.length < 3) {
        $("#results").html("<p>Please enter at least 3 characters to search.</p>");
        return;
    }

    $("#results").html("<p>Searching...</p>");

    let resultsHtml = "";

    // First, search for drops
    $.getJSON(`https://api.warframestat.us/drops/search/${searchTerm}`, function(dropData) {
        if (dropData.length > 0) {
            dropData.forEach(item => {
                let rarity = getRarity(item.chance);
                resultsHtml += `
                    <div class="result-card">
                        <div class="result-info">
                            <div class="result-title">${item.item}</div>
                            <div class="result-details">Location: ${item.place}</div>
                            <div class="result-details">Chance: ${item.chance}%</div>
                        </div>
                        <span class="rarity ${rarity.toLowerCase()}">${rarity}</span>
                    </div>
                `;
            });
        }

        // Then, search for items
        $.getJSON(`https://api.warframestat.us/items/search/${searchTerm}`, function(itemData) {
            if (itemData.length > 0) {
                itemData.forEach(item => {
                    let statsHtml = '';
                    let acquisitionHtml = '';

                    // Mod-specifikus információk
                    if (item.type && item.type.toLowerCase().includes('mod')) {
                        if (item.levelStats) {
                            statsHtml += '<div class="result-stats"><strong>Level Stats:</strong><table class="level-stats-table">';
                            item.levelStats.forEach((stat, index) => {
                                statsHtml += `<tr><td>Rank ${index}</td><td>${stat.stats.join(', ')}</td></tr>`;
                            });
                            statsHtml += '</table></div>';
                        }

                        if (item.polarity) {
                            statsHtml += `<div class="result-stats"><strong>Polarity:</strong> ${item.polarity}</div>`;
                        }

                        if (item.rarity) {
                            statsHtml += `<div class="result-stats"><strong>Rarity:</strong> ${item.rarity}</div>`;
                        }

                        if (item.fusionLimit) {
                            statsHtml += `<div class="result-stats"><strong>Max Rank:</strong> ${item.fusionLimit}</div>`;
                        }
                    }

                    // Megszerzési információk
                    if (item.drop) {
                        acquisitionHtml += '<div class="result-acquisition"><strong>Drops:</strong><ul>';
                        item.drop.forEach(drop => {
                            acquisitionHtml += `<li>${drop.location}: ${drop.chance}%</li>`;
                        });
                        acquisitionHtml += '</ul></div>';
                    }

                    let wikiUrl = item.wikiaUrl || `https://warframe.fandom.com/wiki/${encodeURIComponent(item.name.replace(/ /g, '_'))}`;

                    resultsHtml += `
                        <div class="result-card">
                            <div class="result-content">
                                <div class="result-info">
                                    <h2 class="result-title">${item.name}</h2>
                                    <div class="result-details">Type: ${item.type || 'N/A'}</div>
                                    ${item.description ? `<div class="result-description">${item.description}</div>` : ''}
                                    ${statsHtml}
                                    ${acquisitionHtml}
                                </div>
                                <div class="result-image-container">
                                    ${item.wikiaThumbnail ? `<img src="${item.wikiaThumbnail}" alt="${item.name}" class="result-image" onerror="this.onerror=null;this.src='placeholder.png';">` : ''}
                                    <a href="${wikiUrl}" target="_blank" class="wiki-link">Wiki Page</a>
                                </div>
                            </div>
                        </div>
                    `;
                });
            }

            if (resultsHtml === "") {
                resultsHtml = "<p>No results found for the search term.</p>";
            }

            $("#results").html(resultsHtml);
        }).fail(function() {
            $("#results").html("<p>Error occurred while searching for items. Please try again later.</p>");
        });
    }).fail(function() {
        $("#results").html("<p>Error occurred while searching for drops. Please try again later.</p>");
    });
}

$(document).ready(function() {
    console.log("Document ready");
    $("#search-button").on('click', function() {
        console.log("Search button clicked");
        searchDrops();
    });
    $("#search-input").on('keyup', function(e) {
        if (e.key === 'Enter') {
            console.log("Enter key pressed");
            searchDrops();
        }
    });

    $(document).on('click', '.wiki-link', function(e) {
        e.preventDefault();
        let url = $(this).attr('href');
        if (typeof window.pyotherside !== 'undefined' && window.pyotherside.open_url) {
            window.pyotherside.open_url(url);
        } else {
            window.open(url, '_blank');
        }
    });
});