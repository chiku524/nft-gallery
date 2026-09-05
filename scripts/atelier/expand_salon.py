"""Emit works 51-500. Each file is a self-contained painter.

Thirty drawing families are interleaved so neighbors never share a geometry.
Fifteen layouts per family change count, scale, crop, and motion — not just color.
Media names are unique and do not reuse the first fifty.
"""

from __future__ import annotations

import random
from pathlib import Path
from textwrap import dedent

WORKS_DIR = Path(__file__).resolve().parent / "works"

# Family index = (id - 51) % 30. Layout = (id - 51) // 30.
# Fifteen unique names per family (layout 0..14).

FAMILIES: list[list[tuple[str, str, str, str, str, str]]] = [
    [  # 0 seismograph
        ("jolt-trace", "Jolt Trace", "Seismograph ink", "Tick", "Graphite cream", "A needle that writes the floor and will not lift."),
        ("fault-line", "Fault Line", "Drum recorder", "Slip", "Ink bone", "The paper keeps a secret the bedrock already spent."),
        ("ward-strip", "Ward Strip", "EKG paper", "Beat", "Clinical red", "A heart with no body. The grid is the only furniture."),
        ("aftershock", "Aftershock", "Smoked drum", "Jolt", "Char lamp", "The second wave is smaller and somehow louder."),
        ("quiet-line", "Quiet Line", "Baseline ink", "Hold", "Pale graphite", "Almost nothing happens. That is the drawing."),
        ("needle-graph", "Needle Graph", "Galvanometer", "Sweep", "Brass pale", "A coil arguing with a strip of paper."),
        ("tremor-roll", "Tremor Roll", "Portable seismograph", "Roll", "Field khaki", "Packed for a ridge. Unpacked as a loop."),
        ("scope-needle", "Scope Needle", "Medical scope", "Scan", "Green ward", "Not a radar. A pulse that forgot the patient."),
        ("drift-graph", "Drift Graph", "Tiltmeter", "Lean", "Clay slip", "The room is moving. The ink admits it."),
        ("shock-ribbon", "Shock Ribbon", "Ribbon galvanometer", "Flick", "Violet paper", "Light, not ink — but the paper still takes a scar."),
        ("bedrock-tick", "Bedrock Tick", "Geophone paper", "Tick", "Ochre dust", "Listening downward until the line flinches."),
        ("epicenter", "Epicenter", "Iso-seismal", "Bloom", "Map rose", "Rings that mean trouble, drawn as if they were weather."),
        ("spikes", "Spikes", "Spike train", "Fire", "Night phosphor", "A neuron with nowhere to live except this strip."),
        ("amp-trace", "Amp Trace", "Oscillograph", "Drive", "Amber bakelite", "Voltage pretending it has a landscape."),
        ("postage-jolt", "Postage Jolt", "Stamp seismograph", "Crop", "Carmine pulp", "The quake, reduced to a denomination."),
    ],
    [  # 1 hex
        ("wax-comb", "Wax Comb", "Beeswax comb", "Fill", "Honey black", "A hive plan with no bees left to argue."),
        ("bolt-head", "Bolt Head", "Hex bolt", "Turn", "Shop steel", "Hardware enlarged until it becomes a room."),
        ("tile-hex", "Tile Hex", "Hex tile", "Shift", "Lobby clay", "A floor that refuses a square."),
        ("graphite-net", "Graphite Net", "Graphene sketch", "Drift", "Pencil silver", "Six-sided and almost not there."),
        ("game-hex", "Game Hex", "Wargame hex", "Advance", "Olive map", "A campaign with no pieces, only the board breathing."),
        ("nut-plate", "Nut Plate", "Hex nut", "Seat", "Cadmium shop", "Threaded air."),
        ("comb-void", "Comb Void", "Empty comb", "Drain", "Wax night", "The cells are open. The honey already left."),
        ("paving-hex", "Paving Hex", "Hex paver", "Settle", "Garden slate", "Outdoor geometry brought indoors without permission."),
        ("mesh-hex", "Mesh Hex", "Hex mesh", "Tension", "Fence zinc", "A net that wants to be jewelry."),
        ("cell-map", "Cell Map", "Cellular map", "Index", "Planner blue", "Addresses for a city that is only corners."),
        ("amber-comb", "Amber Comb", "Amber section", "Glow", "Resin lamp", "A fossil of work."),
        ("snow-hex", "Snow Hex", "Snowflake plate", "Melt", "Ice paper", "Six arms, one decision."),
        ("oil-cell", "Oil Cell", "Oilstone cell", "Well", "Slick umber", "A reservoir drawn as if it were polite."),
        ("capsule-hex", "Capsule Hex", "Capsule tile", "Dock", "Clinic white", "Medicine as architecture."),
        ("tiny-comb", "Tiny Comb", "Microcomb", "Pulse", "Nectar dusk", "Too small to harvest, still a field."),
    ],
    [  # 2 fishscale
        ("armor-scale", "Armor Scale", "Lamellar", "Lift", "Bronze dusk", "A soldier reduced to the idea of overlapping."),
        ("roof-scale", "Roof Scale", "Fish-scale shingle", "Shed", "Tar silver", "Weather on a wall that never saw rain."),
        ("koi-mail", "Koi Mail", "Koi scale", "Swim", "Vermilion pond", "A fish that is only its weather."),
        ("pine-cone", "Pine Cone", "Cone scale", "Open", "Forest rust", "The tree’s argument, stacked."),
        ("paillette", "Paillette", "Paillette", "Flicker", "Show gold", "Costume armor for a room."),
        ("scallop-tile", "Scallop Tile", "Scallop tile", "Lap", "Bath cream", "A wall learning to be a shore."),
        ("dragon-scale", "Dragon Scale", "Dragon scale", "Heave", "Temple green", "Myth as a repeat."),
        ("asphalt-scale", "Asphalt Scale", "Mineral paper", "Grit", "Roof black", "Cheap and glittering."),
        ("nacre-row", "Nacre Row", "Nacre", "Iridesce", "Pearl dusk", "Mother-of-pearl without the animal."),
        ("clinker", "Clinker", "Clinker row", "Overlap", "Boat tar", "A hull that forgot the water."),
        ("scale-fan", "Scale Fan", "Scale fan", "Open", "Opera red", "One gesture, many lids."),
        ("zinc-scale", "Zinc Scale", "Zinc shingle", "Weather", "Industrial pale", "A shed elevated to a painting."),
        ("scale-void", "Scale Void", "Missing scale", "Gap", "Ink gap", "The hole is the subject."),
        ("gilt-scale", "Gilt Scale", "Gilt scale", "Burnish", "Icon gold", "A relic that repeats itself."),
        ("postage-scale", "Postage Scale", "Scale stamp", "Crop", "Issue blue", "Armor, perforated."),
    ],
    [  # 3 parquet
        ("oak-chevron", "Oak Chevron", "Chevron parquet", "March", "Floor honey", "A hallway with nowhere to walk."),
        ("end-grain", "End Grain", "End-grain block", "Seat", "Butcher warm", "The tree seen the hard way."),
        ("versailles", "Versailles", "Versailles parquet", "Turn", "Palace oak", "A room quoting another room."),
        ("herring-floor", "Herring Floor", "Herringbone oak", "Walk", "Walnut cream", "Not a tweed. A floor that points."),
        ("basket-oak", "Basket Oak", "Basket parquet", "Weave", "Blond oak", "Squares pretending they are cloth."),
        ("ship-deck", "Ship Deck", "Teak deck", "Caulk", "Marine teak", "A boat that will not leave the salon."),
        ("inlay-band", "Inlay Band", "Marquetry band", "Trace", "Satinwood", "A border that thinks it is a river."),
        ("ebony-run", "Ebony Run", "Ebony run", "Slide", "Piano black", "Dark wood, one direction."),
        ("cork-plank", "Cork Plank", "Cork plank", "Give", "Tan give", "A floor that remembers feet. No pins."),
        ("ash-ladder", "Ash Ladder", "Ash strip", "Rise", "Pale ash", "Rungs without a climb."),
        ("parquet-star", "Parquet Star", "Star parquet", "Align", "Medallion oak", "The center of a room that is only center."),
        ("worn-path", "Worn Path", "Worn parquet", "Fade", "Traffic oak", "The walk is the drawing."),
        ("green-oak", "Green Oak", "Green oak", "Cure", "Raw sap", "Unseasoned and already a pattern."),
        ("tiny-blocks", "Tiny Blocks", "Mosaique", "Scatter", "Toy wood", "A floor for a smaller building."),
        ("corner-chevron", "Corner Chevron", "Chevron crop", "Crop", "Amber varnish", "Only the turn survives."),
    ],
    [  # 4 tartan
        ("clan-sett", "Clan Sett", "Tartan sett", "Lock", "Wool night", "A family reduced to crossings."),
        ("windowpane", "Windowpane", "Windowpane check", "Frame", "Suit grey", "A window that is only thread."),
        ("madras-cross", "Madras Cross", "Madras", "Bleed", "Monsoon dye", "The crossings ran in the rain on purpose."),
        ("black-watch", "Black Watch", "Black Watch", "Hold", "Night green", "Military cloth without the regiment."),
        ("gingham-field", "Gingham Field", "Gingham", "Picnic", "Picnic red", "A tablecloth promoted."),
        ("pinstripe-run", "Pinstripe Run", "Pinstripe", "Stride", "Bank navy", "A suit that forgot the body."),
        ("glen-check", "Glen Check", "Glen plaid", "Step", "Fog wool", "Hills turned into a repeat."),
        ("shepherd", "Shepherd", "Shepherd check", "Fold", "Flock black", "A blanket for weather that never arrives."),
        ("district-check", "District Check", "District check", "Bound", "Estate rust", "Land drawn as crossings."),
        ("overcheck", "Overcheck", "Overcheck", "Layer", "Scarlet grid", "A grid on a grid, still not a cage."),
        ("silk-plaid", "Silk Plaid", "Silk plaid", "Sheen", "Opera plaid", "Light doing the weaving."),
        ("faded-sett", "Faded Sett", "Sun-faded tartan", "Bleach", "Washed clan", "The family got tired."),
        ("mini-check", "Mini Check", "Mini check", "Tick", "Shirt pale", "Too small for a clan, still a law."),
        ("bias-plaid", "Bias Plaid", "Bias tartan", "Tilt", "Cut wool", "The sett, turned until it is a new country."),
        ("selvedge", "Selvedge", "Selvedge plaid", "Stop", "Mill cream", "The edge is the only honest part."),
    ],
    [  # 5 shibori
        ("kanoko", "Kanoko", "Kanoko shibori", "Bind", "Indigo rice", "Dots that were once pinched cloth."),
        ("arashi-pole", "Arashi Pole", "Arashi shibori", "Twist", "Storm indigo", "Cloth pole-wrapped into weather."),
        ("itajime", "Itajime", "Itajime", "Clamp", "Board indigo", "A fold remembered by dye."),
        ("kumo-web", "Kumo Web", "Kumo shibori", "Pull", "Spider indigo", "Tied into a sky."),
        ("miura", "Miura", "Miura shibori", "Loop", "Bound blue", "Loops that never become rope."),
        ("nui-resist", "Nui Resist", "Nui shibori", "Stitch", "Sewn indigo", "The stitch is gone. The absence stayed."),
        ("dip-line", "Dip Line", "Dip dye", "Lift", "Horizon indigo", "A tide on cloth."),
        ("ne-maki", "Ne Maki", "Ne-maki", "Wind", "Root indigo", "Wound from the root out."),
        ("tesuji", "Tesuji", "Tesuji", "Pleat", "Hand indigo", "Pleats that dye like a riverbed."),
        ("boshi", "Boshi", "Boshi shibori", "Cap", "Capped white", "A resist that behaves like a hat."),
        ("indigo-void", "Indigo Void", "Vat void", "Sink", "Deep vat", "The cloth went in and almost did not return."),
        ("rice-dot", "Rice Dot", "Rice resist", "Speck", "Grain blue", "Food used as a dam."),
        ("pole-crop", "Pole Crop", "Arashi crop", "Crop", "Pole rust", "Weather, framed."),
        ("pale-shibori", "Pale Shibori", "Once-dipped", "Fade", "Sky cloth", "One dip. A rumor of blue."),
        ("night-bind", "Night Bind", "Night shibori", "Bind", "Ink vat", "Tied in the dark on purpose."),
    ],
    [  # 6 terrazzo
        ("lobby-chip", "Lobby Chip", "Terrazzo chip", "Settle", "Lobby mint", "A floor pouring itself into a wall."),
        ("venetian-chip", "Venetian Chip", "Venetian terrazzo", "Gleam", "Palace chip", "Marble, reduced to confetti and then promoted."),
        ("brass-divider", "Brass Divider", "Terrazzo strip", "Bound", "Brass mint", "The divider is the drawing."),
        ("pink-agg", "Pink Agg", "Pink aggregate", "Scatter", "Salon pink", "Candy that pretends it is stone."),
        ("noir-chip", "Noir Chip", "Black terrazzo", "Glint", "Noir speck", "A night floor."),
        ("coarse-pour", "Coarse Pour", "Coarse terrazzo", "Heavy", "Brutal chip", "The chips refused to be polite."),
        ("fine-sand", "Fine Sand", "Fine terrazzo", "Dust", "Pale grit", "Almost a color field. Then a stone speaks."),
        ("glass-agg", "Glass Agg", "Glass terrazzo", "Spark", "Bottle green", "A beach that used to be windows."),
        ("hospital-chip", "Hospital Chip", "Clinic terrazzo", "Clean", "Clinic green", "Hygiene as a pattern."),
        ("broken-plate", "Broken Plate", "Plate terrazzo", "Shard", "China blue", "Dinner, recycled into a ground."),
        ("gold-chip", "Gold Chip", "Gilt terrazzo", "Flash", "Gilt lobby", "Ostentation, ground flat."),
        ("tiny-agg", "Tiny Agg", "Micro terrazzo", "Speck", "Dust marble", "A floor for a dollhouse atrium."),
        ("corner-pour", "Corner Pour", "Terrazzo crop", "Crop", "Edge chip", "Only the accident remains."),
        ("wet-grind", "Wet Grind", "Ground terrazzo", "Polish", "Wet stone", "The grinder is still in the room."),
        ("void-chip", "Void Chip", "Missing chip", "Gap", "Hole mint", "The stone that left."),
    ],
    [  # 7 diamond plate
        ("tread-plate", "Tread Plate", "Diamond plate", "Grip", "Shop aluminum", "A floor that warns the foot."),
        ("checker-steel", "Checker Steel", "Checker plate", "Stamp", "Mill grey", "Raised, repeating, unfriendly."),
        ("dock-plate", "Dock Plate", "Dock plate", "Load", "Harbor steel", "Cargo without the ship."),
        ("ramp-grip", "Ramp Grip", "Ramp tread", "Climb", "Safety silver", "An incline that stayed flat."),
        ("tread-gold", "Tread Gold", "Gilt tread", "Flash", "Show plate", "Utility dressed for a lobby."),
        ("worn-tread", "Worn Tread", "Worn plate", "Polish", "Traffic steel", "The diamonds are tired."),
        ("black-plate", "Black Plate", "Black tread", "Absorb", "Night steel", "A warning that learned to whisper."),
        ("micro-tread", "Micro Tread", "Bead plate", "Grit", "Bead silver", "Grip at a smaller scale."),
        ("offset-tread", "Offset Tread", "Offset plate", "Shift", "Mill shift", "The pattern missed its registration and stayed."),
        ("one-diamond", "One Diamond", "Single tread", "Seat", "Lone plate", "One raised fact."),
        ("rust-tread", "Rust Tread", "Rusted plate", "Bloom", "Yard rust", "The grip is becoming earth."),
        ("blue-plate", "Blue Plate", "Painted tread", "Coat", "Machine blue", "Shop paint over a threat."),
        ("corner-grip", "Corner Grip", "Tread crop", "Crop", "Edge mill", "Only the warning."),
        ("inverted-tread", "Inverted Tread", "Debossed plate", "Sink", "Negative steel", "The diamonds went in instead of out."),
        ("runway-plate", "Runway Plate", "Airstrip plate", "Align", "Tarmac silver", "A landing that never happens."),
    ],
    [  # 8 chainmail
        ("mail-field", "Mail Field", "Chainmail", "Rattle", "Armory steel", "A body of rings with no body inside."),
        ("butted-ring", "Butted Ring", "Butted mail", "Close", "Iron pale", "Cheap armor, honest about it."),
        ("riveted-mail", "Riveted Mail", "Riveted mail", "Lock", "Forge dark", "Each ring remembers a hammer."),
        ("gold-mail", "Gold Mail", "Gilt mail", "Gleam", "Relic gold", "Ceremony that could still cut."),
        ("scale-mail", "Scale Mail", "Scale mail", "Layer", "Dragon steel", "Rings pretending they are scales."),
        ("void-mail", "Void Mail", "Broken mail", "Gap", "Missing ring", "The wound is a missing circle."),
        ("copper-mail", "Copper Mail", "Copper mail", "Tarnish", "Penny mail", "Armor that wants to be a roof."),
        ("tiny-mail", "Tiny Mail", "Miniature mail", "Glint", "Toy steel", "A hauberk for no one."),
        ("japanese-mail", "Japanese Mail", "Kusari", "Drape", "Kusari ink", "Rings in a different grammar."),
        ("mail-collar", "Mail Collar", "Aventail", "Hang", "Helm steel", "A neck with no head."),
        ("rust-mail", "Rust Mail", "Rusted mail", "Bloom", "Bog iron", "Pulled from water and not cleaned."),
        ("blackened", "Blackened", "Blackened mail", "Absorb", "Night iron", "Armor that refuses highlight."),
        ("one-ring", "One Ring", "Single ring", "Turn", "Lone iron", "The rest of the shirt is implied."),
        ("mail-crop", "Mail Crop", "Mail crop", "Crop", "Edge steel", "A corner of a war."),
        ("ceremonial", "Ceremonial", "Parade mail", "Shine", "Parade silver", "Too bright to hide in."),
    ],
    [  # 9 cloisonne
        ("wire-cell", "Wire Cell", "Cloisonné", "Fill", "Kiln jewel", "Wires holding color the way a fence holds sheep."),
        ("enamel-well", "Enamel Well", "Cell enamel", "Well", "Jewel night", "A well of glass in a metal room."),
        ("lotus-cell", "Lotus Cell", "Lotus cloisonné", "Open", "Temple enamel", "A flower that is only partitions."),
        ("cloud-wire", "Cloud Wire", "Cloud cloisonné", "Drift", "Sky enamel", "Weather, soldered."),
        ("gold-cloison", "Gold Cloison", "Gold cloisonné", "Burnish", "Imperial gold", "A small empire."),
        ("broken-wire", "Broken Wire", "Broken cloisonné", "Gap", "Fracture enamel", "The fence failed. The color stayed."),
        ("tiny-cells", "Tiny Cells", "Micro cloisonné", "Glint", "Bead enamel", "Too small to be a story, still a city."),
        ("black-ground", "Black Ground", "Black cloisonné", "Absorb", "Lacquer enamel", "Night as a setting for wires."),
        ("one-cell", "One Cell", "Single cloison", "Hold", "Lone enamel", "One room of color."),
        ("silver-wire", "Silver Wire", "Silver cloisonné", "Trace", "Moon enamel", "Cold metal, warm glass."),
        ("vessel-lip", "Vessel Lip", "Vessel cloisonné", "Rim", "Vase jewel", "The rim of a jar that is not here."),
        ("geometric", "Geometric", "Geometric cloisonné", "Lock", "Deco enamel", "No flowers. Only law."),
        ("pale-enamel", "Pale Enamel", "Pale cloisonné", "Wash", "Opal cell", "Color that almost declined."),
        ("corner-wire", "Corner Wire", "Cloisonné crop", "Crop", "Edge jewel", "A fragment of a box."),
        ("fire-scale", "Fire Scale", "Fire cloisonné", "Pit", "Kiln ash", "The firing left a weather of its own."),
    ],
    [  # 10 sgraffito
        ("slip-scratch", "Slip Scratch", "Sgraffito", "Carve", "Terracotta slip", "Through the pale into the dark."),
        ("graffito-wall", "Graffito Wall", "Wall sgraffito", "Score", "Plaster umber", "A facade that writes on itself."),
        ("black-scratch", "Black Scratch", "Black sgraffito", "Cut", "Night slip", "The line is a wound in soot."),
        ("white-on-red", "White on Red", "Red-figure scratch", "Reveal", "Pot red", "A vase grammar without the vase."),
        ("combed-slip", "Combed Slip", "Combed slip", "Drag", "Comb clay", "Fingers, replaced by a tool, replaced by a loop."),
        ("one-cut", "One Cut", "Single sgraffito", "Slash", "Lone slip", "One decision through two colors."),
        ("lattice-cut", "Lattice Cut", "Lattice sgraffito", "Grid", "Garden slip", "A fence cut into clay."),
        ("script-scratch", "Script Scratch", "Script sgraffito", "Write", "Letter slip", "Words that are only their absence."),
        ("bird-scratch", "Bird Scratch", "Bird sgraffito", "Peck", "Avian slip", "A silhouette that is a scratch."),
        ("wet-carve", "Wet Carve", "Wet sgraffito", "Slip", "Wet terra", "Carved before it could dry."),
        ("fine-needle", "Fine Needle", "Needle sgraffito", "Tick", "Needle clay", "Almost engraving."),
        ("broad-gouged", "Broad Gouged", "Gouge sgraffito", "Gouge", "Wide slip", "The tool was not polite."),
        ("corner-scratch", "Corner Scratch", "Sgraffito crop", "Crop", "Edge slip", "A fragment of a pot."),
        ("inlaid-cut", "Inlaid Cut", "Inlaid sgraffito", "Fill", "Inlay clay", "The scratch, filled again, still a scar."),
        ("night-plaster", "Night Plaster", "Night sgraffito", "Score", "Moon plaster", "A wall after the lamps go out."),
    ],
    [  # 11 glaze drip
        ("celadon-run", "Celadon Run", "Celadon drip", "Run", "Jade kiln", "The glaze decided to leave."),
        ("tenmoku-spot", "Tenmoku Spot", "Tenmoku", "Well", "Oil-spot black", "Iron, pooled, then a star."),
        ("oribe-splash", "Oribe Splash", "Oribe", "Splash", "Oribe green", "A copper accident kept on purpose."),
        ("shino-crawl", "Shino Crawl", "Shino", "Crawl", "Shino orange", "The glaze refused to sit."),
        ("ash-run", "Ash Run", "Ash glaze", "Melt", "Wood ash", "The kiln’s weather, poured."),
        ("copper-red", "Copper Red", "Copper red", "Flush", "Sacrificial red", "A reduction that looks like a blush."),
        ("salt-orange", "Salt Orange", "Salt glaze", "Pit", "Salt orange", "Orange-peel from a vapor."),
        ("chun-opalescent", "Chun Opalescent", "Jun glaze", "Opalesce", "Jun blue", "A sky trapped in a bowl that is not here."),
        ("temmoku-hare", "Temmoku Hare", "Hare’s fur", "Streak", "Hare brown", "Fur without the animal."),
        ("drip-only", "Drip Only", "Single drip", "Drop", "Lone glaze", "One decision, gravity’s."),
        ("overfired", "Overfired", "Overfired drip", "Boil", "Blister kiln", "Too hot. Still a painting."),
        ("white-crawl", "White Crawl", "Crawl white", "Shrink", "Snow crawl", "The white left islands."),
        ("lip-run", "Lip Run", "Vessel lip", "Spill", "Rim glaze", "The pour over the edge."),
        ("night-tenmoku", "Night Tenmoku", "Night tenmoku", "Pool", "Void iron", "Blacker than the room."),
        ("postage-drip", "Postage Drip", "Drip stamp", "Crop", "Shard green", "A shard, issued."),
    ],
    [  # 12 piano
        ("keybed", "Keybed", "Piano key", "Travel", "Ivory ebony", "A keyboard with no song, still a walk."),
        ("player-roll", "Player Roll", "Piano roll", "Advance", "Perforated cream", "Holes that used to be notes."),
        ("prepared", "Prepared", "Prepared piano", "Mute", "Felt brass", "Objects on strings you cannot see."),
        ("harpsi", "Harpsi", "Harpsichord key", "Pluck", "Gilt cream", "A different attack, same furniture."),
        ("organ-manual", "Organ Manual", "Organ manual", "Stop", "Church wood", "Stops implied by color alone."),
        ("black-keys", "Black Keys", "Sharps only", "Skip", "Ebony night", "The pentatonic leftover."),
        ("broken-action", "Broken Action", "Broken action", "Jam", "Repair ivory", "A key that will not return."),
        ("tiny-spinet", "Tiny Spinet", "Spinet", "Tinkle", "Toy ivory", "Furniture for a smaller room."),
        ("felt-hammer", "Felt Hammer", "Hammer felt", "Strike", "Felt dust", "The hit, without the string."),
        ("sustain", "Sustain", "Sustain pedal", "Hold", "Pedal brass", "A bar that means continue."),
        ("lid-prop", "Lid Prop", "Piano lid", "Open", "Lacquer black", "A mouth."),
        ("tuning-pin", "Tuning Pin", "Tuning pin", "Turn", "Pin steel", "Hardware that is the music."),
        ("key-crop", "Key Crop", "Key crop", "Crop", "Ivory edge", "Only a few decisions."),
        ("night-keyboard", "Night Keyboard", "Night keyboard", "Walk", "Nocturne", "The keys after the concert."),
        ("one-key", "One Key", "Single key", "Depress", "Lone ivory", "Middle C with no middle."),
    ],
    [  # 13 lissajous
        ("figure-eight", "Figure Eight", "Lissajous", "Knot", "Scope amber", "Two tones arguing until they draw a knot."),
        ("scope-rose", "Scope Rose", "Oscilloscope rose", "Bloom", "CRT gold", "Not a phosphor hold. A ratio."),
        ("untuned", "Untuned", "Detuned figure", "Drift", "Slip amber", "The lock is lost. The drawing continues."),
        ("tight-ratio", "Tight Ratio", "High-order figure", "Weave", "Fine gold", "Too many lobes to count politely."),
        ("circle-lock", "Circle Lock", "Locked circle", "Hold", "Unity amber", "1:1. A circle that had to be earned."),
        ("square-wave", "Square Wave", "Square lissajous", "Chop", "Logic green", "The sine got honest."),
        ("phase-slip", "Phase Slip", "Phase portrait", "Slip", "Phase violet", "The second channel arrived late."),
        ("fat-trace", "Fat Trace", "Thick figure", "Glow", "Bloom gold", "A knot drawn with a tired beam."),
        ("tiny-knot", "Tiny Knot", "Miniature figure", "Spin", "Pocket amber", "A whole argument, small."),
        ("grid-scope", "Grid Scope", "Graticule figure", "Align", "Scope grid", "The knot vs the furniture."),
        ("red-beam", "Red Beam", "Red figure", "Burn", "Alert red", "A warning that learned choreography."),
        ("night-knot", "Night Knot", "Night lissajous", "Orbit", "Void gold", "The room is the afterglow."),
        ("crop-lobe", "Crop Lobe", "Lobe crop", "Crop", "Edge amber", "One petal of a ratio."),
        ("triple", "Triple", "Three-tone figure", "Braid", "Triple gold", "A third voice enters and ruins the bow."),
        ("still-dot", "Still Dot", "Spot figure", "Park", "Parked beam", "The tones agreed to stop. Almost."),
    ],
    [  # 14 zellige
        ("star-zellige", "Star Zellige", "Zellige star", "Lock", "Fes enamel", "A star that is only cuts."),
        ("cut-tile", "Cut Tile", "Hand-cut zellige", "Facet", "Mosaic mineral", "Irregular on purpose."),
        ("andusi", "Andusi", "Andalusian tile", "Repeat", "Cordoba glaze", "A memory of a courtyard."),
        ("black-star", "Black Star", "Black zellige", "Absorb", "Night tile", "A star that swallowed the room."),
        ("white-grid", "White Grid", "White zellige", "Calm", "Riad white", "Almost silence."),
        ("eight-fold", "Eight Fold", "Eight-point star", "Turn", "Islamic gold", "Geometry as hospitality."),
        ("broken-glaze", "Broken Glaze", "Crazed zellige", "Crack", "Craze mineral", "The glaze aged into a second pattern."),
        ("fountain-rim", "Fountain Rim", "Fountain zellige", "Ring", "Water tile", "A rim with no water."),
        ("tiny-cuts", "Tiny Cuts", "Micro zellige", "Glint", "Chip glaze", "A wall for a smaller riad."),
        ("green-field", "Green Field", "Green zellige", "Field", "Garden tile", "A garden with no plants."),
        ("one-star", "One Star", "Single zellige", "Seat", "Lone star", "The rest of the wall is implied."),
        ("corner-riad", "Corner Riad", "Zellige crop", "Crop", "Edge glaze", "A fragment of a courtyard."),
        ("gold-line", "Gold Line", "Gold zellige", "Trace", "Gilt tile", "The line is the luxury."),
        ("night-riad", "Night Riad", "Night zellige", "Dim", "Moon tile", "The courtyard after the lamps."),
        ("repair-tile", "Repair Tile", "Replacement zellige", "Patch", "Misfit glaze", "The new tile does not match. Good."),
    ],
    [  # 15 sashiko
        ("running-white", "Running White", "Sashiko", "Run", "Indigo white", "A repair that became a law."),
        ("shippo", "Shippo", "Shippo tsunagi", "Link", "Seven jewels", "Circles that refuse to close."),
        ("asanoha", "Asanoha", "Asanoha", "Radiate", "Hemp indigo", "Hemp leaf, stitched."),
        ("seigaiha", "Seigaiha", "Seigaiha", "Wave", "Wave indigo", "Waves that are only stitches."),
        ("higaki", "Higaki", "Higaki", "Fence", "Cypress stitch", "A fence drawn with thread."),
        ("kagome", "Kagome", "Kagome", "Weave", "Basket stitch", "A basket that is only holes."),
        ("boro-field", "Boro Field", "Boro", "Patch", "Mended indigo", "Patches that outlived the garment."),
        ("one-row", "One Row", "Single sashiko", "Sew", "Lone running", "One repair across a night."),
        ("dense-run", "Dense Run", "Dense sashiko", "Fill", "Work indigo", "So many repairs the cloth is new."),
        ("gold-sashiko", "Gold Sashiko", "Gold sashiko", "Gleam", "Gilt indigo", "Repair as jewelry."),
        ("pale-cloth", "Pale Cloth", "Pale sashiko", "Whisper", "Sky hemp", "Indigo that almost wasn’t."),
        ("corner-mend", "Corner Mend", "Sashiko crop", "Crop", "Edge indigo", "A fragment of a jacket."),
        ("hitomezashi", "Hitomezashi", "Hitomezashi", "Count", "Grid stitch", "Counted, then crossed."),
        ("night-mend", "Night Mend", "Night sashiko", "Run", "Void indigo", "Mending in the dark."),
        ("red-thread", "Red Thread", "Red sashiko", "Mark", "Amulet red", "A charm stitched as a field."),
    ],
    [  # 16 jalousie
        ("blind-slat", "Blind Slat", "Venetian blind", "Tilt", "Office cream", "A window that is only its refusal."),
        ("jalousie-glass", "Jalousie Glass", "Jalousie", "Crank", "Miami glass", "A climate drawn as slats."),
        ("shutter-pair", "Shutter Pair", "Plantation shutter", "Fold", "Porch white", "A porch without a house."),
        ("black-blind", "Black Blind", "Black blind", "Close", "Noir slat", "The room deciding not to see."),
        ("gold-slat", "Gold Slat", "Gilt blind", "Sheen", "Lobby brass", "Privacy as luxury."),
        ("one-slat", "One Slat", "Single slat", "Tilt", "Lone cream", "One decision about light."),
        ("broken-slat", "Broken Slat", "Broken blind", "Gap", "Repair slat", "The view leaks."),
        ("micro-blind", "Micro Blind", "Mini blind", "Tick", "Desk white", "A smaller refusal."),
        ("exterior-louver", "Exterior Louver", "Louver", "Shade", "Brutal concrete", "A facade’s eyelashes."),
        ("colored-slat", "Colored Slat", "Colored blind", "Cycle", "Motel tint", "A motel that is only its window."),
        ("night-blind", "Night Blind", "Night blind", "Close", "Sleep slat", "Drawn for a sleep that does not happen."),
        ("tilt-crop", "Tilt Crop", "Blind crop", "Crop", "Edge cream", "A fragment of a refusal."),
        ("wood-louver", "Wood Louver", "Wood louver", "Breathe", "Teak slat", "Furniture that used to be a tree’s privacy."),
        ("leaking-light", "Leaking Light", "Light leak", "Stripe", "Dawn slat", "The sun wins a little."),
        ("industrial-fin", "Industrial Fin", "Cooling fin", "Radiate", "Machine slat", "A blind that thinks it is an engine."),
    ],
    [  # 17 topo
        ("contour-ridge", "Contour Ridge", "Topographic ink", "Wind", "Survey brown", "Height without a hill."),
        ("closed-loop", "Closed Loop", "Closed contour", "Nest", "Map umber", "A summit that is only a sentence."),
        ("depression", "Depression", "Hachure pit", "Sink", "Pit brown", "A hole drawn politely."),
        ("index-contour", "Index Contour", "Index contour", "Bold", "Survey ink", "Every fifth line speaks up."),
        ("spot-height", "Spot Height", "Spot height", "Mark", "Triangle brown", "A number that forgot its digits."),
        ("ridge-crop", "Ridge Crop", "Contour crop", "Crop", "Edge survey", "A fragment of a range."),
        ("blue-hydro", "Blue Hydro", "Hydrography", "Flow", "River cyan", "Water as a law."),
        ("night-survey", "Night Survey", "Night topo", "Glow", "Moon survey", "A map after the office closed."),
        ("dense-relief", "Dense Relief", "Dense contour", "Crowd", "Steep brown", "The hill is almost black with trying."),
        ("sparse-plain", "Sparse Plain", "Sparse contour", "Rest", "Plain cream", "Almost no news."),
        ("fault-topo", "Fault Topo", "Faulted contour", "Break", "Rift brown", "The lines refuse to meet."),
        ("gold-survey", "Gold Survey", "Gilt contour", "Trace", "Gilt map", "A luxury map of nothing."),
        ("tiny-knoll", "Tiny Knoll", "Knoll", "Rise", "Pocket brown", "A hill for a smaller country."),
        ("bathymetry", "Bathymetry", "Bathymetry", "Deep", "Ocean ink", "Down, not up."),
        ("lone-contour", "Lone Contour", "Single contour", "Hold", "Lone brown", "One height. No neighbors."),
    ],
    [  # 18 fingerprint
        ("whorl", "Whorl", "Fingerprint whorl", "Turn", "Ink pad", "An identity with no person."),
        ("loop-print", "Loop Print", "Loop print", "Enter", "Pad black", "A loop that never names anyone."),
        ("arch-print", "Arch Print", "Arch print", "Rise", "Arch ink", "The quietest kind of identity."),
        ("double-loop", "Double Loop", "Double loop", "Braid", "Twin ink", "Two decisions in one pad."),
        ("latent", "Latent", "Latent print", "Dust", "Powder grey", "Found, not pressed."),
        ("smudged", "Smudged", "Smudged print", "Smear", "Bad lift", "The identity failed on purpose."),
        ("gold-dust", "Gold Dust", "Gold latent", "Spark", "Show powder", "A crime scene dressed for a lobby."),
        ("partial", "Partial", "Partial print", "Crop", "Edge pad", "Not enough for a court. Enough for a painting."),
        ("night-pad", "Night Pad", "Night print", "Press", "Void ink", "Pressed in the dark."),
        ("red-ink", "Red Ink", "Red pad", "Stamp", "Official red", "Bureaucracy as a fingertip."),
        ("tiny-whorl", "Tiny Whorl", "Miniature print", "Spin", "Pocket ink", "A smaller someone."),
        ("over-inked", "Over Inked", "Over-inked", "Flood", "Heavy pad", "Too much identity."),
        ("ridge-count", "Ridge Count", "Ridge count", "Tally", "File brown", "Counting as a landscape."),
        ("two-prints", "Two Prints", "Paired prints", "Meet", "Twin pad", "A meeting that is only ridges."),
        ("void-center", "Void Center", "Delta void", "Gap", "Delta ink", "The center declined."),
    ],
    [  # 19 corrugated
        ("box-flute", "Box Flute", "Corrugated flute", "Flex", "Carton kraft", "A box that forgot its product."),
        ("roof-iron", "Roof Iron", "Corrugated iron", "Weather", "Shed rust", "A shed elevated."),
        ("cardboard-edge", "Cardboard Edge", "Board edge", "Reveal", "Kraft stripe", "The flute, seen from the cut."),
        ("sine-sheet", "Sine Sheet", "Sine metal", "Wave", "Mill silver", "A sheet that refused to stay flat."),
        ("packing-void", "Packing Void", "Packing corrugate", "Cushion", "Void kraft", "Protection with nothing to protect."),
        ("painted-iron", "Painted Iron", "Painted corrugate", "Coat", "Barn red", "A barn that is only its skin."),
        ("tiny-flute", "Tiny Flute", "Microflute", "Tick", "Mailer kraft", "A smaller box."),
        ("night-iron", "Night Iron", "Night corrugate", "Dim", "Yard black", "The shed after closing."),
        ("gold-flute", "Gold Flute", "Gilt corrugate", "Flash", "Luxury kraft", "A box for nothing expensive."),
        ("crushed", "Crushed", "Crushed flute", "Fail", "Damaged kraft", "The cushion lost."),
        ("one-ridge", "One Ridge", "Single flute", "Hold", "Lone kraft", "One fold of a box."),
        ("edge-crop", "Edge Crop", "Corrugate crop", "Crop", "Cut kraft", "The cut is the picture."),
        ("plastic-flute", "Plastic Flute", "Corflute", "Flex", "Yard blue", "A sign that used to campaign."),
        ("wet-kraft", "Wet Kraft", "Wet corrugate", "Sag", "Rain kraft", "The box met weather."),
        ("aligned-flutes", "Aligned Flutes", "End-on flute", "Aim", "Tunnel kraft", "Looking down the tunnels."),
    ],
    [  # 20 paisley
        ("boteh", "Boteh", "Paisley boteh", "Curl", "Kashmir dye", "A seed that learned to be a comma."),
        ("shawl-field", "Shawl Field", "Paisley shawl", "Drape", "Kashmir night", "A field of commas."),
        ("one-boteh", "One Boteh", "Single boteh", "Seat", "Lone dye", "One seed."),
        ("gold-paisley", "Gold Paisley", "Gold paisley", "Burnish", "Brocade gold", "A comma in metal."),
        ("mono-paisley", "Mono Paisley", "Mono paisley", "Stamp", "Ink boteh", "No color, still a swagger."),
        ("tiny-boteh", "Tiny Boteh", "Micro paisley", "Speck", "Pocket dye", "A smaller swagger."),
        ("inverted", "Inverted Boteh", "Negative paisley", "Flip", "Void dye", "The comma as a hole."),
        ("border-paisley", "Border Paisley", "Paisley border", "March", "Edge kashmir", "The edge doing all the talking."),
        ("night-shawl", "Night Shawl", "Night paisley", "Dim", "Moon kashmir", "The shawl after the lamp."),
        ("red-boteh", "Red Boteh", "Red paisley", "Pulse", "Paisley red", "A seed that wants to be a heart."),
        ("pair-boteh", "Pair Boteh", "Paired boteh", "Face", "Twin dye", "Two commas conferring."),
        ("crop-curl", "Crop Curl", "Boteh crop", "Crop", "Edge dye", "Only the hook."),
        ("block-paisley", "Block Paisley", "Paisley block", "Stamp", "Wood dye", "Printed, not woven."),
        ("pale-kashmir", "Pale Kashmir", "Pale paisley", "Wash", "Mist dye", "A rumor of a shawl."),
        ("overgrown", "Overgrown", "Dense paisley", "Crowd", "Jungle dye", "Too many seeds."),
    ],
    [  # 21 bead loom
        ("loom-row", "Loom Row", "Bead loom", "String", "Trade bead", "A belt with no waist."),
        ("peyote", "Peyote", "Peyote stitch", "Offset", "Medicine bead", "A stagger that is a law."),
        ("brick-bead", "Brick Bead", "Brick stitch", "Bond", "Bead clay", "Beads pretending they are a wall."),
        ("wampum", "Wampum", "Wampum", "Treaty", "Shell purple", "A treaty with no parties named."),
        ("seed-grid", "Seed Grid", "Seed bead", "Tally", "Seed glass", "Counting as cloth."),
        ("one-strand", "One Strand", "Single strand", "Hang", "Lone bead", "One decision, vertical."),
        ("broken-thread", "Broken Thread", "Broken loom", "Gap", "Snap bead", "The belt failed."),
        ("gold-bead", "Gold Bead", "Gold bead", "Flash", "Gilt glass", "Trade that became jewelry."),
        ("tiny-loom", "Tiny Loom", "Miniature loom", "Tick", "Pocket bead", "A smaller treaty."),
        ("night-bead", "Night Bead", "Night loom", "Dim", "Void glass", "Strung in the dark."),
        ("color-crash", "Color Crash", "Crash bead", "Clash", "Fair bead", "The palette refused manners."),
        ("edge-loom", "Edge Loom", "Loom crop", "Crop", "Edge glass", "A fragment of a belt."),
        ("metal-bead", "Metal Bead", "Metal bead", "Clink", "Shop bead", "Hardware strung."),
        ("white-shell", "White Shell", "White wampum", "Calm", "Shell pale", "The quiet half of a treaty."),
        ("drop-fringe", "Drop Fringe", "Bead fringe", "Hang", "Fringe glass", "The belt growing a weather."),
    ],
    [  # 22 muqarnas
        ("honeycomb-vault", "Honeycomb Vault", "Muqarnas", "Cascade", "Vault gold", "A ceiling that climbs down."),
        ("alhambra-cell", "Alhambra Cell", "Alhambra muqarnas", "Nest", "Nasrid gold", "A palace reduced to one stalactite."),
        ("plaster-cell", "Plaster Cell", "Plaster muqarnas", "Cast", "Gesso cave", "White caves, stacked."),
        ("one-cell-vault", "One Cell Vault", "Single muqarnas", "Hang", "Lone gold", "One stalactite."),
        ("night-vault", "Night Vault", "Night muqarnas", "Dim", "Moon vault", "The ceiling after the lamps."),
        ("blue-cell", "Blue Cell", "Blue muqarnas", "Well", "Isfahan blue", "A sky hanging downward."),
        ("wood-muqarnas", "Wood Muqarnas", "Wood muqarnas", "Join", "Cedar vault", "Carpentry pretending it is stone."),
        ("tiny-vault", "Tiny Vault", "Miniature muqarnas", "Glint", "Pocket gold", "A smaller heaven."),
        ("broken-cell", "Broken Cell", "Broken muqarnas", "Gap", "Ruin gold", "The cave failed."),
        ("gold-leaf-vault", "Gold Leaf Vault", "Gilt muqarnas", "Burnish", "Leaf vault", "Light as structure."),
        ("corner-cascade", "Corner Cascade", "Muqarnas crop", "Crop", "Edge vault", "A fragment of a heaven."),
        ("flat-muqarnas", "Flat Muqarnas", "Plan muqarnas", "Plan", "Draft gold", "The ceiling, seen from above."),
        ("shadow-cell", "Shadow Cell", "Shadow muqarnas", "Shade", "Shade vault", "The caves as only their dark."),
        ("repair-vault", "Repair Vault", "Repaired muqarnas", "Patch", "Misfit gold", "The new cell does not match."),
        ("dense-cave", "Dense Cave", "Dense muqarnas", "Crowd", "Packed gold", "Too many heavens."),
    ],
    [  # 23 stencil
        ("spray-star", "Spray Star", "Stencil spray", "Mist", "Shop star", "A star that arrived as weather."),
        ("letter-stencil", "Letter Stencil", "Letter stencil", "Index", "Crate black", "A letter with no word."),
        ("bridge-stencil", "Bridge Stencil", "Bridged stencil", "Hold", "Army olive", "The bridges are the drawing."),
        ("one-spray", "One Spray", "Single spray", "Burst", "Lone mist", "One pull of the can."),
        ("over-spray", "Over Spray", "Over-spray", "Halo", "Halo black", "The accident around the law."),
        ("gold-stencil", "Gold Stencil", "Gold stencil", "Flash", "Show spray", "A crate dressed for a lobby."),
        ("tiny-stencil", "Tiny Stencil", "Mini stencil", "Tick", "Pocket spray", "A smaller instruction."),
        ("night-spray", "Night Spray", "Night stencil", "Mist", "Void spray", "Sprayed in the dark."),
        ("repeat-stamp", "Repeat Stamp", "Repeat stencil", "March", "Poster spray", "The same order, again."),
        ("broken-bridge", "Broken Bridge", "Broken stencil", "Gap", "Failed spray", "The letter leaked."),
        ("circle-cut", "Circle Cut", "Circle stencil", "Cut", "Dot spray", "A hole that makes a moon."),
        ("edge-mist", "Edge Mist", "Stencil crop", "Crop", "Edge spray", "A fragment of an order."),
        ("two-color", "Two Color", "Two-pass stencil", "Register", "Pass spray", "The second pass missed and stayed."),
        ("caution-stenc", "Caution Stenc", "Caution stencil", "Warn", "Shop yellow", "A warning with no hazard."),
        ("number-plate", "Number Plate", "Number stencil", "Count", "Lot white", "A digit that forgot its lot."),
    ],
    [  # 24 foil leaf
        ("gold-leaf", "Gold Leaf", "Gold leaf", "Lay", "Icon gold", "A square of sun, thin as rumor."),
        ("silver-leaf", "Silver Leaf", "Silver leaf", "Lay", "Icon silver", "Moon, beaten."),
        ("broken-leaf", "Broken Leaf", "Broken leaf", "Crack", "Fault gold", "The leaf failed. The fault is the drawing."),
        ("varnish-size", "Varnish Size", "Gilding size", "Tack", "Size amber", "The sticky hour before the leaf."),
        ("one-square", "One Square", "Single leaf", "Seat", "Lone gold", "One book of gold, one page."),
        ("skewings", "Skewings", "Skewings", "Scatter", "Waste gold", "The leftovers are the luxury."),
        ("night-leaf", "Night Leaf", "Night leaf", "Dim", "Void gold", "Gilding after the lamps."),
        ("copper-leaf", "Copper Leaf", "Copper leaf", "Tarnish", "Penny leaf", "A cheaper sun."),
        ("tiny-book", "Tiny Book", "Miniature leaf", "Glint", "Pocket gold", "A smaller icon."),
        ("burnish-spot", "Burnish Spot", "Burnished leaf", "Polish", "Mirror gold", "One place rubbed into a mirror."),
        ("matte-field", "Matte Field", "Matte leaf", "Flat", "Matte gold", "Gold that refused to shine."),
        ("edge-leaf", "Edge Leaf", "Leaf crop", "Crop", "Edge gold", "A fragment of an icon."),
        ("punch-dot", "Punch Dot", "Punched leaf", "Stamp", "Tool gold", "The gold, dotted like a sky."),
        ("water-gild", "Water Gild", "Water gilding", "Flood", "Bole red", "Red clay under a sun."),
        ("loose-leaf", "Loose Leaf", "Loose leaf", "Drift", "Floating gold", "Not yet stuck."),
    ],
    [  # 25 deckle
        ("deckle-edge", "Deckle Edge", "Deckle", "Tear", "Rag cream", "The edge that refuses a guillotine."),
        ("laid-line", "Laid Line", "Laid paper", "Wire", "Rag blue", "Wires remembered by pulp."),
        ("chain-line", "Chain Line", "Chain line", "Interval", "Rag interval", "The other wires."),
        ("watermark-wire", "Watermark Wire", "Watermark", "Glow", "Wire pale", "A picture that is only thinner."),
        ("torn-sheet", "Torn Sheet", "Torn rag", "Rip", "Rag wound", "A sheet that chose its own border."),
        ("one-edge", "One Edge", "Single deckle", "Hold", "Lone rag", "One ragged decision."),
        ("night-rag", "Night Rag", "Night paper", "Dim", "Void rag", "Pulp after the mill."),
        ("colored-rag", "Colored Rag", "Colored pulp", "Tint", "Mill tint", "The rag already had a past."),
        ("tiny-sheet", "Tiny Sheet", "Miniature deckle", "Crop", "Pocket rag", "A smaller sheet."),
        ("couching", "Couching", "Couched sheet", "Press", "Felt rag", "Wet, transferred, still a drawing."),
        ("vatman", "Vatman", "Vat dip", "Lift", "Vat cream", "The mould coming up."),
        ("edge-crop-rag", "Edge Crop Rag", "Deckle crop", "Crop", "Edge rag", "Only the tear."),
        ("gold-rag", "Gold Rag", "Gilt deckle", "Flash", "Luxury rag", "A torn edge dressed up."),
        ("two-sheets", "Two Sheets", "Overlapped deckle", "Stack", "Twin rag", "Two tears conferring."),
        ("dry-edge", "Dry Edge", "Dried deckle", "Cure", "Sun rag", "The tear, set."),
    ],
    [  # 26 ogham
        ("stone-score", "Stone Score", "Ogham", "Score", "Standing stone", "A language of cuts along an edge."),
        ("one-letter", "One Letter", "Single ogham", "Cut", "Lone score", "One name."),
        ("edge-script", "Edge Script", "Ogham edge", "Climb", "Pillar grey", "The arris is the page."),
        ("gold-score", "Gold Score", "Gilt ogham", "Inlay", "Gilt stone", "Cuts filled with sun."),
        ("wood-ogham", "Wood Ogham", "Wood ogham", "Carve", "Ogham oak", "A stick that is a sentence."),
        ("night-stone", "Night Stone", "Night ogham", "Dim", "Moon stone", "The pillar after the walkers leave."),
        ("dense-score", "Dense Score", "Dense ogham", "Crowd", "Packed score", "Too many names."),
        ("broken-pillar", "Broken Pillar", "Broken ogham", "Gap", "Ruin score", "The sentence failed mid-word."),
        ("tiny-score", "Tiny Score", "Miniature ogham", "Tick", "Pocket stone", "A smaller name."),
        ("red-cut", "Red Cut", "Red ogham", "Mark", "Amulet score", "A charm in cuts."),
        ("two-edges", "Two Edges", "Paired ogham", "Face", "Twin stone", "Two pillars conferring."),
        ("crop-arris", "Crop Arris", "Ogham crop", "Crop", "Edge stone", "A fragment of a name."),
        ("incised-deep", "Incised Deep", "Deep ogham", "Gouge", "Deep score", "The tool was sure."),
        ("faint-score", "Faint Score", "Faint ogham", "Whisper", "Weather stone", "Almost gone. Still a law."),
        ("new-cut", "New Cut", "Fresh ogham", "Open", "Fresh grey", "The stone still pale at the wound."),
    ],
    [  # 27 runway
        ("centerline", "Centerline", "Runway paint", "Aim", "Tarmac yellow", "A landing that does not happen."),
        ("threshold", "Threshold", "Threshold bars", "Hold", "Piano tarmac", "The bars that mean here."),
        ("touchdown", "Touchdown", "Touchdown mark", "Mark", "Aim white", "A place to hit that is only paint."),
        ("taxiway", "Taxiway", "Taxiway yellow", "Turn", "Hold short", "A path for a plane that is not here."),
        ("chevron-stop", "Chevron Stop", "Blast chevron", "Stop", "Blast yellow", "Do not go further."),
        ("one-stripe", "One Stripe", "Single centerline", "Hold", "Lone yellow", "One decision about direction."),
        ("night-tarmac", "Night Tarmac", "Night runway", "Glow", "Void tarmac", "The paint after the flights."),
        ("worn-paint", "Worn Paint", "Worn runway", "Fade", "Traffic yellow", "The landing wore the law away."),
        ("tiny-strip", "Tiny Strip", "Model runway", "Toy", "Pocket tarmac", "A smaller airport."),
        ("edge-lights", "Edge Lights", "Edge light", "Blink", "Blue edge", "Lights without a strip."),
        ("displaced", "Displaced", "Displaced threshold", "Shift", "Arrow tarmac", "The landing moved."),
        ("crop-tarmac", "Crop Tarmac", "Runway crop", "Crop", "Edge yellow", "A fragment of an approach."),
        ("closed-x", "Closed X", "Closed runway", "Cancel", "Closed white", "Do not land."),
        ("two-stripes", "Two Stripes", "Paired centerline", "Split", "Twin yellow", "Two directions conferring."),
        ("wet-tarmac", "Wet Tarmac", "Wet runway", "Sheen", "Rain tarmac", "The paint on water."),
    ],
    [  # 28 rattan
        ("cane-web", "Cane Web", "Cane webbing", "Seat", "Chair cane", "A seat with no chair."),
        ("wicker-hex", "Wicker Hex", "Wicker", "Bind", "Porch cane", "A porch that is only its weave."),
        ("rattan-peel", "Rattan Peel", "Rattan peel", "Wind", "Peel tan", "Skin of a vine."),
        ("one-hex-cane", "One Hex Cane", "Single cane hex", "Hold", "Lone cane", "One hole of a seat."),
        ("broken-cane", "Broken Cane", "Broken cane", "Gap", "Repair cane", "The seat failed."),
        ("night-cane", "Night Cane", "Night rattan", "Dim", "Void tan", "The porch after dinner."),
        ("painted-cane", "Painted Cane", "Painted wicker", "Coat", "Porch green", "A weave that took a color."),
        ("tiny-web", "Tiny Web", "Miniature cane", "Tick", "Pocket cane", "A smaller seat."),
        ("tight-bind", "Tight Bind", "Tight cane", "Tension", "Work cane", "No air left."),
        ("loose-web", "Loose Web", "Loose cane", "Sag", "Summer cane", "The seat gave."),
        ("edge-cane", "Edge Cane", "Cane crop", "Crop", "Edge tan", "A fragment of a chair."),
        ("binder-cane", "Binder Cane", "Binder cane", "Wrap", "Wrap tan", "The wrap that finishes a seat."),
        ("plastic-cane", "Plastic Cane", "Plastic cane", "Fake", "Patio white", "A porch that never was vine."),
        ("two-hex", "Two Hex", "Paired cane", "Meet", "Twin cane", "Two holes conferring."),
        ("sun-bleached", "Sun Bleached", "Bleached cane", "Fade", "Sun cane", "The porch won."),
    ],
    [  # 29 mezzotint
        ("rocker-ground", "Rocker Ground", "Mezzotint rocker", "Tooth", "Copper black", "A plate made of night, then scraped."),
        ("scrape-light", "Scrape Light", "Mezzotint scrape", "Lift", "Moon copper", "Light is what you remove."),
        ("roulette", "Roulette", "Roulette ground", "Roll", "Tooth grey", "A wheel that makes dark."),
        ("one-scrape", "One Scrape", "Single scrape", "Slash", "Lone copper", "One removal."),
        ("burnish-moon", "Burnish Moon", "Burnished mezzotint", "Polish", "Moon plate", "A moon made by rubbing."),
        ("void-copper", "Void Copper", "Night mezzotint", "Hold", "Void copper", "Almost no scrape. Almost a void."),
        ("coarse-tooth", "Coarse Tooth", "Coarse rocker", "Grit", "Heavy tooth", "The rocker was sure."),
        ("fine-tooth", "Fine Tooth", "Fine rocker", "Whisper", "Silk tooth", "A quieter night."),
        ("tiny-plate", "Tiny Plate", "Miniature mezzotint", "Glint", "Pocket copper", "A smaller dark."),
        ("over-rocked", "Over Rocked", "Over-rocked", "Flood", "Black flood", "Too much night."),
        ("edge-scrape", "Edge Scrape", "Mezzotint crop", "Crop", "Edge copper", "A fragment of a dark."),
        ("burr-catch", "Burr Catch", "Drypoint burr", "Catch", "Burr silver", "A different dark — the burr holds ink."),
        ("two-moons", "Two Moons", "Paired scrape", "Face", "Twin copper", "Two removals conferring."),
        ("red-ground", "Red Ground", "Red mezzotint", "Stain", "Blood copper", "Night in another color."),
        ("proof-wipe", "Proof Wipe", "Wiped proof", "Wipe", "Rag copper", "The plate after the printer."),
    ],
]


