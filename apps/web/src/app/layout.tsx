import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Simple Memo App",
  description: "Local storage based memo application",
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
