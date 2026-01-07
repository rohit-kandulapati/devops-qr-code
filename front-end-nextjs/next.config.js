/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Required for Docker optimization
  
  // Allow images from S3 bucket (adjust to your bucket name)
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.s3.*.amazonaws.com',
      },
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
      },
    ],
  },
};

module.exports = nextConfig;