def _colors(work_id: int, layout: int) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    rng = random.Random(work_id * 7919 + layout * 104729)
    bg = (rng.randint(12, 248), rng.randint(12, 248), rng.randint(12, 248))
    ink = (255 - bg[0], 255 - bg[1], 255 - bg[2])
    if sum(abs(a - b) for a, b in zip(bg, ink)) < 220:
        ink = (12, 12, 14) if sum(bg) > 380 else (244, 240, 232)
    accent = (rng.randint(20, 240), rng.randint(20, 240), rng.randint(20, 240))
    mid = tuple(int((a + b) / 2) for a, b in zip(bg, ink))
    return bg, ink, accent, mid


def _header(work_id: int, slug: str, title: str, description: str, medium: str, motion: str, palette: str) -> str:
    return dedent(
        f'''
        """{medium}. Independent salon work {work_id}."""

        from __future__ import annotations

        import math

        import numpy as np
        from PIL import Image, ImageDraw

        from atelier.surface import WorkSpec

        SIZE = 512
        WORK = WorkSpec(
            id={work_id},
            slug={slug!r},
            title={title!r},
            description={description!r},
            medium={medium!r},
            motion={motion!r},
            palette={palette!r},
        )
        '''
    ).strip() + "\n\n"


def _paint_source(family: int, layout: int, bg, ink, accent, mid) -> str:
    mode = layout % 5
    pack = layout // 5
    scale = (0.72, 1.0, 1.28)[pack]
    ox = (-70, 0, 80)[pack]
    oy = (60, 0, -50)[pack]
    spin = (0.0, 0.35, -0.5)[pack]
    b, i, a, m = bg, ink, accent, mid
    common = f"""
    t = frame / 12 * math.tau
    bg, ink, accent, mid = {b}, {i}, {a}, {m}
    scale, ox, oy, spin = {scale:.3f}, {ox}, {oy}, {spin:.3f}
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    """
    body = {
        0: _body_seismo,
        1: _body_hex,
        2: _body_scale,
        3: _body_parquet,
        4: _body_tartan,
        5: _body_shibori,
        6: _body_terrazzo,
        7: _body_tread,
        8: _body_mail,
        9: _body_cloisonne,
        10: _body_sgraffito,
        11: _body_drip,
        12: _body_piano,
        13: _body_lissajous,
        14: _body_zellige,
        15: _body_sashiko,
        16: _body_jalousie,
        17: _body_topo,
        18: _body_print,
        19: _body_corrugate,
        20: _body_paisley,
        21: _body_bead,
        22: _body_muqarnas,
        23: _body_stencil,
        24: _body_leaf,
        25: _body_deckle,
        26: _body_ogham,
        27: _body_runway,
        28: _body_rattan,
        29: _body_mezzo,
    }[family](mode)
    return "def paint(frame: int) -> Image.Image:\n" + common + body + "\n    return canvas.convert(\"RGBA\")\n"


