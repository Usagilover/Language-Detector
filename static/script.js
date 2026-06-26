const input = document.getElementById("input");
const charCount = document.getElementById("charCount");
const sendBtn = document.getElementById("sendBtn");
const result = document.getElementById("result");

const SEGMENTS = 16;

input.addEventListener("input", () => {
  charCount.textContent = input.value.length;
});

sendBtn.addEventListener("click", () => detect());
input.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") detect();
});

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function meterRow(item, isTop) {
  const lit = Math.round(item.confidence * SEGMENTS);
  let segs = "";
  for (let i = 0; i < SEGMENTS; i++) {
    const cls = i < lit ? `is-lit${isTop ? " top" : ""}` : "";
    segs += `<span class="meter__seg ${cls}"></span>`;
  }
  return `
    <div class="meter">
      <span class="meter__lang">${escapeHtml(item.name)}</span>
      <span class="meter__track">${segs}</span>
      <span class="meter__pct">${(item.confidence * 100).toFixed(0)}%</span>
    </div>`;
}

async function detect() {
  const text = input.value.trim();
  if (!text) {
    showError("Send some text to decode.");
    return;
  }

  sendBtn.disabled = true;
  sendBtn.querySelector(".btn__label").textContent = "DECODING…";

  try {
    const res = await fetch("/api/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Something went wrong on the line.");
      return;
    }
    render(data);
  } catch (err) {
    showError("Lost the signal — couldn't reach the decoder.");
  } finally {
    sendBtn.disabled = false;
    sendBtn.querySelector(".btn__label").textContent = "TRANSMIT";
  }
}

function showError(msg) {
  result.className = "telegram telegram--error";
  result.innerHTML = `<p class="telegram__hint">⚠ ${escapeHtml(msg)}</p>`;
}

function render(data) {
  result.className = "telegram";

  const top = data.detected;
  const rows = data.top
    .map((item, i) => meterRow(item, i === 0))
    .join("");

  result.innerHTML = `
    <div class="telegram__body">
      <div class="seal">
        <span class="seal__code">${escapeHtml(top.code.toUpperCase())}</span>
        <span class="seal__tag">DECODED</span>
      </div>
      <div class="readout">
        <p class="readout__lang">${escapeHtml(top.name)}</p>
        <p class="readout__conf">CONFIDENCE ${(top.confidence * 100).toFixed(1)}%</p>
        ${rows}
      </div>
    </div>`;
}
