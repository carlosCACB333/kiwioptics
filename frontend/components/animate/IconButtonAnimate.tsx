import { m } from "framer-motion";
import { forwardRef, ReactNode } from "react";
import { Box, IconButton, IconButtonProps, SxProps } from "@mui/material";

interface Props extends IconButtonProps {
  sxWrap?: SxProps;
}

type AnimateWrapProp = {
  children: ReactNode;
  size: "small" | "medium" | "large";
  sxWrap?: SxProps;
};

const varSmall = {
  hover: { scale: 1.1 },
  tap: { scale: 0.95 },
};

const varMedium = {
  hover: { scale: 1.09 },
  tap: { scale: 0.97 },
};

const varLarge = {
  hover: { scale: 1.08 },
  tap: { scale: 0.99 },
};

function AnimateWrap({ size, children, sxWrap }: AnimateWrapProp) {
  const isSmall = size === "small";
  const isLarge = size === "large";

  return (
    <Box
      component={m.div}
      whileTap="tap"
      whileHover="hover"
      variants={(isSmall && varSmall) || (isLarge && varLarge) || varMedium}
      sx={{
        display: "inline-flex",
        ...sxWrap,
      }}
    >
      {children}
    </Box>
  );
}

export const IconButtonAnimate = forwardRef<HTMLButtonElement, Props>(
  (props, ref) => {
    const { children, size = "medium", sxWrap, ...other } = props;

    return (
      <AnimateWrap size={size} sxWrap={sxWrap}>
        <IconButton size={size} ref={ref} {...other}>
          {children}
        </IconButton>
      </AnimateWrap>
    );
  }
);

IconButtonAnimate.displayName = "IconButtonAnimate";
