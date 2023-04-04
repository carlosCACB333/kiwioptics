import { SxProps } from "@mui/material";

export type NavProps = {
  isScrolling?: boolean | undefined;
  isTransparent?: boolean | undefined;
  navConfig: NavItemProps[];
  sx?: SxProps;
};

export type NavItemChildProps = {
  subheader: string;
  cover?: string;
  items: {
    title: string;
    path: string;
  }[];
};

type NavItemProps = {
  title: string;
  path: string;
};

export type NavItemDesktopProps = {
  item: NavItemProps;
  isScrolling: boolean | undefined;
  isTransparent: boolean | undefined;
};
