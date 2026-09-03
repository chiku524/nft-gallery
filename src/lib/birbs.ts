export const BIRBS_BASE = "/birbs";

export function birbsPath(path = ""): string {
  if (!path || path === "/") {
    return BIRBS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${BIRBS_BASE}${suffix}`;
}
