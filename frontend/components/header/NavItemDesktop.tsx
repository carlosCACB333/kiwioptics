"use client";
import { styled } from "@mui/material/styles";
import { Link, LinkProps } from "@mui/material";
import { NavItemDesktopProps } from "@/@types/layout";
import NextLink from "next/link";
import { FC } from "react";
import { usePathname } from "next/navigation";

interface RootLinkStyleProps extends LinkProps {
  active?: boolean;
  scrolling?: boolean;
  transparent?: boolean;
}

const RootLinkStyle = styled(Link, {
  shouldForwardProp: (prop) =>
    prop !== "active" &&
    prop !== "scrolling" &&
    prop !== "transparent" &&
    prop !== "open",
})<RootLinkStyleProps>(({ active, scrolling, transparent, theme }) => {
  const dotActiveStyle = {
    "&:before": {
      top: 0,
      width: 6,
      height: 6,
      bottom: 0,
      left: -14,
      content: '""',
      display: "block",
      margin: "auto 0",
      borderRadius: "50%",
      position: "absolute",
      backgroundColor: theme.palette.primary.main,
    },
  };
  return {
    ...theme.typography.subtitle2,
    fontWeight: theme.typography.fontWeightMedium,
    display: "flex",
    color: "inherit",
    position: "relative",
    alignItems: "center",
    transition: theme.transitions.create("opacity", {
      duration: theme.transitions.duration.shortest,
    }),
    "&:hover": {
      opacity: 0.72,
      textDecoration: "none",
    },
    ...(active && {
      ...dotActiveStyle,
      color: theme.palette.text.primary,
      ...(transparent && { color: theme.palette.common.white }),
      ...(scrolling && { color: theme.palette.text.primary }),
    }),
  };
});

export const NavItemDesktop: FC<NavItemDesktopProps> = ({
  item,
  isScrolling,
  isTransparent,
}) => {
  const { title, path } = item;
  const pathname = usePathname();
  const isActive = path === pathname;

  return (
    <RootLinkStyle
      as={NextLink}
      active={isActive}
      scrolling={isScrolling}
      transparent={isTransparent}
      key={title}
      href={path}
    >
      {title}
    </RootLinkStyle>
  );
};
