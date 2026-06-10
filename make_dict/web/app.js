const state = {
  terms: [],
  visible: [],
  stats: {},
  search: "",
  filter: "all",
  renderLimit: 500,
  sortField: "rowIndex",
  sortDirection: "asc",
};

const $ = (id) => document.getElementById(id);
const collator = new Intl.Collator(["vi", "zh-Hant"], { numeric: true, sensitivity: "base" });

function toast(message) {
  const node = $("toast");
  node.textContent = message;
  node.classList.add("visible");
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => node.classList.remove("visible"), 2600);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || `HTTP ${response.status}`);
  }
  return data;
}

function setBusy(button, busy) {
  if (!button) return;
  button.disabled = busy;
}

async function loadTerms() {
  const data = await api("/api/terms");
  state.terms = data.terms;
  state.stats = data.stats;
  state.renderLimit = 500;
  applyFilters();
  updateStats();
  renderTable();
}

function normalized(text) {
  return (text || "").toString().toLowerCase();
}

function applyFilters() {
  const query = normalized(state.search).trim();
  const terms = query ? query.split(/\s+/).filter(Boolean) : [];
  state.visible = state.terms.filter((term) => {
    if (state.filter === "withChinese" && !term.chinese) return false;
    if (state.filter === "blankChinese" && term.chinese) return false;
    if (state.filter === "duplicate" && !term.duplicate) return false;
    if (!terms.length) return true;
    const text = normalized(
      [
        term.vietnamese,
        term.chinese,
        term.cleanVietnamese,
        term.pinyin,
        term.telex,
        term.rowIndex,
      ].join("\n"),
    );
    return terms.every((part) => text.includes(part));
  });
  sortVisibleTerms();
}

function compareValues(first, second, direction) {
  const firstEmpty = first === null || first === undefined || first === "";
  const secondEmpty = second === null || second === undefined || second === "";
  if (firstEmpty && secondEmpty) return 0;
  if (firstEmpty) return 1;
  if (secondEmpty) return -1;
  const result = typeof first === "number" && typeof second === "number"
    ? first - second
    : collator.compare(String(first), String(second));
  return result * direction;
}

function sortVisibleTerms() {
  const direction = state.sortDirection === "desc" ? -1 : 1;
  const field = state.sortField;
  state.visible.sort((first, second) => {
    const result = compareValues(first[field], second[field], direction);
    if (result !== 0) return result;
    return first.rowIndex - second.rowIndex;
  });
}

function updateStats() {
  $("totalCount").textContent = state.stats.total ?? 0;
  $("withChineseCount").textContent = state.stats.withChinese ?? 0;
  $("blankChineseCount").textContent = state.stats.blankChinese ?? 0;
  $("visibleCount").textContent = Math.min(state.renderLimit, state.visible.length);
}

