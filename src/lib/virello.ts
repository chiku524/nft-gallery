export const VIRELLO_BASE = "/virello";

export function virelloPath(path = ""): string {
  if (!path || path === "/") {
    return VIRELLO_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${VIRELLO_BASE}${suffix}`;
}
