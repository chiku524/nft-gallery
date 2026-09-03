export const FOXKINS_BASE = "/foxkins";

export function foxkinsPath(path = ""): string {
  if (!path || path === "/") {
    return FOXKINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${FOXKINS_BASE}${suffix}`;
}
