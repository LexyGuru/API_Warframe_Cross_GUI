const API_URL = 'https://api.github.com/repos/LexyGuru/API_Warframe_Cross_GUI/commits';
const REPO_URL = 'https://github.com/LexyGuru/API_Warframe_Cross_GUI/commit/';

async function fetchCommits() {
    try {
        const response = await fetch(API_URL);
        const commits = await response.json();
        displayCommits(commits);
    } catch (error) {
        console.error('Hiba történt az adatok lekérése közben:', error);
        document.getElementById('commitTableBody').innerHTML = `
            <tr>
                <td colspan="4">Hiba történt az adatok lekérése közben: ${error.message}</td>
            </tr>
        `;
    }
}

function displayCommits(commits) {
    const tableBody = document.getElementById('commitTableBody');
    tableBody.innerHTML = '';

    commits.forEach(commit => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${commit.sha.substring(0, 7)}</td>
            <td>${commit.commit.message}</td>
            <td>${commit.commit.author.name}</td>
            <td>${new Date(commit.commit.author.date).toLocaleString('hu-HU')}</td>
        `;
        row.addEventListener('click', () => openCommitPage(commit.sha));
        tableBody.appendChild(row);
    });
}

function openCommitPage(sha) {
    const url = REPO_URL + sha;
    if (typeof window.pyotherside !== 'undefined' && window.pyotherside.open_url) {
        window.pyotherside.open_url(url);
    } else {
        console.error('pyotherside not available, falling back to window.open');
        window.open(url, '_blank');
    }
}

// Várjunk a pyotherside objektum inicializálására
function waitForPyotherside(callback) {
    if (typeof window.pyotherside !== 'undefined') {
        callback();
    } else {
        setTimeout(function() { waitForPyotherside(callback); }, 100);
    }
}

// Csak akkor indítsuk el a fetchCommits függvényt, ha a pyotherside objektum már elérhető
waitForPyotherside(fetchCommits);