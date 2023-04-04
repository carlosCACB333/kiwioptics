export type ThemeMode = "light" | "dark";
export type SettingsValueProps = {
  themeMode: ThemeMode;
};

export type SettingsContextProps = {
  themeMode: ThemeMode;
  onToggleMode: VoidFunction;
};