def _body_seismo(mode: int) -> str:
    if mode == 0:
        return """
    pts = []
    for x in range(24, 488):
        y = 256 + oy + int((70 * scale) * math.sin(x * 0.055 + t) + (28 * scale) * math.sin(x * 0.17 + t * 2))
        pts.append((x + ox // 4, y))
    draw.line(pts, fill=ink, width=max(2, int(3 * scale)))
    """
    if mode == 1:
        return """
    for row in range(7):
        pts = []
        base = 70 + row * 58
        for x in range(20, 492):
            y = base + int(16 * scale * math.sin(x * 0.08 + t + row))
            pts.append((x, y))
        draw.line(pts, fill=ink if row % 2 == 0 else accent, width=2)
    """
    if mode == 2:
        return """
    pts = []
    for k in range(240):
        ang = k / 240 * math.tau + t * 0.2
        r = 40 + (160 * scale) + 26 * math.sin(k * 0.35 + t)
        pts.append((256 + ox + r * math.cos(ang), 256 + oy + r * math.sin(ang)))
    draw.line([(int(x), int(y)) for x, y in pts], fill=ink, width=3)
    """
    if mode == 3:
        return """
    pts = [(20, 480)]
    for x in range(20, 492):
        y = 300 + int((90 * scale) * math.sin(x * 0.04 + t))
        pts.append((x, y))
    pts.append((492, 480))
    draw.polygon(pts, fill=ink)
    draw.polygon([(p[0], p[1] - 8) for p in pts[1:-1]], outline=accent)
    """
    return """
    draw.rectangle((90, 110, 422, 402), outline=ink, width=8)
    pts = []
    for x in range(110, 402):
        y = 256 + int(40 * math.sin(x * 0.12 + t))
        pts.append((x, y))
    draw.line(pts, fill=accent, width=3)
    """


