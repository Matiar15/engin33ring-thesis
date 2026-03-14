import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react-swc";
// @ts-expect-error: IDK why it is like that, but it does not impact application startup.
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
  },
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
});
