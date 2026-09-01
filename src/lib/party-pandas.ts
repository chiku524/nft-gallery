export const PARTY_PANDAS_BASE = "/party-pandas";

export function partyPandasPath(path = ""): string {
  if (!path || path === "/") {
    return PARTY_PANDAS_BASE;
  }
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${PARTY_PANDAS_BASE}${suffix}`;
}
