// ----------------------------------------------------------------------

export default function Link() {
  return {
    MuiLink: {
      defaultProps: {
        underline: "hover",
      },

      styleOverrides: {
        root: {
          cursor: "pointer",
          default: {
            color: "inherit",
          },
        },
      },
    },
  };
}
