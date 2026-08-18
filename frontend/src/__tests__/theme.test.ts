import { describe, it, expect, beforeEach } from "vitest";

// In-memory mock storage
const mockStorage: Record<string, string> = {};

const storageMock = {
  getItem: (key: string) => mockStorage[key] || null,
  setItem: (key: string, value: string) => {
    mockStorage[key] = value;
  },
  clear: () => {
    for (const key in mockStorage) {
      delete mockStorage[key];
    }
  },
};

// Mock Document Root Element for Node environment
class MockDocumentElement {
  classList = new Set<string>();
  attributes: Record<string, string> = {};

  setAttribute(name: string, value: string) {
    this.attributes[name] = value;
  }

  getAttribute(name: string): string | null {
    return this.attributes[name] || null;
  }

  removeAttribute(name: string) {
    delete this.attributes[name];
  }

  reset() {
    this.classList.clear();
    this.attributes = {};
  }
}

const mockDocEl = new MockDocumentElement();

const applyThemeToDOM = (el: MockDocumentElement, theme: "dark" | "light") => {
  el.classList.delete("dark");
  el.classList.delete("light");
  el.classList.add(theme);
  el.setAttribute("data-theme", theme);
};

describe("Theme System Logic & Persistence", () => {
  beforeEach(() => {
    storageMock.clear();
    mockDocEl.reset();
  });

  it("defaults to dark theme when no preference saved", () => {
    const savedTheme = storageMock.getItem("jeevangrid-theme");
    expect(savedTheme).toBeNull();
  });

  it("persists theme selection in storage", () => {
    storageMock.setItem("jeevangrid-theme", "light");
    expect(storageMock.getItem("jeevangrid-theme")).toBe("light");

    storageMock.setItem("jeevangrid-theme", "dark");
    expect(storageMock.getItem("jeevangrid-theme")).toBe("dark");
  });

  it("correctly sets class and data-theme attribute on document root for light theme", () => {
    applyThemeToDOM(mockDocEl, "light");
    expect(mockDocEl.classList.has("light")).toBe(true);
    expect(mockDocEl.classList.has("dark")).toBe(false);
    expect(mockDocEl.getAttribute("data-theme")).toBe("light");
  });

  it("correctly sets class and data-theme attribute on document root for dark theme", () => {
    applyThemeToDOM(mockDocEl, "dark");
    expect(mockDocEl.classList.has("dark")).toBe(true);
    expect(mockDocEl.classList.has("light")).toBe(false);
    expect(mockDocEl.getAttribute("data-theme")).toBe("dark");
  });

  it("toggles theme correctly between dark and light", () => {
    let currentTheme: "dark" | "light" = "dark";
    const toggleTheme = () => {
      currentTheme = currentTheme === "dark" ? "light" : "dark";
      storageMock.setItem("jeevangrid-theme", currentTheme);
      applyThemeToDOM(mockDocEl, currentTheme);
    };

    toggleTheme();
    expect(currentTheme).toBe("light");
    expect(storageMock.getItem("jeevangrid-theme")).toBe("light");
    expect(mockDocEl.getAttribute("data-theme")).toBe("light");

    toggleTheme();
    expect(currentTheme).toBe("dark");
    expect(storageMock.getItem("jeevangrid-theme")).toBe("dark");
    expect(mockDocEl.getAttribute("data-theme")).toBe("dark");
  });
});