def _body_hex(mode: int) -> str:
    if mode == 0:
        return """
    s = int(22 * scale)
    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = 40 + col * s * 1.75 + (row % 2) * s * 0.88 + 8 * math.cos(t + row)
            cy = 36 + row * s * 1.5
            r = s * 0.62
            pts = [(cx + r * math.cos(k * math.tau / 6 + spin), cy + r * math.sin(k * math.tau / 6 + spin)) for k in range(6)]
            draw.polygon([(int(x), int(y)) for x, y in pts], outline=ink, width=2)
    """
    if mode == 1:
        return """
    cx, cy, r = 256 + ox, 256 + oy, int(150 * scale)
    rot = t * 0.25 + spin
    pts = [(cx + r * math.cos(k * math.tau / 6 + rot), cy + r * math.sin(k * math.tau / 6 + rot)) for k in range(6)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink)
    draw.polygon([(int(256 + 70 * math.cos(k * math.tau / 6 + rot)), int(256 + 70 * math.sin(k * math.tau / 6 + rot))) for k in range(6)], fill=accent)
    """
    if mode == 2:
        return """
    s = int(48 * scale)
    for n, (cx, cy) in enumerate(((180, 200), (330, 210), (250, 340))):
        r = s + 10 * math.sin(t + n)
        pts = [(cx + r * math.cos(k * math.tau / 6), cy + r * math.sin(k * math.tau / 6)) for k in range(6)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if n == 1 else ink, outline=mid, width=4)
    """
    if mode == 3:
        return """
    s = int(14 * scale)
    for row in range(20):
        for col in range(20):
            cx = col * s * 1.7 + (row % 2) * 12
            cy = row * s * 1.5
            if (row + col + frame) % 5 == 0:
                draw.regular_polygon((cx, cy, s * 0.55), 6, rotation=spin * 40, fill=accent)
            else:
                draw.regular_polygon((cx, cy, s * 0.4), 6, outline=ink)
    """
    return """
    draw.rectangle((40, 40, 472, 472), outline=ink, width=6)
    r = int(90 * scale)
    draw.regular_polygon((256 + ox, 256 + oy, r), 6, rotation=t * 8, fill=accent, outline=ink)
    """


