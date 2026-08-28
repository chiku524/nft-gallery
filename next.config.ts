import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    localPatterns: [
      { pathname: "/**" },
      { pathname: "/traits/**", search: "?v=*" },
    ],
  },
};

export default nextConfig;
