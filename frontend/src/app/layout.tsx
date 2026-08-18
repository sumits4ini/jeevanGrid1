import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AppShell } from "@/components/layout/AppShell";
import { ThemeProvider } from "@/context/ThemeContext";
import { EOCProvider } from "@/context/EOCContext";

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
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              try {
                var theme = localStorage.getItem('jeevangrid-theme') || 'dark';
                document.documentElement.classList.add(theme);
                document.documentElement.setAttribute('data-theme', theme);
              } catch (e) {}
            `,
          }}
        />
      </head>
      <body className={`${inter.className} min-h-screen bg-background text-foreground antialiased selection:bg-cyan-500 selection:text-white`}>
        <ThemeProvider>
          <EOCProvider>
            <AppShell>{children}</AppShell>
          </EOCProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
