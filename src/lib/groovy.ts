export const GROOVY_BASE = "/groovy";

export function groovyPath(path = ""): string {
  if (!path || path === "/") {
    return GROOVY_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${GROOVY_BASE}${suffix}`;
}
