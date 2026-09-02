export const MOCHINS_BASE = "/mochins";

export function mochinsPath(path = ""): string {
  if (!path || path === "/") {
    return MOCHINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${MOCHINS_BASE}${suffix}`;
}
