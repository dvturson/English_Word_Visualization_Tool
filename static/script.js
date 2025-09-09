// References
const input = document.getElementById("input");
const list = document.getElementById("suggestions");
const imageContainer = document.getElementById("images");


// Getting the last word
function getLastWord(text) {
    const words = text.trim().split(/\s+/);
    return words[words.length - 1].toLowerCase();
}

// Find suggest
async function fetchSuggestions(prefix) {
    const res = await fetch(`/suggest?prefix=${encodeURIComponent(prefix)}`);
    return await res.json();
}

// Show suggest
function showSuggestions(words) {
    list.innerHTML = ""; // clear prev
    words.forEach(word => {
        const li = document.createElement("li");
        li.textContent = word;
        list.appendChild(li);
    });
}

// Fetch image
async function fetchImage(word) {
    try {
        const res = await fetch(`/fetch_image?word=${encodeURIComponent(word)}`);
        const data = await res.json();
        return data.img;
    } catch {
        return null;
    }
}

// When user type
input.addEventListener("input", async () => {
    const lastWord = getLastWord(input.value);
    if (!lastWord) {
        list.innerHTML = ""; // cleared
        imageContainer.innerHTML = "";
        return;
    }

    // Get / show suggestions
    const suggestions = await fetchSuggestions(lastWord);
    showSuggestions(suggestions);
});

// When space bar
input.addEventListener("keyup", async (event) => {
    if (event.key === 'Enter') {
        const full_text = input.value.trim();
        if (!full_text)
            return;

        const words = full_text.split(/\s+/);
        imageContainer.innerHTML = "";

        for (const word of words) {
            const imgSrc = await fetchImage(word);
            if (imgSrc) {
                const img = document.createElement("img");
                img.src = imgSrc;
                img.alt = word;
                imageContainer.appendChild(img);
            }
        }
    }
});