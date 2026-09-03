import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    localPatterns: [
      { pathname: "/**" },
      { pathname: "/traits/**", search: "?v=*" },
      { pathname: "/inklings-traits/**", search: "?v=*" },
      { pathname: "/purrkins-traits/**", search: "?v=*" },
      { pathname: "/hoodkins-traits/**", search: "?v=*" },
      { pathname: "/shookums-traits/**", search: "?v=*" },
      { pathname: "/foxkins-traits/**", search: "?v=*" },
    ],
  },
  async redirects() {
    return [
      { source: "/traits", destination: "/loopkins/traits", permanent: false },
      { source: "/gallery", destination: "/loopkins/gallery", permanent: false },
      { source: "/launch", destination: "/loopkins/launch", permanent: false },
      { source: "/pugs-on-the-block", destination: "/loopkins", permanent: false },
      { source: "/pugs-on-the-block/:path*", destination: "/loopkins/:path*", permanent: false },
    ];
  },
};

export default nextConfig;
