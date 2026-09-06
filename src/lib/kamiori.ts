export const KAMIORI_BASE = "/kamiori";

export function kamioriPath(path = ""): string {
  if (!path || path === "/") {
    return KAMIORI_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${KAMIORI_BASE}${suffix}`;
}
