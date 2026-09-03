export const SHOOKUMS_BASE = "/shookums";

export function shookumsPath(path = ""): string {
  if (!path || path === "/") {
    return SHOOKUMS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${SHOOKUMS_BASE}${suffix}`;
}
