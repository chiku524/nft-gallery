export type SampleMint = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

export const sampleMints: SampleMint[] = [
  {
    id: 1,
    name: "Pugs On The Block #1",
    image: "/gallery/mint-01-stoop-beanie.png",
    attributes: [
      { trait_type: "Background", value: "Brownstone" },
      { trait_type: "Base", value: "Fawn Peek" },
      { trait_type: "Hat", value: "Forest Beanie" },
      { trait_type: "Body", value: "Forest Bandana" },
      { trait_type: "Accessory", value: "None" },
    ],
  },
  {
    id: 2,
    name: "Pugs On The Block #2",
    image: "/gallery/mint-02-neon-crown.png",
    attributes: [
      { trait_type: "Background", value: "Neon Alley" },
      { trait_type: "Base", value: "Black Peek" },
      { trait_type: "Hat", value: "Stoop Crown" },
      { trait_type: "Body", value: "Gold Chain" },
      { trait_type: "Accessory", value: "None" },
    ],
  },
  {
    id: 3,
    name: "Pugs On The Block #3",
    image: "/gallery/mint-03-rooftop-newsie.png",
    attributes: [
      { trait_type: "Background", value: "Golden Rooftop" },
      { trait_type: "Base", value: "Apricot Peek" },
      { trait_type: "Hat", value: "Newsie Cap" },
      { trait_type: "Body", value: "None" },
      { trait_type: "Accessory", value: "Stoop Coffee" },
    ],
  },
  {
    id: 4,
    name: "Pugs On The Block #4",
    image: "/gallery/mint-04-day-hardhat.png",
    attributes: [
      { trait_type: "Background", value: "Sunny Stoop" },
      { trait_type: "Base", value: "Fawn Peek" },
      { trait_type: "Hat", value: "Block Hard Hat" },
      { trait_type: "Body", value: "None" },
      { trait_type: "Accessory", value: "Toy Blocks" },
    ],
  },
  {
    id: 5,
    name: "Pugs On The Block #5",
    image: "/gallery/mint-05-subway-snapback.png",
    attributes: [
      { trait_type: "Background", value: "Subway Platform" },
      { trait_type: "Base", value: "Black Peek" },
      { trait_type: "Hat", value: "Stoop Snapback" },
      { trait_type: "Body", value: "None" },
      { trait_type: "Accessory", value: "Round Shades" },
    ],
  },
  {
    id: 6,
    name: "Pugs On The Block #6",
    image: "/gallery/mint-06-green-monocle.png",
    attributes: [
      { trait_type: "Background", value: "Grid Green" },
      { trait_type: "Base", value: "Apricot Peek" },
      { trait_type: "Hat", value: "Bare head" },
      { trait_type: "Body", value: "Red Collar" },
      { trait_type: "Accessory", value: "Gold Monocle" },
    ],
  },
  {
    id: 7,
    name: "Pugs On The Block #7",
    image: "/gallery/mint-07-cream-hoodie.png",
    attributes: [
      { trait_type: "Background", value: "Cream Paper" },
      { trait_type: "Base", value: "Fawn Peek" },
      { trait_type: "Hat", value: "Bare head" },
      { trait_type: "Body", value: "Cream Hoodie" },
      { trait_type: "Accessory", value: "Chewed Bone" },
    ],
  },
  {
    id: 8,
    name: "Pugs On The Block #8",
    image: "/gallery/mint-08-sunset-bandana.png",
    attributes: [
      { trait_type: "Background", value: "Golden Rooftop" },
      { trait_type: "Base", value: "Black Peek" },
      { trait_type: "Hat", value: "Bare head" },
      { trait_type: "Body", value: "Forest Bandana" },
      { trait_type: "Accessory", value: "Round Shades" },
    ],
  },
];
