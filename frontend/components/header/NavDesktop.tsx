import { Stack } from "@mui/material";
import { NavProps } from "@/@types/layout";
import { NavItemDesktop } from "./NavItemDesktop";

export default function NavDesktop({
  isScrolling,
  isTransparent,
  navConfig,
}: NavProps) {
  return (
    <Stack
      direction="row"
      spacing={6}
      sx={{
        ml: 6,
        color: "text.secondary",
        ...(isTransparent && {
          color: "inherit",
        }),
        ...(isScrolling && {
          color: "text.secondary",
        }),
      }}
    >
      {navConfig.map((link) => (
        <NavItemDesktop
          key={link.title}
          item={link}
          isScrolling={isScrolling}
          isTransparent={isTransparent}
        />
      ))}
    </Stack>
  );
}
