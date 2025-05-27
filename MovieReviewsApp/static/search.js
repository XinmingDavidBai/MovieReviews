async function handleSearch(event) {
    // gets the user input text
    const text = event.target.value;

    // prepares the container for the id specified in index.html
    const resultsContainer = document.getElementById('results');

    // if the text is empty it sets the html content for the container to be nothing and returns
    if (!text.trim()) {
        resultsContainer.innerHTML = '';
        return;
    }
    // makes a GET request to the 'search' route in flask. We wait until we get a response
    const response = await fetch(`/search?text=${text}`);

    // gets the json data and produces a javascript object
    const data = await response.json();
    
    // if we the data is empty we didn't get a match.
    if (data.length === 0) {
        resultsContainer.innerHTML = `<p>No results found.</p>`;
    } else {
        // we map over the data and produce a list. we join it as one big html string.
        resultsContainer.innerHTML = '<ul>' +
            data.map(([id, name, rating]) => `<li>ID: ${id}, ${name}, Rating: ${rating}</li>`).join('') +
            '</ul>';
    }
}
