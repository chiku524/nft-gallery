export const PERFIN_BASE = "/perfin";

export function perfinPath(path = ""): string {
  if (!path || path === "/") {
    return PERFIN_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${PERFIN_BASE}${suffix}`;
}
