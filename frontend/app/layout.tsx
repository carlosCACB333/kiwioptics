import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

import ThemeProvider from "../theme/index";
import Header from "@/components/header/Header";
import { SettingsProvider } from "@/contexts/SettingsContext";

export const metadata = {
  title: "Kiwioptics",
  description: "App web de gestión de prescripciones de las ópticas",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>
        <SettingsProvider>
          <ThemeProvider>
            <Header transparent />
            {children}
          </ThemeProvider>
        </SettingsProvider>
      </body>
    </html>
  );
}
