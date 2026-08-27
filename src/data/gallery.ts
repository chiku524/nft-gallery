export type SampleMint = {
  id: number;
  name: string;
  image: string;
  attributes: { trait_type: string; value: string }[];
};

function mint(
  id: number,
  background: string,
  base: string,
  block: string,
  hat: string,
  body: string,
  accessory: string,
): SampleMint {
  return {
    id,
    name: `Pugs On The Block #${id}`,
    image: `/generated-preview/${id}.jpg`,
    attributes: [
      { trait_type: "Background", value: background },
      { trait_type: "Base", value: base },
      { trait_type: "Block", value: block },
      { trait_type: "Hat", value: hat },
      { trait_type: "Body", value: body },
      { trait_type: "Accessory", value: accessory },
    ],
  };
}

export const sampleMints: SampleMint[] = [
  mint(1, "Sunny Stoop", "Apricot Peek", "Cinder Block", "Stoop Snapback", "No clothes", "Empty paws"),
  mint(2, "Brownstone", "Apricot Peek", "Brownstone Ledge", "Forest Beanie", "Gold Chain", "Stoop Coffee"),
  mint(3, "Sunny Stoop", "Fawn Peek", "Crate Stack", "Bare head", "Red Collar", "Chewed Bone"),
  mint(4, "Brownstone", "Fawn Peek", "Cinder Block", "Newsie Cap", "Gold Chain", "Empty paws"),
  mint(5, "Dusk Court", "Apricot Peek", "Cinder Block", "Forest Beanie", "No clothes", "Empty paws"),
  mint(6, "Brownstone", "Fawn Peek", "Cinder Block", "Stoop Snapback", "Cream Hoodie", "Toy Blocks"),
  mint(7, "Brownstone", "Fawn Peek", "Default concrete", "Stoop Snapback", "No clothes", "Gold Monocle"),
  mint(8, "Brownstone", "Fawn Peek", "Cinder Block", "Stoop Snapback", "Forest Bandana", "Stoop Coffee"),
];
