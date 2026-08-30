export const AFTERIMAGES_BASE = "/afterimages";

export function afterimagesPath(path = ""): string {
  if (!path || path === "/") {
    return AFTERIMAGES_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${AFTERIMAGES_BASE}${suffix}`;
}
