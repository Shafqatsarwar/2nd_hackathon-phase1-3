/** @type {import('next').NextConfig} */
const DEFAULT_BACKEND_URL = "http://127.0.0.1:800";

const sanitizeBackendUrl = (value) => {
    let base = value || DEFAULT_BACKEND_URL;
    base = base.replace(/\/+$/, ""); // drop trailing slashes
    return base.endsWith("/api") ? base : `${base}/api`;
};

const nextConfig = {
    // Next.js 15+ ignores
    typescript: {
        ignoreBuildErrors: true,
    },

    async rewrites() {
        const backendUrl = sanitizeBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);
        return [
            {
                source: "/api/:path*",
                destination: `${backendUrl}/:path*`,
            },
        ];
    },
};

module.exports = nextConfig;