def _body_scale(mode: int) -> str:
    if mode == 0:
        return """
    step = int(28 * scale)
    for row, y in enumerate(range(20, 520, step)):
        shift = (row % 2) * step // 2 + int(6 * math.sin(t + row))
        for x in range(-20 + shift, 540, step):
            draw.chord((x, y, x + step + 8, y + step + 4), 200, 340, fill=ink if row % 3 else accent, outline=mid)
    """
    if mode == 1:
        return """
    for i in range(9):
        y = 40 + i * 48
        draw.pieslice((80, y, 430, y + 90), 200, 340, fill=ink if i % 2 == 0 else accent, outline=mid)
    """
    if mode == 2:
        return """
    cx, cy = 256 + ox, 300 + oy
    for i in range(8):
        r = int((40 + i * 22) * scale)
        draw.arc((cx - r, cy - r, cx + r, cy + r), 200 + 8 * math.sin(t), 340, fill=ink, width=6)
    """
    if mode == 3:
        return """
    draw.polygon([(256, 70), (420, 400), (90, 400)], fill=mid)
    for i, (x, y) in enumerate(((200, 180), (280, 200), (230, 260), (300, 280), (180, 300))):
        draw.chord((x, y, x + 50, y + 36), 200, 340, fill=accent if i == frame % 5 else ink)
    """
    return """
    draw.ellipse((60, 80, 450, 470), outline=ink, width=8)
    for y in range(120, 420, int(36 * scale)):
        for x in range(100, 400, 40):
            draw.chord((x, y, x + 34, y + 24), 210, 330, fill=accent)
    """


