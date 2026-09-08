export const CERA_BASE = "/cera";

export function ceraPath(path = ""): string {
  if (!path || path === "/") {
    return CERA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${CERA_BASE}${suffix}`;
}
