import { Analytics } from "@vercel/analytics/react";
import { Inter, Roboto_Mono } from "next/font/google";
import Script from "next/script";
import Navigation from "../components/Navigation";
import { AuthProvider } from "../contexts/AuthContext";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const robotoMono = Roboto_Mono({
  variable: "--font-roboto-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "EduAIthon",
  description: "AI-powered personalized learning platform",
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <head>
        <Script id="microsoft-clarity" strategy="afterInteractive">
          {`
            (function(c,l,a,r,i,t,y){
              c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
              t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
              y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
            })(window, document, "clarity", "script", "r6ejow727a");
          `}
        </Script>
      </head>
      <body className={`${inter.variable} ${robotoMono.variable} antialiased`}>
        <AuthProvider>
          <Navigation />
          <main className="min-h-screen">{children}</main>
        </AuthProvider>
        <Analytics />
      </body>
    </html>
  );
} 