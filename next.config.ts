import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    localPatterns: [
      { pathname: "/**" },
      { pathname: "/traits/**", search: "?v=*" },
    ],
  },
  async redirects() {
    return [
      { source: "/traits", destination: "/pugs-on-the-block/traits", permanent: true },
      { source: "/gallery", destination: "/pugs-on-the-block/gallery", permanent: true },
      { source: "/launch", destination: "/pugs-on-the-block/launch", permanent: true },
    ];
  },
};

export default nextConfig;
