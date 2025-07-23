// References
const input = document.getElementById("input");
const list = document.getElementById("suggestions");
const image = document.getElementById("image");


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
        const res = await fetch(`/fetch?word=${encodeURIComponent(word)}`);
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
        return;
    }

    // Get / show suggestions
    const suggestions = await fetchSuggestions(lastWord);
    showSuggestions(suggestions);
});

// When space bar
input.addEventListener("keyup", async (event) => {
    if (event.key === ' ') {
        const word = getLastWord(input.value);

        // Get / update <img>
        const imgSrc = await fetchImage(word);
        const image = document.getElementById("image")
        if (imgSrc) {
            image.src = imgSrc;
            image.style.display = "block";
        } else {
            image.style.display = "none";
        }
    }
});