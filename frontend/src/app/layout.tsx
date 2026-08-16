import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AppShell } from "@/components/layout/AppShell";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "JeevanGrid — Disaster Intelligence & Emergency Response Platform",
  description: "Next-generation real-world disaster intelligence, spatial risk analytics, and emergency response decision platform for SIH 2026.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} min-h-screen bg-background text-slate-100 antialiased`}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
