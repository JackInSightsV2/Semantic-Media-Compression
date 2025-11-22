import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Semantical.Ink - Transform, Protect, and Monetize Your Semantic Content",
  description: "Platform for indie creators to transform, protect, and monetize their semantic content",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

