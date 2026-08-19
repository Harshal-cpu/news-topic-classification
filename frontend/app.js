// Backend API URL - replace with your Render backend URL
const API_URL = "https://news-topic-classification-api.onrender.com";

const SAMPLES = {
    "🚀 Space Exploration": "NASA's Perseverance rover has discovered organic molecules on Mars, suggesting the red planet may have once harbored microbial life. The rover's instruments detected complex carbon-based compounds in ancient lake bed rocks, providing the strongest evidence yet that Mars was once habitable.",
    "⚽ Sports News": "In a thrilling championship game, the home team secured victory with a last-minute goal. The stadium erupted as the striker found the back of the net in injury time, completing an incredible comeback from two goals down. Fans celebrated the historic win that secured the team's first title in over a decade.",
    "💻 Technology": "Apple unveiled its latest iPhone featuring revolutionary AI capabilities and improved camera technology. The new device includes advanced machine learning processors that enable real-time language translation and enhanced computational photography. Pre-orders begin next week with shipping expected in early next month.",
    "🏥 Medical Breakthrough": "Researchers at Johns Hopkins University have developed a new gene therapy treatment showing promising results in clinical trials for treating certain types of cancer. The innovative approach uses modified immune cells to target and destroy cancer cells while leaving healthy tissue unharmed.",
    "💰 Business & Finance": "Stock markets reached record highs today as investors responded positively to strong corporate earnings reports. Technology stocks led the rally, with major companies reporting better-than-expected quarterly results. Analysts predict continued growth in the coming months.",
    "🔬 Scientific Discovery": "Scientists have identified a new species of deep-sea creature living near hydrothermal vents in the Pacific Ocean. The bioluminescent organism has unique adaptations allowing it to survive in extreme pressure and temperature conditions, providing insights into how life might exist on other planets."
};

function formatCategoryName(category) {
    if (!category) return "Unknown";
    const parts = category.split(".");
    if (parts.length > 1) {
        const main = parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
        const sub = parts.slice(1).join(" ").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
        return `${main}: ${sub}`;
    }
    return category.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

function renderSamples() {
    const container = document.getElementById("samples");
    Object.entries(SAMPLES).forEach(([title, text]) => {
        const btn = document.createElement("button");
        btn.className = "sample-btn";
        btn.textContent = title;
        btn.addEventListener("click", () => {
            document.getElementById("news-text").value = text;
        });
        container.appendChild(btn);
    });
}

function normalizeConfidence(scores) {
    if (scores.length < 2) return scores.map(() => 50);
    const min = Math.min(...scores);
    const max = Math.max(...scores);
    if (max === min) return scores.map(() => 50);
    return scores.map(s => (s - min) / (max - min) * 100);
}

function renderResults(data) {
    const results = document.getElementById("results");
    results.classList.remove("hidden");

    document.getElementById("result-box").textContent = `📰 Category: ${formatCategoryName(data.predicted_category)}`;

    const bars = document.getElementById("confidence-bars");
    bars.innerHTML = "";

    const normalized = normalizeConfidence(data.top_predictions.map(p => p.confidence));

    data.top_predictions.forEach((pred, i) => {
        const item = document.createElement("div");
        item.className = "confidence-item";

        const label = document.createElement("div");
        label.className = "confidence-label";
        label.textContent = formatCategoryName(pred.category);

        const bar = document.createElement("div");
        bar.className = "confidence-bar";

        const fill = document.createElement("div");
        fill.className = "confidence-fill";
        fill.style.width = `${Math.max(normalized[i], 3)}%`;
        fill.textContent = `${normalized[i].toFixed(1)}%`;

        bar.appendChild(fill);
        item.appendChild(label);
        item.appendChild(bar);
        bars.appendChild(item);
    });

    document.getElementById("article-preview").textContent = data.text;
    results.scrollIntoView({ behavior: "smooth" });
}

async function classify() {
    const text = document.getElementById("news-text").value.trim();
    const errorMsg = document.getElementById("error-msg");
    const loading = document.getElementById("loading");
    const btn = document.getElementById("classify-btn");

    errorMsg.classList.add("hidden");

    if (!text) {
        errorMsg.textContent = "⚠️ Please enter some text to classify!";
        errorMsg.classList.remove("hidden");
        return;
    }

    btn.disabled = true;
    loading.classList.remove("hidden");

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `Request failed (${response.status})`);
        }

        renderResults(data);
    } catch (err) {
        errorMsg.textContent = `❌ ${err.message}`;
        errorMsg.classList.remove("hidden");
    } finally {
        btn.disabled = false;
        loading.classList.add("hidden");
    }
}

document.getElementById("classify-btn").addEventListener("click", classify);
document.addEventListener("DOMContentLoaded", renderSamples);
