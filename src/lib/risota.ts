export const RISOTA_BASE = "/risota";

export function risotaPath(path = ""): string {
  if (!path || path === "/") {
    return RISOTA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${RISOTA_BASE}${suffix}`;
}