def _body_parquet(mode: int) -> str:
    if mode == 0:
        return """
    w, h = int(70 * scale), int(18 * scale)
    for row in range(16):
        for col in range(10):
            x = 20 + col * (w + 4) + (row % 2) * w // 2
            y = 20 + row * (h + 6)
            tilt = 18 if (row + col) % 2 == 0 else -18
            draw.polygon([(x, y), (x + w, y + tilt), (x + w, y + h + tilt), (x, y + h)], fill=ink if (row + col + frame) % 4 else accent)
    """
    if mode == 1:
        return """
    s = int(36 * scale)
    for y in range(16, 500, s):
        for x in range(16, 500, s):
            draw.rectangle((x, y, x + s - 4, y + s - 4), fill=ink if (x // s + y // s) % 2 else mid, outline=accent)
    """
    if mode == 2:
        return """
    draw.polygon([(256, 60), (452, 256), (256, 452), (60, 256)], outline=ink, width=6)
    for i in range(8):
        r = 40 + i * 22
        draw.rectangle((256 - r, 256 - 8, 256 + r, 256 + 8), outline=accent)
        draw.rectangle((256 - 8, 256 - r, 256 + 8, 256 + r), outline=ink)
    """
    if mode == 3:
        return """
    for i, y in enumerate(range(40, 480, int(28 * scale))):
        draw.rectangle((30 + (i % 3) * 8, y, 482, y + 16), fill=ink if i % 2 == 0 else accent)
        draw.line((30, y + 16, 482, y + 16), fill=mid, width=2)
    """
    return """
    draw.rectangle((48, 48, 464, 464), outline=ink, width=10)
    for i in range(6):
        x = 80 + i * 60
        draw.polygon([(x, 140), (x + 40, 200), (x + 40, 360), (x, 300)], fill=accent if i == frame % 6 else ink)
    """


def _body_tartan(mode: int) -> str:
    if mode == 0:
        return """
    for x in range(0, 512, int(28 * scale)):
        draw.rectangle((x, 0, x + 10, 512), fill=ink)
    for y in range(0, 512, int(36 * scale)):
        draw.rectangle((0, y, 512, y + 8), fill=accent)
    draw.rectangle((0, 0, 512, 512), outline=mid, width=18)
    """
    if mode == 1:
        return """
    bands = [18, 6, 40, 10, 22]
    x = 0
    for i, w in enumerate(bands * 8):
        draw.rectangle((x, 0, x + w, 512), fill=(ink, accent, mid, bg, ink)[i % 5])
        x += w
    y = int(80 + 40 * math.sin(t))
    draw.rectangle((0, y, 512, y + 26), fill=accent)
    """
    if mode == 2:
        return """
    draw.rectangle((0, 0, 512, 512), fill=mid)
    for i in range(14):
        p = int(i * 36 * scale)
        draw.line((p, 0, 512, 512 - p), fill=ink, width=3)
        draw.line((0, p, 512 - p, 512), fill=accent, width=2)
    """
    if mode == 3:
        return """
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for n in range(8):
        mgn = 60 + n * 22
        draw.rectangle((mgn, mgn, 512 - mgn, 512 - mgn), outline=accent if n % 2 else bg, width=4)
    """
    return """
    draw.polygon([(256, 30), (480, 256), (256, 482), (32, 256)], fill=ink)
    for i in range(-6, 7):
        draw.line((256 + i * 28, 30, 256 + i * 28, 482), fill=accent, width=2)
        draw.line((30, 256 + i * 28, 482, 256 + i * 28), fill=bg, width=2)
    """


def _body_shibori(mode: int) -> str:
    if mode == 0:
        return """
    step = int(36 * scale)
    for y in range(30, 490, step):
        for x in range(30 + (y // step % 2) * step // 2, 490, step):
            r = int(8 + 5 * math.sin(t + x * 0.02 + y * 0.02))
            draw.ellipse((x - r, y - r, x + r, y + r), fill=ink)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=bg)
    """
    if mode == 1:
        return """
    for i in range(16):
        y = 20 + i * int(30 * scale) + int(10 * math.sin(t + i))
        draw.arc((40, y, 472, y + 80), 0, 180, fill=ink, width=5)
    """
    if mode == 2:
        return """
    pts = [(256, 40), (420, 140), (380, 400), (130, 400), (90, 140)]
    draw.polygon(pts, fill=mid)
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        draw.line((p[0], p[1], q[0], q[1]), fill=ink, width=10)
    draw.regular_polygon((256 + int(20 * math.sin(t)), 240, 50), 4, fill=accent)
    """
    if mode == 3:
        return """
    for i in range(7):
        r = int((40 + i * 28) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=4)
    """
    return """
    draw.rectangle((0, 0, 512, int(220 + 40 * math.sin(t))), fill=ink)
    for x in range(20, 500, 18):
        draw.line((x, 0, x + 8, 512), fill=accent, width=2)
    """


def _body_terrazzo(mode: int) -> str:
    if mode == 0:
        return """
    rng = np.random.default_rng(21 + int(scale * 10))
    for n in range(int(90 * scale)):
        x, y = int(rng.integers(10, 500)), int(rng.integers(10, 500))
        w, h = int(rng.integers(6, 28)), int(rng.integers(4, 18))
        color = accent if n % 5 == frame % 5 else ink
        draw.polygon([(x, y), (x + w, y + 2), (x + w - 3, y + h), (x - 2, y + h - 1)], fill=color)
    """
    if mode == 1:
        return """
    draw.line((40, 40, 472, 40), fill=accent, width=8)
    draw.line((40, 40, 40, 472), fill=accent, width=8)
    rng = np.random.default_rng(8)
    for n in range(50):
        x, y = int(rng.integers(60, 450)), int(rng.integers(60, 450))
        draw.ellipse((x, y, x + 16, y + 10), fill=ink if n % 2 else mid)
    """
    if mode == 2:
        return """
    for i in range(12):
        x = 30 + (i * 41 + frame * 7) % 450
        y = 40 + (i * 73) % 420
        draw.regular_polygon((x, y, 18), 3 + (i % 3), fill=accent if i % 2 else ink)
    """
    if mode == 3:
        return """
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for i in range(20):
        draw.ellipse((100 + i * 12, 120 + (i * 17) % 200, 130 + i * 12, 150 + (i * 17) % 200), fill=ink)
    """
    return """
    draw.polygon([(40, 40), (472, 90), (430, 470), (70, 440)], fill=mid)
    draw.polygon([(200, 180), (260, 160), (240, 230)], fill=accent)
    draw.polygon([(300, 300), (360, 280), (340, 350)], fill=ink)
    """


def _body_tread(mode: int) -> str:
    if mode == 0:
        return """
    step = int(46 * scale)
    for y in range(20, 500, step):
        for x in range(20 + (y // step % 2) * step // 2, 500, step):
            draw.regular_polygon((x, y + int(3 * math.sin(t)), 14), 4, rotation=45, fill=ink)
    """
    if mode == 1:
        return """
    draw.rectangle((60, 60, 452, 452), fill=mid)
    for i in range(5):
        for j in range(5):
            draw.regular_polygon((120 + i * 70, 120 + j * 70, 22), 4, rotation=45 + t * 4, fill=ink)
    """
    if mode == 2:
        return """
    draw.regular_polygon((256 + ox, 256 + oy, int(120 * scale)), 4, rotation=45, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 40), 4, rotation=45 + t * 10, fill=accent)
    """
    if mode == 3:
        return """
    for i in range(10):
        y = 40 + i * 44
        for x in range(30, 480, 50):
            draw.polygon([(x, y), (x + 16, y + 8), (x, y + 16), (x - 16, y + 8)], fill=accent if i == frame % 10 else ink)
    """
    return """
    draw.rectangle((30, 30, 482, 482), outline=ink, width=12)
    draw.regular_polygon((256, 256, 90), 4, rotation=45, fill=accent)
    """


def _body_mail(mode: int) -> str:
    if mode == 0:
        return """
    s = int(22 * scale)
    for row in range(18):
        for col in range(18):
            cx = 20 + col * s + (row % 2) * s // 2
            cy = 20 + row * s * 0.72
            r = 10 + 2 * math.sin(t + row)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=2)
    """
    if mode == 1:
        return """
    for i, (cx, cy) in enumerate(((180, 200), (300, 200), (240, 300), (180, 300), (300, 300))):
        r = 48 + 8 * math.sin(t + i)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=8)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=accent)
    """
    if mode == 2:
        return """
    draw.ellipse((80, 80, 432, 432), outline=ink, width=16)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=10)
    """
    if mode == 3:
        return """
    r = int(70 * scale)
    draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=14)
    draw.ellipse((256 - 12, 256 - 12, 256 + 12, 256 + 12), fill=accent)
    """
    return """
    for i in range(6):
        x = 70 + i * 70
        draw.ellipse((x, 180, x + 64, 360), outline=ink if i % 2 else accent, width=5)
    """


def _body_cloisonne(mode: int) -> str:
    if mode == 0:
        return """
    cells = [(80, 80, 220, 240), (200, 70, 430, 200), (220, 190, 460, 400), (60, 230, 230, 450), (180, 300, 340, 470)]
    for n, box in enumerate(cells):
        draw.rectangle(box, fill=accent if n == frame % 5 else mid, outline=ink, width=5)
    """
    if mode == 1:
        return """
    draw.ellipse((70, 70, 442, 442), outline=ink, width=8)
    for k in range(8):
        ang = k * math.tau / 8 + t * 0.1
        x, y = 256 + 140 * math.cos(ang), 256 + 140 * math.sin(ang)
        draw.line((256, 256, x, y), fill=ink, width=5)
        draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=accent)
    """
    if mode == 2:
        return """
    draw.rectangle((100, 100, 412, 412), fill=accent, outline=ink, width=10)
    draw.rectangle((170, 170, 342, 342), fill=mid, outline=ink, width=6)
    """
    if mode == 3:
        return """
    for i in range(6):
        for j in range(6):
            draw.rectangle((40 + i * 76, 40 + j * 76, 100 + i * 76, 100 + j * 76), outline=ink, width=4, fill=accent if (i + j + frame) % 4 == 0 else mid)
    """
    return """
    draw.polygon([(256, 60), (430, 200), (370, 430), (140, 430), (80, 200)], fill=mid, outline=ink, width=8)
    draw.ellipse((200, 190, 312, 300), fill=accent)
    """


def _body_sgraffito(mode: int) -> str:
    if mode == 0:
        return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(18):
        x0, y0 = 20 + i * 26, 30
        draw.line((x0, y0, x0 + 80, 490), fill=bg, width=3)
    """
    if mode == 1:
        return """
    draw.rectangle((0, 0, 512, 512), fill=mid)
    draw.line((60, 80, 420, 400), fill=ink, width=16)
    draw.line((80, 400, 400, 90), fill=accent, width=10)
    """
    if mode == 2:
        return """
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for y in range(70, 450, int(28 * scale)):
        draw.line((70, y, 440, y + int(20 * math.sin(t + y))), fill=bg, width=2)
    """
    if mode == 3:
        return """
    draw.ellipse((60, 60, 452, 452), fill=ink)
    draw.arc((100, 100, 412, 412), 20 + t * 10, 200, fill=bg, width=12)
    """
    return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.polygon([(80, 400), (256, 80), (430, 400)], outline=bg, width=8)
    """


