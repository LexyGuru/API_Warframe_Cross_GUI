console.log('Search script loaded');
let pyotherside;

function initWebChannel() {
    if (typeof QWebChannel === "undefined") {
        console.log("QWebChannel not available yet, retrying...");
        setTimeout(initWebChannel, 100);
        return;
    }
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.pyotherside = channel.objects.pyotherside;
        console.log("QWebChannel initialized");
        initSearch();
    });
}

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded");
    initWebChannel();
});

console.log('Search script loaded');

function initSearch() {
    console.log("Search initialization started");

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
        if (window.pyotherside && window.pyotherside.open_url) {
            window.pyotherside.open_url(url);
        } else {
            window.open(url, '_blank');
        }
    });

    console.log("Search initialization completed");
}


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
                                    ${item.wikiaThumbnail ? `<img src="${item.wikiaThumbnail}" alt="${item.name}" class="result-image">` : ''}
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

            // Itt adjuk hozzá az időzítést és a képellenőrzést
            setTimeout(function() {
                console.log("Delayed image loading check");
                checkImages();
            }, 1000);  // 1 másodperces késleltetés

        }).fail(function() {
            $("#results").html("<p>Error occurred while searching for items. Please try again later.</p>");
        });
    }).fail(function() {
        $("#results").html("<p>Error occurred while searching for drops. Please try again later.</p>");
    });
}

function checkImages() {
    $('.result-image').each(function() {
        if (!this.complete || this.naturalWidth === 0) {
            console.error("Image failed to load:", this.src);
            $(this).attr('src', 'path/to/placeholder-image.png');
        } else {
            console.log("Image loaded successfully:", this.src);
        }
    });
}

// Képbetöltés eseményfigyelők
$(document).on('load', '.result-image', function() {
    console.log('Image loaded event:', this.src);
}).on('error', '.result-image', function() {
    console.error('Image failed to load event:', this.src);
    $(this).attr('src', 'path/to/placeholder-image.png');
});