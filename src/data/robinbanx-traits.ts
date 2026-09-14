export type RobinBanxTrait = { id: string; name: string; image: string; rarity: number };
export type RobinBanxCategoryId = "safehouse" | "chain_trail" | "alias" | "getup" | "disguise" | "headpiece" | "instrument" | "evidence_mark";
export type RobinBanxTraitCategory = { id: RobinBanxCategoryId; label: string; optional: boolean; traits: RobinBanxTrait[] };
export const ROBINBANX_ART_VERSION = "robinbanx-v1";
export const robinBanxTraitCategories: RobinBanxTraitCategory[] = [
  { id: "safehouse", label: "Safehouse", optional: false, traits: [
    { id: "ledger-room", name: "Ledger Room", image: "/robinbanx-traits/safehouse/ledger-room.png", rarity: 18 },
    { id: "night-vault", name: "Night Vault", image: "/robinbanx-traits/safehouse/night-vault.png", rarity: 16 },
    { id: "rail-archive", name: "Rail Archive", image: "/robinbanx-traits/safehouse/rail-archive.png", rarity: 14 },
    { id: "concrete-cellar", name: "Concrete Cellar", image: "/robinbanx-traits/safehouse/concrete-cellar.png", rarity: 13 },
    { id: "redacted-office", name: "Redacted Office", image: "/robinbanx-traits/safehouse/redacted-office.png", rarity: 12 },
    { id: "signal-attic", name: "Signal Attic", image: "/robinbanx-traits/safehouse/signal-attic.png", rarity: 10 },
    { id: "canal-depot", name: "Canal Depot", image: "/robinbanx-traits/safehouse/canal-depot.png", rarity: 8 },
    { id: "embassy-basement", name: "Embassy Basement", image: "/robinbanx-traits/safehouse/embassy-basement.png", rarity: 5 },
    { id: "offshore-bunker", name: "Offshore Bunker", image: "/robinbanx-traits/safehouse/offshore-bunker.png", rarity: 3 },
    { id: "black-site", name: "Black Site", image: "/robinbanx-traits/safehouse/black-site.png", rarity: 1 },
  ] },
  { id: "chain_trail", label: "Chain Trail", optional: true, traits: [
    { id: "none", name: "No Trail", image: "/robinbanx-traits/chain-trail/none.png", rarity: 28 },
    { id: "base-blueprint", name: "Base Blueprint", image: "/robinbanx-traits/chain-trail/base-blueprint.png", rarity: 18 },
    { id: "ethereum-rubric", name: "Ethereum Rubric", image: "/robinbanx-traits/chain-trail/ethereum-rubric.png", rarity: 14 },
    { id: "bitcoin-ransom", name: "Bitcoin Ransom", image: "/robinbanx-traits/chain-trail/bitcoin-ransom.png", rarity: 12 },
    { id: "solana-transit", name: "Solana Transit", image: "/robinbanx-traits/chain-trail/solana-transit.png", rarity: 9 },
    { id: "arbitrum-route", name: "Arbitrum Route", image: "/robinbanx-traits/chain-trail/arbitrum-route.png", rarity: 7 },
    { id: "optimism-signal", name: "Optimism Signal", image: "/robinbanx-traits/chain-trail/optimism-signal.png", rarity: 5 },
    { id: "polygon-grid", name: "Polygon Grid", image: "/robinbanx-traits/chain-trail/polygon-grid.png", rarity: 4 },
    { id: "zora-negative", name: "Zora Negative", image: "/robinbanx-traits/chain-trail/zora-negative.png", rarity: 2 },
    { id: "multichain-crossing", name: "Multichain Crossing", image: "/robinbanx-traits/chain-trail/multichain-crossing.png", rarity: 1 },
  ] },
  { id: "alias", label: "Alias", optional: false, traits: [
    { id: "rook", name: "Rook", image: "/robinbanx-traits/alias/rook.png", rarity: 16 },
    { id: "vesper", name: "Vesper", image: "/robinbanx-traits/alias/vesper.png", rarity: 15 },
    { id: "cutlass", name: "Cutlass", image: "/robinbanx-traits/alias/cutlass.png", rarity: 14 },
    { id: "cipher", name: "Cipher", image: "/robinbanx-traits/alias/cipher.png", rarity: 13 },
    { id: "morrow", name: "Morrow", image: "/robinbanx-traits/alias/morrow.png", rarity: 12 },
    { id: "switch", name: "Switch", image: "/robinbanx-traits/alias/switch.png", rarity: 10 },
    { id: "locke", name: "Locke", image: "/robinbanx-traits/alias/locke.png", rarity: 8 },
    { id: "parallax", name: "Parallax", image: "/robinbanx-traits/alias/parallax.png", rarity: 6 },
    { id: "zero-day", name: "Zero Day", image: "/robinbanx-traits/alias/zero-day.png", rarity: 4 },
    { id: "ghost-key", name: "Ghost Key", image: "/robinbanx-traits/alias/ghost-key.png", rarity: 2 },
  ] },
  { id: "getup", label: "Getup", optional: false, traits: [
    { id: "pinstripe-rig", name: "Pinstripe Rig", image: "/robinbanx-traits/getup/pinstripe-rig.png", rarity: 17 },
    { id: "courier-coat", name: "Courier Coat", image: "/robinbanx-traits/getup/courier-coat.png", rarity: 16 },
    { id: "night-vest", name: "Night Vest", image: "/robinbanx-traits/getup/night-vest.png", rarity: 14 },
    { id: "heist-knit", name: "Heist Knit", image: "/robinbanx-traits/getup/heist-knit.png", rarity: 13 },
    { id: "archive-suit", name: "Archive Suit", image: "/robinbanx-traits/getup/archive-suit.png", rarity: 12 },
    { id: "armored-shirt", name: "Armored Shirt", image: "/robinbanx-traits/getup/armored-shirt.png", rarity: 10 },
    { id: "signal-parka", name: "Signal Parka", image: "/robinbanx-traits/getup/signal-parka.png", rarity: 8 },
    { id: "embassy-tux", name: "Embassy Tux", image: "/robinbanx-traits/getup/embassy-tux.png", rarity: 5 },
    { id: "hazmat-tailoring", name: "Hazmat Tailoring", image: "/robinbanx-traits/getup/hazmat-tailoring.png", rarity: 3 },
    { id: "carbon-mail", name: "Carbon Mail", image: "/robinbanx-traits/getup/carbon-mail.png", rarity: 2 },
  ] },
  { id: "disguise", label: "Disguise", optional: true, traits: [
    { id: "none", name: "Unmasked", image: "/robinbanx-traits/disguise/none.png", rarity: 24 },
    { id: "bandit-cloth", name: "Bandit Cloth", image: "/robinbanx-traits/disguise/bandit-cloth.png", rarity: 18 },
    { id: "ledger-blind", name: "Ledger Blind", image: "/robinbanx-traits/disguise/ledger-blind.png", rarity: 14 },
    { id: "mirror-specs", name: "Mirror Specs", image: "/robinbanx-traits/disguise/mirror-specs.png", rarity: 13 },
    { id: "half-respirator", name: "Half Respirator", image: "/robinbanx-traits/disguise/half-respirator.png", rarity: 10 },
    { id: "paper-visage", name: "Paper Visage", image: "/robinbanx-traits/disguise/paper-visage.png", rarity: 8 },
    { id: "cipher-goggles", name: "Cipher Goggles", image: "/robinbanx-traits/disguise/cipher-goggles.png", rarity: 6 },
    { id: "full-respirator", name: "Full Respirator", image: "/robinbanx-traits/disguise/full-respirator.png", rarity: 4 },
    { id: "holo-scrambler", name: "Holo Scrambler", image: "/robinbanx-traits/disguise/holo-scrambler.png", rarity: 2 },
    { id: "blank-plate", name: "Blank Plate", image: "/robinbanx-traits/disguise/blank-plate.png", rarity: 1 },
  ] },
  { id: "headpiece", label: "Headpiece", optional: true, traits: [
    { id: "none", name: "Bareheaded", image: "/robinbanx-traits/headpiece/none.png", rarity: 30 },
    { id: "watch-cap", name: "Watch Cap", image: "/robinbanx-traits/headpiece/watch-cap.png", rarity: 18 },
    { id: "creased-fedora", name: "Creased Fedora", image: "/robinbanx-traits/headpiece/creased-fedora.png", rarity: 14 },
    { id: "courier-hood", name: "Courier Hood", image: "/robinbanx-traits/headpiece/courier-hood.png", rarity: 12 },
    { id: "radio-phones", name: "Radio Phones", image: "/robinbanx-traits/headpiece/radio-phones.png", rarity: 10 },
    { id: "night-beret", name: "Night Beret", image: "/robinbanx-traits/headpiece/night-beret.png", rarity: 7 },
    { id: "breach-helmet", name: "Breach Helmet", image: "/robinbanx-traits/headpiece/breach-helmet.png", rarity: 4 },
    { id: "crown-of-keys", name: "Crown of Keys", image: "/robinbanx-traits/headpiece/crown-of-keys.png", rarity: 2 },
    { id: "validator-halo", name: "Validator Halo", image: "/robinbanx-traits/headpiece/validator-halo.png", rarity: 2 },
    { id: "burner-aureole", name: "Burner Aureole", image: "/robinbanx-traits/headpiece/burner-aureole.png", rarity: 1 },
  ] },
  { id: "instrument", label: "Instrument", optional: true, traits: [
    { id: "none", name: "Empty Hands", image: "/robinbanx-traits/instrument/none.png", rarity: 22 },
    { id: "bolt-cutters", name: "Bolt Cutters", image: "/robinbanx-traits/instrument/bolt-cutters.png", rarity: 17 },
    { id: "burner-phone", name: "Burner Phone", image: "/robinbanx-traits/instrument/burner-phone.png", rarity: 15 },
    { id: "cold-wallet", name: "Cold Wallet", image: "/robinbanx-traits/instrument/cold-wallet.png", rarity: 13 },
    { id: "glass-key", name: "Glass Key", image: "/robinbanx-traits/instrument/glass-key.png", rarity: 10 },
    { id: "signal-jammer", name: "Signal Jammer", image: "/robinbanx-traits/instrument/signal-jammer.png", rarity: 8 },
    { id: "bridge-case", name: "Bridge Case", image: "/robinbanx-traits/instrument/bridge-case.png", rarity: 6 },
    { id: "validator-drill", name: "Validator Drill", image: "/robinbanx-traits/instrument/validator-drill.png", rarity: 4 },
    { id: "genesis-charge", name: "Genesis Charge", image: "/robinbanx-traits/instrument/genesis-charge.png", rarity: 3 },
    { id: "sequencer-override", name: "Sequencer Override", image: "/robinbanx-traits/instrument/sequencer-override.png", rarity: 2 },
  ] },
  { id: "evidence_mark", label: "Evidence Mark", optional: true, traits: [
    { id: "none", name: "Clean File", image: "/robinbanx-traits/evidence-mark/none.png", rarity: 26 },
    { id: "case-open", name: "Case Open", image: "/robinbanx-traits/evidence-mark/case-open.png", rarity: 18 },
    { id: "seized", name: "Seized", image: "/robinbanx-traits/evidence-mark/seized.png", rarity: 14 },
    { id: "classified", name: "Classified", image: "/robinbanx-traits/evidence-mark/classified.png", rarity: 12 },
    { id: "redacted", name: "Redacted", image: "/robinbanx-traits/evidence-mark/redacted.png", rarity: 10 },
    { id: "base-8453", name: "Base 8453", image: "/robinbanx-traits/evidence-mark/base-8453.png", rarity: 8 },
    { id: "wanted", name: "Wanted", image: "/robinbanx-traits/evidence-mark/wanted.png", rarity: 6 },
    { id: "chain-of-custody", name: "Chain of Custody", image: "/robinbanx-traits/evidence-mark/chain-of-custody.png", rarity: 3 },
    { id: "inside-job", name: "Inside Job", image: "/robinbanx-traits/evidence-mark/inside-job.png", rarity: 2 },
    { id: "case-000", name: "Case 000", image: "/robinbanx-traits/evidence-mark/case-000.png", rarity: 1 },
  ] },
];
export type RobinBanxSelection = Record<RobinBanxCategoryId, string>;
export const defaultRobinBanxSelection: RobinBanxSelection = {"safehouse": "ledger-room", "chain_trail": "base-blueprint", "alias": "rook", "getup": "pinstripe-rig", "disguise": "bandit-cloth", "headpiece": "creased-fedora", "instrument": "bolt-cutters", "evidence_mark": "case-open"};
export const robinBanxIncompatiblePairs = [{"left": {"category": "disguise", "trait": "full-respirator"}, "right": {"category": "headpiece", "trait": "courier-hood"}}, {"left": {"category": "disguise", "trait": "blank-plate"}, "right": {"category": "headpiece", "trait": "radio-phones"}}, {"left": {"category": "disguise", "trait": "holo-scrambler"}, "right": {"category": "headpiece", "trait": "breach-helmet"}}, {"left": {"category": "getup", "trait": "hazmat-tailoring"}, "right": {"category": "disguise", "trait": "bandit-cloth"}}, {"left": {"category": "getup", "trait": "carbon-mail"}, "right": {"category": "instrument", "trait": "bolt-cutters"}}, {"left": {"category": "headpiece", "trait": "crown-of-keys"}, "right": {"category": "instrument", "trait": "validator-drill"}}, {"left": {"category": "chain_trail", "trait": "bitcoin-ransom"}, "right": {"category": "instrument", "trait": "sequencer-override"}}] as const;
export function isRobinBanxSelectionCompatible(selection: RobinBanxSelection) {
  return !robinBanxIncompatiblePairs.some(({ left, right }) =>
    selection[left.category] === left.trait && selection[right.category] === right.trait,
  );
}
export function robinBanxTraitSrc(path: string) { return `${path}?v=${ROBINBANX_ART_VERSION}`; }
export function robinBanxSelectionToLayers(selection: RobinBanxSelection) {
  return robinBanxTraitCategories.map((category) => category.traits.find((trait) => trait.id === selection[category.id]))
    .filter((trait): trait is RobinBanxTrait => Boolean(trait)).map((trait) => robinBanxTraitSrc(trait.image));
}
