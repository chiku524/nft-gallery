export const SCRIBBLINS_BASE = "/scribblins";

export function scribblinsPath(path = ""): string {
  if (!path || path === "/") {
    return SCRIBBLINS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${SCRIBBLINS_BASE}${suffix}`;
}
