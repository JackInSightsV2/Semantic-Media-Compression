import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SemanticGuard - Content Protection Dashboard",
  description: "Protect your semantic intellectual property with blockchain technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-50 font-sans">
        {children}
      </body>
    </html>
  );
}
