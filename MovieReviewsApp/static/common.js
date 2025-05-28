document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('common-actors')
    const resultsContainer = document.getElementById('common-actors-results')

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const movieId1 = form.movieId1.value;
        const movieId2 = form.movieId2.value;

        const response = await fetch(`/actors?movieId1=${movieId1}&movieId2=${movieId2}`);
        const data = await response.json();

        if (data.length == 0) {
            resultsContainer.innerHTML = `<p>No results found.</p>`;
        } else {
            resultsContainer.innerHTML = '<ul>' +
            data.map(
                ([id, name]) =>
                    `<li data-id="${id}">ID: ${id}, ${name}</li>`
            ).join('') +
            '</ul>';
        }
        form.reset();
    });
});