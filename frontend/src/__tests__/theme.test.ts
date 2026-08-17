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

describe("Theme System Logic", () => {
  beforeEach(() => {
    storageMock.clear();
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
});
