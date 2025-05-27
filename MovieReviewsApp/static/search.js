async function handleSearch(event) {
    const text = event.target.value;
    const resultsContainer = document.getElementById('results');
    if (!text.trim()) {
        resultsContainer.innerHTML = '';
        return;
    }
    const response = await fetch(`/search?text=${encodeURIComponent(text)}`);
    const data = await response.json();

    if (data.length === 0) {
        resultsContainer.innerHTML = `<p>No results found.</p>`;
    } else {
        resultsContainer.innerHTML = '<ul>' +
            data.map(
                ([id, name, rating]) =>
                    `<li data-id="${id}">ID: ${id}, ${name}, Rating: ${rating}</li>`
            ).join('') +
            '</ul>';
    }
}
