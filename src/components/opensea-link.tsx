import type { ReactNode } from "react";

type OpenSeaLinkProps = {
  href: string;
  children?: ReactNode;
  className?: string;
};

export function OpenSeaLink({ href, children = "View on OpenSea", className }: OpenSeaLinkProps) {
  return (
    <a href={href} target="_blank" rel="noreferrer" className={className}>
      {children}
    </a>
  );
}
