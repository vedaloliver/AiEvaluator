/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@ai-evaluator/shared-types'],
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000',
    EVALUATOR_SERVICE_URL: process.env.EVALUATOR_SERVICE_URL || 'http://localhost:3001',
  },
}

module.exports = nextConfig
