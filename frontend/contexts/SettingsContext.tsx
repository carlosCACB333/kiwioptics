"use client";

import { createContext, ReactNode } from "react";
import { defaultSettings } from "../config";
import { useLocalStorage } from "@/hooks/";
import { SettingsContextProps } from "@/@types/settings";

const initialState: SettingsContextProps = {
  ...defaultSettings,
  onToggleMode: () => {},
};

const SettingsContext = createContext(initialState);

type Props = {
  children: ReactNode;
};

function SettingsProvider({ children }: Props) {
  const [settings, setSettings] = useLocalStorage("settings", {
    ...defaultSettings,
  });

  const onToggleMode = () => {
    setSettings({
      ...settings,
      themeMode: settings.themeMode === "light" ? "dark" : "light",
    });
  };

  return (
    <SettingsContext.Provider
      value={{
        ...settings,
        onToggleMode,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export { SettingsProvider, SettingsContext };