function renderTable() {
  const body = $("termsBody");
  body.innerHTML = "";
  updateSortHeaders();
  const rows = state.visible.slice(0, state.renderLimit);
  const fragment = document.createDocumentFragment();
  for (const term of rows) {
    const tr = document.createElement("tr");
    const clearButton = term.chinese
      ? `<button class="danger" data-action="clear" data-row="${term.rowIndex}">清空中文</button>`
      : "";
    tr.innerHTML = `
      <td>${term.rowIndex}</td>
      <td>${escapeHtml(term.vietnamese)}</td>
      <td class="${term.chinese ? "" : "empty-cell"}">${escapeHtml(term.chinese)}</td>
      <td>${escapeHtml(term.cleanVietnamese)}</td>
      <td>${escapeHtml(term.pinyin)}</td>
      <td>${escapeHtml(term.telex)}</td>
      <td>
        <div class="row-actions">
          <button class="secondary" data-action="edit" data-row="${term.rowIndex}">編輯</button>
          ${clearButton}
        </div>
      </td>
    `;
    fragment.appendChild(tr);
  }
  body.appendChild(fragment);
  if (state.visible.length > state.renderLimit) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td colspan="7" class="more-row">
        已顯示 ${state.renderLimit} / ${state.visible.length} 筆
        <button type="button" class="secondary" id="showMoreButton">顯示更多</button>
      </td>
    `;
    body.appendChild(tr);
  }
}

function updateSortHeaders() {
  document.querySelectorAll("th").forEach((header) => header.removeAttribute("aria-sort"));
  document.querySelectorAll(".sort-button").forEach((button) => {
    const indicator = button.querySelector(".sort-indicator");
    const active = button.dataset.sort === state.sortField;
    button.classList.toggle("active", active);
    if (indicator) {
      indicator.textContent = active ? (state.sortDirection === "asc" ? "↑" : "↓") : "";
    }
    if (active) {
      button.closest("th")?.setAttribute("aria-sort", state.sortDirection === "asc" ? "ascending" : "descending");
    }
  });
}

function escapeHtml(value) {
  return (value || "").toString().replace(/[&<>"']/g, (char) => {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[char];
  });
}

async function addTerm(event) {
  event.preventDefault();
  const vietnamese = $("vietnameseInput").value.trim();
  const chinese = $("chineseInput").value.trim();
  if (!vietnamese) return;
  const result = await api("/api/terms", {
    method: "POST",
    body: JSON.stringify({ vietnamese, chinese }),
  });
  $("vietnameseInput").value = "";
  $("chineseInput").value = "";
  await loadTerms();
  toast(result.backup ? "已新增詞彙，並建立備份" : "已新增詞彙");
}

function openEdit(rowIndex) {
  const term = state.terms.find((item) => item.rowIndex === rowIndex);
  if (!term) return;
  $("editRow").value = term.rowIndex;
  $("editVietnamese").value = term.vietnamese;
  $("editChinese").value = term.chinese;
  $("editDialog").showModal();
}

async function saveEdit(event) {
  event.preventDefault();
  const rowIndex = Number($("editRow").value);
  const result = await api(`/api/terms/${rowIndex}`, {
    method: "PUT",
    body: JSON.stringify({
      vietnamese: $("editVietnamese").value.trim(),
      chinese: $("editChinese").value.trim(),
    }),
  });
  $("editDialog").close();
  await loadTerms();
  toast(result.backup ? "已儲存詞彙，並建立備份" : "已儲存詞彙");
}

async function clearChinese(rowIndex) {
  const term = state.terms.find((item) => item.rowIndex === rowIndex);
  if (!term) return;
  const confirmed = window.confirm(`清空「${term.vietnamese}」的中文翻譯？`);
  if (!confirmed) return;
  const result = await api(`/api/terms/${rowIndex}`, { method: "DELETE" });
  await loadTerms();
  toast(result.backup ? "已清空中文欄，並建立備份" : "已清空中文欄");
}

async function importFile(file) {
  const text = await file.text();
  if (!text.trim()) {
    toast("匯入檔案沒有內容");
    return;
  }
  const format = file.name.toLowerCase().endsWith(".json") ? "json" : "tsv";
  const mode = $("importModeSelect").value;
  if (mode === "replace") {
    const confirmed = window.confirm("取代匯入會先清空所有中文欄，再套用匯入內容。確定繼續？");
    if (!confirmed) return;
  }
  const result = await api("/api/import", {
    method: "POST",
    body: JSON.stringify({ text, format, mode }),
  });
  await loadTerms();
  const modeText = result.mode === "replace" ? "取代" : "合併";
  const backupText = result.backup ? "，並建立備份" : "";
  toast(`${modeText}匯入 ${result.imported} 筆，新增 ${result.appended} 筆，更新 ${result.updated} 筆，略過 ${result.skipped} 行${backupText}`);
}

function downloadText(filename, text, type) {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

async function exportGlossary(format) {
  const data = await api("/api/export");
  if (format === "json") {
    downloadText("glossary.json", data.json, "application/json;charset=utf-8");
  } else {
    downloadText("glossary.tsv", data.tsv, "text/tab-separated-values;charset=utf-8");
  }
  toast(`已匯出 ${data.count} 筆`);
}

function showOutput(result) {
  const output = $("commandOutput");
  output.style.display = "block";
  output.textContent = result.output || "(沒有輸出)";
}

async function generateYaml() {
  const button = $("generateButton");
  setBusy(button, true);
  try {
    const result = await api("/api/generate", {
      method: "POST",
      body: JSON.stringify({ syncRoot: true }),
    });
    showOutput(result);
    if (!result.ok) throw new Error("產生 YAML 失敗");
    toast("已產生並同步 YAML");
    await loadTerms();
  } finally {
    setBusy(button, false);
  }
}

async function verifyProject() {
  const button = $("verifyButton");
  setBusy(button, true);
  try {
    const result = await api("/api/verify", { method: "POST", body: "{}" });
    showOutput(result);
    if (!result.ok) throw new Error("驗證失敗");
    toast("驗證完成");
  } finally {
    setBusy(button, false);
  }
}

function bindEvents() {
  $("addForm").addEventListener("submit", (event) => {
    addTerm(event).catch((error) => toast(error.message));
  });
  $("editForm").addEventListener("submit", (event) => {
    saveEdit(event).catch((error) => toast(error.message));
  });
  $("cancelEditButton").addEventListener("click", () => $("editDialog").close());
  $("searchInput").addEventListener("input", (event) => {
    state.search = event.target.value;
    state.renderLimit = 500;
    applyFilters();
    updateStats();
    renderTable();
  });
  $("filterSelect").addEventListener("change", (event) => {
    state.filter = event.target.value;
    state.renderLimit = 500;
    applyFilters();
    updateStats();
    renderTable();
  });
  document.querySelectorAll(".sort-button").forEach((button) => {
    button.addEventListener("click", () => {
      const nextField = button.dataset.sort;
      if (state.sortField === nextField) {
        state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
      } else {
        state.sortField = nextField;
        state.sortDirection = "asc";
      }
      state.renderLimit = 500;
      sortVisibleTerms();
      updateStats();
      renderTable();
    });
  });
  $("termsBody").addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    if (button.id === "showMoreButton") {
      state.renderLimit += 500;
      renderTable();
      updateStats();
      return;
    }
    const row = Number(button.dataset.row);
    if (button.dataset.action === "edit") openEdit(row);
    if (button.dataset.action === "clear") clearChinese(row).catch((error) => toast(error.message));
  });
  $("refreshButton").addEventListener("click", () => loadTerms().then(() => toast("已重新載入")).catch((error) => toast(error.message)));
  $("generateButton").addEventListener("click", () => generateYaml().catch((error) => toast(error.message)));
  $("verifyButton").addEventListener("click", () => verifyProject().catch((error) => toast(error.message)));
  $("importButton").addEventListener("click", () => $("importFile").click());
  $("importFile").addEventListener("change", (event) => {
    const file = event.target.files?.[0];
    if (file) importFile(file).catch((error) => toast(error.message));
    event.target.value = "";
  });
  $("exportTsvButton").addEventListener("click", () => exportGlossary("tsv").catch((error) => toast(error.message)));
  $("exportJsonButton").addEventListener("click", () => exportGlossary("json").catch((error) => toast(error.message)));
}

bindEvents();
loadTerms().catch((error) => toast(error.message));
