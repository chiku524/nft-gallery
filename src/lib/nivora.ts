export const NIVORA_BASE = "/nivora";

export function nivoraPath(path = ""): string {
  if (!path || path === "/") {
    return NIVORA_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${NIVORA_BASE}${suffix}`;
}
