class ComboBox {
  constructor(container) {
    this.container = container;
    this.input = container.querySelector(".combo-input");
    this.hidden = container.querySelector(".combo-value");
    this.list = container.querySelector(".combo-list");

    this.labelField = container.dataset.label || "label";
    this.valueField = container.dataset.value || "value";

    const sourceId = container.dataset.source;
    this.data = JSON.parse(
      document.getElementById(sourceId).textContent
    ); 

    this.init();
  }

  init() {
    this.input.addEventListener("input", () => this.onInput());
    this.input.addEventListener("change", () => this.onChange());

    document.addEventListener("click", (e) => {
      if (!this.container.contains(e.target)) {
        this.list.style.display = "none";
      }
    });
  }

  updateHighlight(items) {
    items.forEach((el, i) => {
        el.style.background = i === this.highlightIndex ? "#ddd" : "";
    });
  }

  onInput() {
    const value = this.input.value.toLowerCase();
    this.list.innerHTML = "";

    const filtered = this.data.filter(item =>
      item[this.labelField].toLowerCase().includes(value)
    );

    filtered.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item[this.labelField];

      li.onclick = () => {
        this.select(item);
      };

      this.list.appendChild(li);
    });

    this.list.style.display = filtered.length ? "block" : "none";
  }

  select(item) {
    this.input.value = item[this.labelField];
    this.hidden.value = item[this.valueField];
    this.list.style.display = "none";
  }

  onChange() {
    const match = this.data.find(item =>
      item[this.labelField] === this.input.value
    );

    this.hidden.value = match ? match[this.valueField] : "";
  }

  onKeyDown(e) {
    const items = this.list.querySelectorAll("li");

    if (!items.length) return;

    if (e.key === "ArrowDown") {
        e.preventDefault();
        this.highlightIndex = (this.highlightIndex + 1) % items.length;
        this.updateHighlight(items);
    }

    if (e.key === "ArrowUp") {
        e.preventDefault();
        this.highlightIndex =
        (this.highlightIndex - 1 + items.length) % items.length;
        this.updateHighlight(items);
    }

    if (e.key === "Enter") {
        if (this.highlightIndex >= 0) {
        e.preventDefault();
        items[this.highlightIndex].click();
        }
    }

    if (e.key === "Tab") {
        if (this.highlightIndex >= 0) {
        items[this.highlightIndex].click();
        }
        // ⚠️ NO prevenir default → deja que tab cambie de campo
    }
    }
}

// 🔹 Inicializar TODOS los combos
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".combo").forEach(el => {
    new ComboBox(el);
  });
});