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

    // First, search for drops
    $.getJSON(`https://api.warframestat.us/drops/search/${searchTerm}`, function(dropData) {
        let resultsHtml = "";

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
                    if (item.damageTypes) {
                        statsHtml += '<div class="result-stats">Damage: ';
                        for (let [damageType, value] of Object.entries(item.damageTypes)) {
                            statsHtml += `${damageType}: ${value}, `;
                        }
                        statsHtml = statsHtml.slice(0, -2) + '</div>';
                    }
                    if (item.criticalChance) {
                        statsHtml += `<div class="result-stats">Critical Chance: ${item.criticalChance}</div>`;
                    }
                    if (item.criticalMultiplier) {
                        statsHtml += `<div class="result-stats">Critical Multiplier: ${item.criticalMultiplier}</div>`;
                    }
                    if (item.procChance) {
                        statsHtml += `<div class="result-stats">Status Chance: ${item.procChance}</div>`;
                    }
                    if (item.fireRate) {
                        statsHtml += `<div class="result-stats">Fire Rate: ${item.fireRate}</div>`;
                    }

                    let acquisitionHtml = '';
                    if (item.components) {
                        acquisitionHtml += '<div class="result-acquisition">Components:';
                        item.components.forEach(component => {
                            acquisitionHtml += `<div>${component.name}: ${component.drops ? component.drops.map(drop => drop.location).join(', ') : 'N/A'}</div>`;
                        });
                        acquisitionHtml += '</div>';
                    }

                    let imageHtml = '';
                    if (item.wikiaThumbnail) {
                        imageHtml = `<img src="${item.wikiaThumbnail}" alt="${item.name}" class="result-image">`;
                    }

                    let wikiHtml = '';
                    if (item.name) {
                        let wikiUrl = `https://warframe.fandom.com/wiki/${encodeURIComponent(item.name.replace(/ /g, '_'))}`;
                        wikiHtml = `<a href="${wikiUrl}" target="_blank" class="wiki-link">Wiki Page</a>`;
                    }

                    resultsHtml += `
                        <div class="result-card">
                            <div class="result-info">
                                <div class="result-title">${item.name}</div>
                                <div class="result-details">Type: ${item.type}</div>
                                ${item.description ? `<div class="result-details">Description: ${item.description}</div>` : ''}
                                ${statsHtml}
                                ${acquisitionHtml}
                            </div>
                            <div class="result-extra">
                                ${imageHtml}
                                ${wikiHtml}
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
        $("#results").html("<p>Error occurred while searching. Please try again later.</p>");
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