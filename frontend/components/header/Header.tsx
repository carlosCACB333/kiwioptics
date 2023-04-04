"use client";
import NextLink from "next/link";
import {
  Box,
  Stack,
  Button,
  AppBar,
  Divider,
  Container,
  Link,
  Typography,
  IconButton,
} from "@mui/material";
import useResponsive from "@/hooks/useResponsive";
import useOffSetTop from "@/hooks/useOffSetTop";
import { ToolbarShadowStyle, ToolbarStyle } from "./HeaderToolbarStyle";
import { HEADER_DESKTOP_HEIGHT } from "@/config";
import Label from "../Label";
import NavDesktop from "./NavDesktop";
import { routes } from "../../utils/routes";
import Iconify from "../Iconify";
import sunIcon from "@iconify/icons-carbon/sun";
import moonIcon from "@iconify/icons-carbon/moon";
import useSettings from "@/hooks/useSettings";

type Props = {
  transparent?: boolean;
};

export default function Header({ transparent }: Props) {
  const { onToggleMode, themeMode } = useSettings();
  const isDesktop = useResponsive("up", "md");
  const isLight = themeMode === "light";
  const isScrolling = useOffSetTop(HEADER_DESKTOP_HEIGHT);

  return (
    <AppBar sx={{ boxShadow: 0, bgcolor: "transparent" }}>
      <ToolbarStyle
        disableGutters
        transparent={transparent}
        scrolling={isScrolling}
      >
        <Container
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-start",
          }}
        >
          <Box sx={{ lineHeight: 0, position: "relative" }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              <Link component={NextLink} href="/">
                KiwiOptics
              </Link>
            </Typography>

            <Label
              color="info"
              sx={{
                ml: 0.5,
                px: 0.5,
                top: -14,
                left: 64,
                height: 20,
                fontSize: 11,
                cursor: "pointer",
                position: "absolute",
              }}
            >
              v1.0
            </Label>
          </Box>

          {isDesktop && (
            <NavDesktop
              isScrolling={isScrolling}
              isTransparent={transparent}
              navConfig={routes}
            />
          )}

          <Box sx={{ flexGrow: 1 }} />

          <Stack spacing={2} direction="row" alignItems="center">
            <IconButton onClick={onToggleMode}>
              <Iconify
                icon={isLight ? moonIcon : sunIcon}
                sx={{ width: 20, height: 20 }}
              />
            </IconButton>

            <Divider orientation="vertical" sx={{ height: 24 }} />

            {isDesktop && (
              <Stack direction="row" spacing={1}>
                <Button
                  color="inherit"
                  variant="outlined"
                  LinkComponent={NextLink}
                  href="/login"
                  sx={{
                    ...(transparent && {
                      color: "common.white",
                    }),
                    ...(isScrolling && isLight && { color: "text.primary" }),
                  }}
                >
                  Iniciar Sesión
                </Button>

                <Button
                  variant="contained"
                  LinkComponent={NextLink}
                  href="/register"
                >
                  únete a nosotros
                </Button>
              </Stack>
            )}
          </Stack>

          {/* {!isDesktop && (
            <NavMobile
              navConfig={navConfig}
              sx={{
                ml: 1,
                ...(isScrolling && { color: "text.primary" }),
              }}
            />
          )} */}
        </Container>
      </ToolbarStyle>

      {isScrolling && <ToolbarShadowStyle />}
    </AppBar>
  );
}
