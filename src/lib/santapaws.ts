export const SANTAPAWS_BASE = "/santapaws";

export function santapawsPath(path = ""): string {
  if (!path || path === "/") {
    return SANTAPAWS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${SANTAPAWS_BASE}${suffix}`;
}
