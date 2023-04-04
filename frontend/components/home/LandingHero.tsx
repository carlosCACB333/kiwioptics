"use client";

import { useRef, useState } from "react";
import locationIcon from "@iconify/icons-carbon/location";
import timeIcon from "@iconify/icons-carbon/time";
import starIcon from "@iconify/icons-carbon/star";
import currencyIcon from "@iconify/icons-carbon/currency";
import { alpha, useTheme } from "@mui/material/styles";
import { Stack, Typography, Button, Avatar, Box } from "@mui/material";
import TextIconLabel from "../TextIconLabel";
import Iconify from "../Iconify";
import BgOverlay from "../BgOverlay";
import Image from "../Image";
import { TextMaxLine } from "../TextMaxLine";
import cssStyles from "@/utils/cssStyles";
import { Swiper, SwiperRef, SwiperSlide } from "swiper/react";
import { Autoplay, Navigation, Pagination, Scrollbar } from "swiper";
import { TourProps } from "@/app/page";
import "swiper/swiper.css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/scrollbar";
type Props = {
  tours: TourProps[];
};

export const LandingHero = ({ tours }: Props) => {
  const theme = useTheme();
  const slider = useRef<SwiperRef>(null);
  const [selected, setSelected] = useState(0);

  const handleChange = (index: number) => {
    slider.current?.swiper.slideTo(index);
  };

  return (
    <Box sx={{ minHeight: "100vh", position: "relative", maxWidth: "100%" }}>
      <Swiper
        ref={slider}
        spaceBetween={0}
        centeredSlides={true}
        loop
        autoplay={{
          delay: 5000,
          disableOnInteraction: false,
        }}
        modules={[Autoplay]}
        onSlideChange={(swiper) => {
          console.log(swiper.activeIndex);

          setSelected(swiper.activeIndex);
        }}
        onSwiper={(swiper) => {
          console.log(swiper.activeIndex);

          setSelected(swiper.activeIndex);
        }}
      >
        {tours.map((tour, index) => (
          <SwiperSlide key={tour.id}>
            <ContentItem key={tour.id} tour={tour} />
          </SwiperSlide>
        ))}
      </Swiper>

      <Stack
        spacing={2}
        justifyContent="center"
        sx={{
          top: 0,
          height: 1,
          maxWidth: 220,
          position: "absolute",
          display: { xs: "none", md: "flex" },
          right: { xs: 20, lg: "6%", xl: "10%" },
          zIndex: 9,
        }}
      >
        {!!tours.length && (
          <>
            {tours.map((tour, index) => (
              <Box key={tour.id} onClick={() => handleChange(index)}>
                <ThumbnailItem tour={tour} isSelected={selected === index} />
              </Box>
            ))}
          </>
        )}
      </Stack>
    </Box>
  );
};

// ----------------------------------------------------------------------

type ItemProps = {
  tour: TourProps;
  isSelected?: boolean;
};

function ContentItem({ tour }: ItemProps) {
  const theme = useTheme();
  const { slug, location, heroImg, ratings, price, duration } = tour;

  return (
    <Box
      sx={{
        display: "flex",
        textAlign: "center",
        alignItems: "center",
        position: "relative",
        color: "common.white",
        justifyContent: "center",
      }}
    >
      {/* Content */}
      <Stack
        alignItems="center"
        sx={{
          zIndex: 9,
          py: { xs: 20, md: 0 },
          position: { md: "absolute" },
        }}
      >
        <Typography variant="overline" sx={{ color: "secondary.main", mb: 5 }}>
          {location}
        </Typography>

        <Typography variant="h1" sx={{ maxWidth: 480 }}>
          {slug}
        </Typography>

        <Stack
          alignItems="center"
          spacing={{ xs: 2.5, md: 5 }}
          direction={{ xs: "column", md: "row" }}
          sx={{
            my: 5,
            "& svg": {
              mr: 1,
              width: 24,
              height: 24,
              color: "primary.main",
            },
          }}
        >
          <TextIconLabel
            icon={<Iconify icon={timeIcon} />}
            value={duration}
            sx={{ typography: "subtitle2" }}
          />

          <TextIconLabel
            icon={<Iconify icon={starIcon} />}
            value={`${ratings} reviews`}
            sx={{ typography: "subtitle2" }}
          />

          <TextIconLabel
            icon={<Iconify icon={currencyIcon} />}
            value={`Starting at ${price}`}
            sx={{ typography: "subtitle2" }}
          />
        </Stack>

        <Button variant="contained" size="large">
          Book Now
        </Button>
      </Stack>

      {/* Background */}
      <Box
        sx={{
          width: 1,
          height: 1,
          position: {
            xs: "absolute",
            md: "relative",
          },
        }}
      >
        <BgOverlay
          startColor={alpha(theme.palette.grey[900], 0.48)}
          endColor={alpha(theme.palette.grey[900], 0.48)}
        />
        <BgOverlay />
        <Image
          alt="hero"
          src={heroImg}
          sx={{
            height: { xs: 1, md: "100vh" },
          }}
        />
      </Box>
    </Box>
  );
}

// ----------------------------------------------------------------------

function ThumbnailItem({ tour, isSelected }: ItemProps) {
  const theme = useTheme();
  const { continent, heroImg, location } = tour;

  return (
    <Stack
      direction="row"
      alignItems="center"
      spacing={2.5}
      sx={{
        px: 2,
        py: 1.5,
        cursor: "pointer",
        color: "common.white",
        ...(isSelected && {
          borderRadius: 2,
          ...cssStyles().bgBlur({
            blur: 8,
            opacity: 0.08,
            color: theme.palette.common.white,
          }),
        }),
      }}
    >
      <Avatar src={heroImg} sx={{ width: 48, height: 48 }} />
      <Stack spacing={0.5}>
        <TextMaxLine variant="h6" line={1}>
          {location}
        </TextMaxLine>
        <TextIconLabel
          icon={
            <Iconify
              icon={locationIcon}
              sx={{ width: 20, height: 20, mr: 1, color: "primary.main" }}
            />
          }
          value={
            <TextMaxLine variant="caption" line={1} sx={{ opacity: 0.48 }}>
              {continent}
            </TextMaxLine>
          }
        />
      </Stack>
    </Stack>
  );
}
