export const STRANGERS_BASE = "/strangers";

export function strangersPath(path = ""): string {
  if (!path || path === "/") {
    return STRANGERS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${STRANGERS_BASE}${suffix}`;
}
