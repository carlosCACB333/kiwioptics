/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ["zone-assets-api.vercel.app"],
  },
};

module.exports = nextConfig;
