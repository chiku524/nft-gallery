export const BOOGIESQUAD_BASE = "/boogiesquad";

export function boogiesquadPath(path = ""): string {
  if (!path || path === "/") {
    return BOOGIESQUAD_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${BOOGIESQUAD_BASE}${suffix}`;
}
