export const ROBIN_BANX_BASE = "/robinbanx";

export function robinBanxPath(path = ""): string {
  if (!path || path === "/") return ROBIN_BANX_BASE;
  return `${ROBIN_BANX_BASE}${path.startsWith("/") ? path : `/${path}`}`;
}
