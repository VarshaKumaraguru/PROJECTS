async function getRecommendations() {
    const text = document.getElementById('text').value;
    const language = document.getElementById('language').value;

    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language })
    });

    const data = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <h2>Emotion: ${data.emotion}</h2>
        <h3>Recommended Songs:</h3>
        ${data.songs.map(song => `<div class="song">${song.song} by ${song.artist} - <a href="${song.url}" target="_blank">Listen</a></div>`).join('')}
    `;
}

async function getRecommendations() {
    const text = document.getElementById('text').value;
    const language = document.getElementById('language').value;

    if (!text || !language) {
        alert('Please enter a sentence and select a language.');
        return;
    }

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, language }),
        });

        if (response.ok) {
            const result = await response.json();

            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <h3>Emotion Detected: ${result.emotion}</h3>
                <h4>Recommended Songs:</h4>
                <ul>
                    ${result.songs.map(song => `<li>${song}</li>`).join('')}
                </ul>
            `;
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        alert('An error occurred. Please try again.');
    }
}
