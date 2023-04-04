"use client";

import { LandingHero } from "@/components/home";
import { Box, Container } from "@mui/material";
export interface TourProps {
  id: number;
  slug: string;
  location: string;
  heroImg: string;
  ratings: number;
  price: number;
  duration: number;
  continent: string;
}
const tours: TourProps[] = [
  {
    id: 1,
    slug: "new-york",
    location: "New York",
    heroImg:
      "https://zone-assets-api.vercel.app/assets/images/travel/travel_1.jpg",
    ratings: 4.5,
    price: 100,
    duration: 5,
    continent: "Europe",
  },
  {
    id: 2,
    slug: "paris",
    location: "Paris",
    heroImg:
      "https://zone-assets-api.vercel.app/assets/images/travel/travel_2.jpg",
    ratings: 4.5,
    price: 100,
    duration: 5,
    continent: "Europe",
  },
  {
    id: 3,
    slug: "london",
    location: "London",
    heroImg:
      "https://zone-assets-api.vercel.app/assets/images/travel/travel_3.jpg",
    ratings: 4.5,
    price: 100,
    duration: 5,
    continent: "Europe",
  },
];
export default function Home() {
  return (
    <main>
      <Box sx={{ position: "relative" }}>
        <LandingHero tours={tours.slice(0, 5)} />

        <Container
          sx={{
            left: 0,
            right: 0,
            bottom: 0,
            mx: "auto",
            position: { md: "absolute" },
          }}
        >
          <h1>kiwioptics</h1>
        </Container>
      </Box>
    </main>
  );
}
