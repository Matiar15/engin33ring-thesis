import "@testing-library/jest-dom";

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

Object.defineProperty(HTMLMediaElement.prototype, "canPlayType", {
  configurable: true,
  value: () => "probably",
});

Object.defineProperty(HTMLCanvasElement.prototype, "getContext", {
  configurable: true,
  value: () => ({
    clearRect: () => {},
    strokeRect: () => {},
    beginPath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    stroke: () => {},
    fillRect: () => {},
    fillText: () => {},
    measureText: () => ({ width: 10 }),
    set shadowColor(_: string) {},
    set shadowBlur(_: number) {},
    set strokeStyle(_: string) {},
    set lineWidth(_: number) {},
    set fillStyle(_: string) {},
    set font(_: string) {},
  }),
});
