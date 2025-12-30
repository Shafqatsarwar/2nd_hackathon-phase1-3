import { sql } from "@vercel/postgres";

async function run() {
    console.log("Initializing Better Auth tables...");

    try {
        await sql`
            CREATE TABLE IF NOT EXISTS "user" (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                "emailVerified" BOOLEAN NOT NULL DEFAULT FALSE,
                image TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "session" (
                id TEXT PRIMARY KEY,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                token TEXT NOT NULL UNIQUE,
                "expiresAt" TIMESTAMPTZ NOT NULL,
                "ipAddress" TEXT,
                "userAgent" TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "account" (
                id TEXT PRIMARY KEY,
                "accountId" TEXT NOT NULL,
                "providerId" TEXT NOT NULL,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                "accessToken" TEXT,
                "refreshToken" TEXT,
                "idToken" TEXT,
                "accessTokenExpiresAt" TIMESTAMPTZ,
                "refreshTokenExpiresAt" TIMESTAMPTZ,
                scope TEXT,
                password TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "verification" (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                "expiresAt" TIMESTAMPTZ NOT NULL,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`CREATE INDEX IF NOT EXISTS idx_session_user ON "session"("userId");`;
        await sql`CREATE INDEX IF NOT EXISTS idx_account_user ON "account"("userId");`;
        await sql`CREATE INDEX IF NOT EXISTS idx_verification_identifier ON "verification"(identifier);`;

        await sql`
            CREATE TABLE IF NOT EXISTS user_mappings (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                file_type VARCHAR(50) NOT NULL,
                mapping JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, file_type)
            );
        `;

        console.log("Done initializing database.");
    } catch (error) {
        console.error("Failed to initialize database:", error);
        process.exit(1);
    }
}

run();
