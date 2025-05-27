document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('review');
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const movieId = form.movieId.value;
      const rating  = form.rating.value;
  
      await fetch('/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movieId, rating })
      });
  
      const res = await fetch(`/movie/${movieId}`);
      const updated = await res.json();
  
      const li = document.querySelector(`#results li[data-id="${movieId}"]`);
      if (li && updated) {
        li.textContent = `ID: ${updated[0]}, ${updated[1]}, Rating: ${updated[2]}`;
      }
  
      form.reset();
    });
  });
  