def _body_drip(mode: int) -> str:
    if mode == 0:
        return """
    for i, x in enumerate(range(40, 480, int(36 * scale))):
        h = int(180 + 140 * math.sin(t + i) * 0.5 + 80)
        draw.rectangle((x, 20, x + 18, 20 + h), fill=ink if i % 2 else accent)
        draw.ellipse((x - 6, 12 + h, x + 24, 40 + h), fill=ink if i % 2 else accent)
    """
    if mode == 1:
        return """
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 170, 300, 290), fill=accent)
    """
    if mode == 2:
        return """
    for i in range(9):
        x = 60 + i * 48
        draw.line((x, 30, x + int(20 * math.sin(t + i)), 480), fill=ink, width=int(8 * scale))
    """
    if mode == 3:
        return """
    draw.rectangle((0, 0, 512, 140), fill=ink)
    draw.polygon([(80, 140), (140, 420), (40, 420)], fill=accent)
    draw.polygon([(300, 140), (360, 460), (250, 460)], fill=mid)
    """
    return """
    draw.pieslice((40, 40, 472, 472), 200, 20 + 20 * math.sin(t), fill=ink)
    draw.ellipse((220, 220, 300, 300), fill=accent)
    """


def _body_piano(mode: int) -> str:
    if mode == 0:
        return """
    for i in range(14):
        x = 10 + i * 36
        pressed = i == (frame % 14)
        draw.rectangle((x, 80, x + 32, 430), fill=bg if not pressed else accent, outline=ink, width=3)
    for i, n in enumerate((1, 2, 4, 5, 6, 8, 9, 11, 12)):
        x = 32 + n * 36
        draw.rectangle((x, 80, x + 22, 250), fill=ink)
    """
    if mode == 1:
        return """
    for row in range(12):
        y = 20 + row * 40
        for col in range(16):
            if (row * 3 + col + frame) % 7 == 0:
                draw.rectangle((20 + col * 30, y, 44 + col * 30, y + 16), fill=ink)
    """
    if mode == 2:
        return """
    draw.rectangle((60, 180, 452, 260), fill=ink)
    draw.rectangle((200 + int(40 * math.sin(t)), 160, 280 + int(40 * math.sin(t)), 280), fill=accent)
    """
    if mode == 3:
        return """
    draw.rectangle((80, 200, 432, 280), fill=mid, outline=ink, width=6)
    draw.ellipse((220, 210, 300, 270), fill=accent)
    """
    return """
    draw.rectangle((40, 40, 120, 472), fill=ink)
    draw.rectangle((392, 40, 472, 472), fill=ink)
    draw.rectangle((140, 200 + int(30 * math.sin(t)), 372, 280), fill=accent)
    """


def _body_lissajous(mode: int) -> str:
    if mode == 0:
        return """
    pts = []
    a, b = 3, 2
    for k in range(360):
        u = k / 360 * math.tau
        x = 256 + ox + int(160 * scale * math.sin(a * u + t))
        y = 256 + oy + int(160 * scale * math.sin(b * u))
        pts.append((x, y))
    draw.line(pts, fill=ink, width=4)
    """
    if mode == 1:
        return """
    pts = []
    for k in range(400):
        u = k / 400 * math.tau
        x = 256 + int(180 * math.sin(5 * u + t))
        y = 256 + int(180 * math.sin(4 * u + t * 0.5))
        pts.append((x, y))
    draw.line(pts, fill=accent, width=3)
    """
    if mode == 2:
        return """
    draw.ellipse((96, 96, 416, 416), outline=ink, width=6)
    """
    if mode == 3:
        return """
    pts = []
    for k in range(200):
        u = k / 200 * math.tau
        x = 256 + int(140 * math.sin(2 * u + t))
        y = 256 + int(140 * (1 if math.sin(3 * u) > 0 else -1) * abs(math.sin(3 * u)))
        pts.append((x, y))
    draw.line(pts, fill=ink, width=5)
    """
    return """
    draw.ellipse((240 + int(10 * math.sin(t)), 240, 272, 272), fill=accent)
    draw.rectangle((40, 40, 472, 472), outline=ink, width=2)
    """


def _body_zellige(mode: int) -> str:
    if mode == 0:
        return """
    for i in range(8):
        for j in range(8):
            cx, cy = 40 + i * 60, 40 + j * 60
            pts = [(cx + 26 * math.cos(k * math.tau / 8 + spin), cy + 26 * math.sin(k * math.tau / 8 + spin)) for k in range(8)]
            draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if (i + j + frame) % 3 == 0 else ink)
    """
    if mode == 1:
        return """
    pts = [(256 + 180 * math.cos(k * math.tau / 8 + t * 0.1), 256 + 180 * math.sin(k * math.tau / 8 + t * 0.1)) for k in range(8)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent, width=6)
    """
    if mode == 2:
        return """
    for i in range(12):
        r = 20 + i * 18
        draw.regular_polygon((256, 256, r), 8, rotation=i * 8 + t * 4, outline=ink)
    """
    if mode == 3:
        return """
    draw.rectangle((60, 60, 452, 452), fill=mid)
    draw.regular_polygon((256 + ox, 256 + oy, int(90 * scale)), 8, fill=accent, outline=ink)
    """
    return """
    for k in range(6):
        ang = k * math.tau / 6
        draw.regular_polygon((256 + 120 * math.cos(ang), 256 + 120 * math.sin(ang), 40), 8, fill=ink if k % 2 else accent)
    """


def _body_sashiko(mode: int) -> str:
    if mode == 0:
        return """
    for y in range(40, 480, int(22 * scale)):
        for x in range(40, 480, 28):
            if ((x + y) // 20 + frame) % 3:
                draw.line((x, y, x + 12, y), fill=ink, width=3)
    """
    if mode == 1:
        return """
    for i in range(10):
        for j in range(10):
            cx, cy = 50 + i * 44, 50 + j * 44
            draw.arc((cx - 20, cy - 20, cx + 20, cy + 20), 0, 270, fill=ink, width=2)
    """
    if mode == 2:
        return """
    for i in range(7):
        for j in range(7):
            cx, cy = 70 + i * 60, 70 + j * 60
            for k in range(6):
                ang = k * math.tau / 6
                draw.line((cx, cy, cx + 22 * math.cos(ang), cy + 22 * math.sin(ang)), fill=ink, width=2)
    """
    if mode == 3:
        return """
    for row in range(9):
        y = 50 + row * 48
        draw.line((40, y, 472, y), fill=mid, width=2)
        for x in range(50, 460, 24):
            draw.line((x, y - 6, x, y + 6), fill=ink, width=3)
    """
    return """
    patches = [(60, 60, 220, 240), (200, 180, 400, 360), (120, 300, 340, 460)]
    for box in patches:
        draw.rectangle(box, outline=ink, width=4)
        draw.line((box[0] + 10, box[1] + 20, box[2] - 10, box[1] + 20), fill=accent, width=2)
    """


