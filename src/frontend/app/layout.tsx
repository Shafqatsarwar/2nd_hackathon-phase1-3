import type { Metadata } from "next";
import "./globals.css";
import GuestButton from "../components/GuestButton";

export const metadata: Metadata = {
    title: "The Evolution of Todo - AI-Powered Vault",
    description: "Next.js + FastAPI + AI Todo Ecosystem",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className="antialiased">
                {children}
                <GuestButton />
            </body>
        </html>
    );
}