def _body_jalousie(mode: int) -> str:
    if mode == 0:
        return """
    for i, y in enumerate(range(20, 500, int(22 * scale))):
        tilt = int(10 * math.sin(t + i * 0.2))
        draw.polygon([(20, y), (492, y + tilt), (492, y + 14 + tilt), (20, y + 14)], fill=ink if i % 2 == 0 else accent)
    """
    if mode == 1:
        return """
    for i, x in enumerate(range(30, 490, 28)):
        draw.rectangle((x, 40, x + 16, 472), fill=ink if i % 2 else mid)
    """
    if mode == 2:
        return """
    draw.rectangle((80, 40, 432, 472), outline=ink, width=10)
    for y in range(70, 450, 24):
        draw.rectangle((100, y, 412, y + 10), fill=accent)
    """
    if mode == 3:
        return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    gap = int(18 + 10 * math.sin(t))
    for y in range(0, 512, 36):
        draw.rectangle((0, y, 512, y + gap), fill=bg)
    """
    return """
    draw.rectangle((40, 200, 472, 280), fill=ink)
    draw.rectangle((40, 200, 472, 220), fill=accent)
    """


def _body_topo(mode: int) -> str:
    if mode == 0:
        return """
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    z = np.sin((xx - 256 - ox) * 0.02 * scale) + np.cos((yy - 256 - oy) * 0.02 * scale + t)
    rings = np.sin(z * 6)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for c in range(3):
        rgb[..., c] = bg[c] + (ink[c] - bg[c]) * (rings > 0)
    canvas = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(canvas)
    """
    if mode == 1:
        return """
    for i in range(10):
        r = int((30 + i * 20) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=2 + (i % 5 == 0) * 2)
    """
    if mode == 2:
        return """
    for i in range(8):
        r = 40 + i * 24
        draw.ellipse((200 - r, 300 - r, 200 + r, 300 + r), outline=ink, width=2)
        draw.line((200 - 8, 300 + r, 200 + 8, 300 + r), fill=accent, width=2)
    """
    if mode == 3:
        return """
    draw.line((80, 400, 200, 180, 320, 260, 430, 90), fill=ink, width=6)
    draw.regular_polygon((430, 90, 8), 3, fill=accent)
    """
    return """
    for i in range(6):
        r = 50 + i * 30
        draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=accent if i == frame % 6 else ink, width=3)
    """


def _body_print(mode: int) -> str:
    if mode == 0:
        return """
    for ring in range(10, int(180 * scale), 8):
        draw.ellipse((256 - ring + ox, 256 - ring + oy, 256 + ring + ox, 256 + ring + oy), outline=ink, width=2)
    """
    if mode == 1:
        return """
    for i in range(12):
        a0 = -40 + i * 8
        a1 = 40 + i * 8
        draw.arc((80, 80, 432, 432), a0, a1, fill=ink, width=3)
    """
    if mode == 2:
        return """
    for i in range(14):
        draw.arc((60, 140 + i * 12, 452, 360 + i * 12), 200, 340, fill=ink, width=2)
    """
    if mode == 3:
        return """
    draw.ellipse((90, 90, 300, 360), outline=ink, width=3)
    draw.ellipse((220, 140, 430, 400), outline=accent, width=3)
    """
    return """
    draw.ellipse((140, 140, 372, 372), outline=ink, width=8)
    draw.ellipse((200, 200, 230, 230), fill=accent)
    """


def _body_corrugate(mode: int) -> str:
    if mode == 0:
        return """
    for x in range(0, 512, int(18 * scale)):
        draw.polygon([(x, 0), (x + 8, 0), (x + 8, 512), (x, 512)], fill=ink if (x // 18) % 2 else accent)
    """
    if mode == 1:
        return """
    pts_a, pts_b = [], []
    for y in range(0, 512, 4):
        wave = int(16 * scale * math.sin(y * 0.08 + t))
        pts_a.append((180 + wave, y))
        pts_b.append((320 + wave, y))
    draw.line(pts_a, fill=ink, width=10)
    draw.line(pts_b, fill=accent, width=10)
    """
    if mode == 2:
        return """
    for i, y in enumerate(range(0, 512, 16)):
        draw.rectangle((0, y, 512, y + 8), fill=ink if i % 2 else mid)
    """
    if mode == 3:
        return """
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for x in range(90, 420, 14):
        draw.line((x, 90, x, 420), fill=ink, width=3)
    """
    return """
    for i in range(8):
        x = 40 + i * 56
        draw.arc((x, 80, x + 56, 432), 270, 90, fill=ink if i % 2 else accent, width=8)
    """


def _body_paisley(mode: int) -> str:
    if mode == 0:
        return """
    def boteh(cx, cy, s, rot):
        pts = []
        for k in range(24):
            u = k / 24 * math.tau
            r = s * (0.65 + 0.35 * math.sin(u))
            x = cx + r * math.cos(u + rot)
            y = cy + r * math.sin(u + rot) - s * 0.35 * math.sin(u)
            pts.append((x, y))
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent)
    for i, (cx, cy) in enumerate(((180, 180), (320, 220), (240, 340), (360, 360), (140, 320))):
        boteh(cx + ox // 4, cy + oy // 4, 48 * scale, t * 0.2 + i)
    """
    if mode == 1:
        return """
    draw.pieslice((120, 80, 360, 400), 220, 40, fill=ink)
    draw.ellipse((230, 120, 300, 190), fill=accent)
    """
    if mode == 2:
        return """
    for i in range(6):
        x = 70 + (i % 3) * 140
        y = 90 + (i // 3) * 180
        draw.pieslice((x, y, x + 120, y + 160), 200, 20, fill=ink if i % 2 else accent)
    """
    if mode == 3:
        return """
    draw.pieslice((150 + ox, 90 + oy, 370 + ox, 420 + oy), 210, 30, fill=ink)
    """
    return """
    for i in range(20):
        x, y = 40 + (i * 47) % 420, 40 + (i * 89) % 420
        draw.pieslice((x, y, x + 40, y + 56), 210, 30, fill=accent if i == frame % 20 else ink)
    """


def _body_bead(mode: int) -> str:
    if mode == 0:
        return """
    colors = [ink, accent, mid, bg]
    for row in range(16):
        for col in range(16):
            x = 24 + col * 30 + (row % 2) * 15
            y = 24 + row * 30
            draw.ellipse((x, y, x + 16, y + 16), fill=colors[(row + col + frame) % 4], outline=ink)
    """
    if mode == 1:
        return """
    for row in range(18):
        for col in range(14):
            x = 40 + col * 30 + (row % 2) * 15
            y = 20 + row * 26
            draw.ellipse((x, y, x + 14, y + 14), fill=ink if (row + col) % 3 else accent)
    """
    if mode == 2:
        return """
    for i in range(9):
        x = 256 + int(8 * math.sin(t + i))
        draw.ellipse((x - 12, 30 + i * 50, x + 12, 54 + i * 50), fill=accent if i % 2 else ink)
    """
    if mode == 3:
        return """
    for i in range(20):
        draw.ellipse((40 + i * 22, 240, 56 + i * 22, 256), fill=ink if i % 2 else accent)
    """
    return """
    for i in range(12):
        draw.ellipse((200, 20 + i * 40, 312, 48 + i * 40), fill=mid)
        draw.ellipse((230, 28 + i * 40, 250, 48 + i * 40), fill=ink)
        draw.ellipse((262, 28 + i * 40, 282, 48 + i * 40), fill=accent)
    """


def _body_muqarnas(mode: int) -> str:
    if mode == 0:
        return """
    for row in range(7):
        count = 3 + row
        for col in range(count):
            x = 256 - count * 28 + col * 56
            y = 40 + row * 62
            draw.polygon([(x, y + 50), (x + 24, y), (x + 48, y + 50)], fill=ink if (row + col) % 2 else accent, outline=mid)
    """
    if mode == 1:
        return """
    draw.polygon([(256, 80), (400, 220), (330, 400), (180, 400), (110, 220)], fill=mid, outline=ink, width=6)
    draw.polygon([(256, 160), (320, 240), (256, 300), (190, 240)], fill=accent)
    """
    if mode == 2:
        return """
    draw.regular_polygon((256, 200, 80), 3, fill=ink)
    draw.regular_polygon((256, 320, 80), 3, rotation=180, fill=accent)
    """
    if mode == 3:
        return """
    draw.polygon([(256 + ox, 90 + oy), (360, 250), (150, 250)], fill=ink)
    """
    return """
    for i in range(5):
        for j in range(i + 1):
            x = 256 - i * 30 + j * 60
            y = 80 + i * 70
            draw.regular_polygon((x, y, 24), 3, fill=accent if (i + j + frame) % 3 == 0 else ink)
    """


def _body_stencil(mode: int) -> str:
    if mode == 0:
        return """
    draw.regular_polygon((256 + ox, 256 + oy, int(140 * scale)), 5, rotation=t * 6, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 50), 5, rotation=t * 6, fill=bg)
    """
    if mode == 1:
        return """
    draw.rectangle((80, 80, 200, 400), fill=ink)
    draw.rectangle((140, 140, 180, 200), fill=bg)
    draw.rectangle((140, 240, 180, 340), fill=bg)
    """
    if mode == 2:
        return """
    for i in range(4):
        draw.regular_polygon((130 + i * 90, 256, 40), 5, rotation=t * 4, fill=ink if i % 2 else accent)
    """
    if mode == 3:
        return """
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 180, 332, 332), fill=bg)
    """
    return """
    draw.polygon([(80, 80), (200, 80), (200, 200), (80, 200)], fill=accent)
    draw.line((80, 140, 200, 140), fill=bg, width=8)
    draw.line((140, 80, 140, 200), fill=bg, width=8)
    """


def _body_leaf(mode: int) -> str:
    if mode == 0:
        return """
    draw.rectangle((60, 60, 452, 452), fill=ink)
    crack = int(40 * math.sin(t))
    draw.line((60, 200 + crack, 452, 280 - crack), fill=bg, width=3)
    draw.line((200, 60, 260, 452), fill=bg, width=2)
    """
    if mode == 1:
        return """
    draw.rectangle((90, 90, 422, 422), fill=accent)
    draw.rectangle((140, 140, 372, 372), fill=ink)
    """
    if mode == 2:
        return """
    for i in range(16):
        x, y = 40 + (i * 53) % 420, 40 + (i * 97) % 420
        draw.rectangle((x, y, x + 36, y + 36), fill=ink if i % 2 else accent)
    """
    if mode == 3:
        return """
    draw.rectangle((120 + ox, 120 + oy, 392, 392), fill=ink)
    draw.ellipse((200, 200, 310, 310), fill=accent)
    """
    return """
    draw.rectangle((40, 40, 472, 472), outline=ink, width=20)
    draw.rectangle((80, 80, 432, 432), fill=accent)
    """


def _body_deckle(mode: int) -> str:
    if mode == 0:
        return """
    rng = np.random.default_rng(4)
    pts = []
    for i in range(40):
        ang = i / 40 * math.tau
        r = 200 + int(rng.integers(-18, 18))
        pts.append((256 + r * math.cos(ang), 256 + r * math.sin(ang)))
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=mid, outline=ink)
    """
    if mode == 1:
        return """
    for x in range(40, 480, 18):
        draw.line((x, 40, x, 472), fill=ink, width=1)
    for x in range(40, 480, 72):
        draw.line((x, 40, x, 472), fill=accent, width=3)
    """
    if mode == 2:
        return """
    draw.rectangle((70, 70, 442, 442), fill=mid)
    draw.ellipse((180, 180, 332, 332), outline=ink, width=1)
    """
    if mode == 3:
        return """
    draw.polygon([(40, 80), (470, 60), (450, 450), (70, 430)], fill=mid, outline=ink)
    """
    return """
    draw.rectangle((90, 90, 300, 400), fill=mid, outline=ink)
    draw.rectangle((220, 140, 430, 440), fill=accent, outline=ink)
    """


def _body_ogham(mode: int) -> str:
    if mode == 0:
        return """
    draw.line((256 + ox, 40, 256 + ox, 472), fill=ink, width=6)
    rng = np.random.default_rng(12)
    for i in range(14):
        y = 50 + i * 30
        side = 1 if i % 2 == 0 else -1
        n = 1 + (i + frame) % 5
        for k in range(n):
            draw.line((256, y + k * 5, 256 + side * 40 * scale, y + k * 5 - 10), fill=ink, width=3)
    """
    if mode == 1:
        return """
    draw.line((200, 60, 200, 450), fill=ink, width=8)
    draw.line((200, 180, 320, 140), fill=accent, width=6)
    draw.line((200, 260, 340, 260), fill=accent, width=6)
    """
    if mode == 2:
        return """
    for x in (160, 256, 352):
        draw.line((x, 50, x, 460), fill=ink, width=5)
        for i in range(8):
            y = 70 + i * 48
            draw.line((x - 30, y, x + 30, y - 12), fill=accent, width=3)
    """
    if mode == 3:
        return """
    draw.line((80, 400, 430, 90), fill=ink, width=7)
    for i in range(9):
        x = 100 + i * 36
        y = 380 - i * 32
        draw.line((x, y, x + 20, y - 28), fill=accent, width=3)
    """
    return """
    draw.line((256, 80, 256, 432), fill=ink, width=10)
    draw.line((256, 200, 360, 160), fill=accent, width=8)
    """


def _body_runway(mode: int) -> str:
    if mode == 0:
        return """
    draw.rectangle((220, 20, 292, 492), fill=mid)
    for y in range(30, 480, 36):
        draw.rectangle((246, y, 266, y + 18), fill=ink if (y // 36 + frame) % 2 else accent)
    """
    if mode == 1:
        return """
    for i in range(8):
        draw.rectangle((80 + i * 12, 80, 88 + i * 12, 200), fill=ink)
    draw.rectangle((80, 360, 432, 400), fill=accent)
    """
    if mode == 2:
        return """
    draw.polygon([(256, 40), (300, 120), (212, 120)], fill=ink)
    draw.polygon([(256, 472), (300, 392), (212, 392)], fill=ink)
    draw.rectangle((248, 140, 264, 372), fill=accent)
    """
    if mode == 3:
        return """
    draw.line((60, 80, 200, 200, 80, 340, 240, 430), fill=ink, width=14)
    draw.regular_polygon((240, 430, 16), 4, rotation=45, fill=accent)
    """
    return """
    draw.line((80, 80, 432, 432), fill=ink, width=18)
    draw.line((120, 80, 472, 432), fill=accent, width=8)
    draw.line((200, 180, 312, 292), fill=bg, width=10)
    """


def _body_rattan(mode: int) -> str:
    if mode == 0:
        return """
    s = int(36 * scale)
    for y in range(20, 500, s):
        for x in range(20, 500, s):
            draw.ellipse((x, y, x + s, y + s), outline=ink, width=3)
    """
    if mode == 1:
        return """
    for i in range(12):
        for j in range(12):
            x, y = 20 + i * 40, 20 + j * 40
            draw.arc((x, y, x + 40, y + 40), 0, 180, fill=ink, width=3)
            draw.arc((x + 20, y + 20, x + 60, y + 60), 180, 360, fill=accent, width=3)
    """
    if mode == 2:
        return """
    draw.ellipse((80, 80, 432, 432), outline=ink, width=8)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=6)
    """
    if mode == 3:
        return """
    draw.ellipse((180 + ox, 180 + oy, 332, 332), outline=ink, width=10)
    """
    return """
    for i in range(8):
        draw.arc((40 + i * 10, 80, 472 - i * 10, 432), 200, 340, fill=ink if i % 2 else accent, width=3)
    """


def _body_mezzo(mode: int) -> str:
    if mode == 0:
        return """
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    tooth = (np.sin(xx * 0.35) * np.sin(yy * 0.35) > 0).astype(np.float32)
    light = np.exp(-((xx - 260 - 20 * math.cos(t)) ** 2 + (yy - 220) ** 2) / (9000 * scale))
    mix = np.clip(tooth * 0.45 + light, 0, 1)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for c in range(3):
        rgb[..., c] = ink[c] + (bg[c] - ink[c]) * mix
    canvas = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(canvas)
    """
    if mode == 1:
        return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((160 + ox, 140 + oy, 360, 360), fill=accent)
    """
    if mode == 2:
        return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(40):
        x = 20 + i * 12
        draw.line((x, 20, x + 8, 492), fill=mid, width=1)
    """
    if mode == 3:
        return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.line((80, 400, 400, 90), fill=bg, width=18)
    """
    return """
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((180, 180, 250, 250), fill=bg)
    draw.ellipse((280, 260, 350, 330), fill=accent)
    """


def write_expansion() -> list[Path]:
    written: list[Path] = []
    seen_slugs: set[str] = set()
    seen_media: set[str] = set()
    seen_titles: set[str] = set()
    for index in range(450):
        family = index % 30
        layout = index // 30
        work_id = 51 + index
        slug, title, medium, motion, palette, description = FAMILIES[family][layout]
        reserved = {
            "shift-block", "two-plate", "phosphor-hold", "tide-cut", "seed-field", "proof-sheet",
            "torn-stack", "interference", "hold-still", "tube-script", "pressed-leaf", "trace-board",
            "nine-patch", "calcite", "night-plate", "tesserae", "rime", "plume", "lockup",
            "fold-plane", "hatch-dune", "lead-light", "punch", "wet-bloom", "cross-stitch",
            "lino-bite", "teletype", "kintsugi", "waybill", "instant-peel", "ben-day", "ikat-shift",
            "tape-window", "bitten-plate", "yield-field", "sand-ring", "carbon-copy", "barricade",
            "urushi", "radar-sweep", "pennant-line", "microfiche", "garter-knit", "slate-dust",
            "encaustic", "cork-pins", "cell-pour", "staff-walk", "flemish-bond", "thermograph",
        }
        if slug in reserved or slug in seen_slugs or title in seen_titles or medium in seen_media:
            raise SystemExit(f"duplicate metadata at {work_id}: {slug} / {title} / {medium}")
        seen_slugs.add(slug)
        seen_titles.add(title)
        seen_media.add(medium)
        bg, ink, accent, mid = _colors(work_id, layout)
        source = _header(work_id, slug, title, description, medium, motion, palette)
        source += _paint_source(family, layout, bg, ink, accent, mid)
        path = WORKS_DIR / f"{work_id:03d}_{slug.replace('-', '_')}.py"
        path.write_text(source, encoding="utf-8")
        written.append(path)
    print(f"wrote {len(written)} painters (51-500)")
    return written


if __name__ == "__main__":
    write_expansion()
