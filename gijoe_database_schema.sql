-- G.I. Joe Database Extension Script
-- Adds tables for comprehensive G.I. Joe data from gijoe.fandom.com

-- G.I. Joe Characters table (enhanced version of character_lookups)
CREATE TABLE IF NOT EXISTS gijoe_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    real_name TEXT,
    code_name TEXT,
    faction TEXT,  -- 'G.I. Joe', 'Cobra', 'Independent', 'Other'
    rank TEXT,
    specialty TEXT,
    birthplace TEXT,
    bio TEXT,
    first_appearance TEXT,
    voice_actor TEXT,
    wiki_url TEXT,
    image_url TEXT,
    status TEXT,  -- 'Active', 'Deceased', 'Missing', 'Retired'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT  -- JSON string of full character data
);

-- G.I. Joe Vehicles table
CREATE TABLE IF NOT EXISTS gijoe_vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    year_introduced INTEGER,
    faction TEXT,  -- 'G.I. Joe', 'Cobra', 'Other'
    category TEXT,  -- 'Aircraft', 'Land Vehicle', 'Naval', 'Space Vehicle'
    vehicle_type TEXT,  -- 'Tank', 'Helicopter', 'Jet', 'Boat', etc.
    description TEXT,
    pilot_driver TEXT,
    crew_capacity INTEGER,
    weapons TEXT,
    features TEXT,
    specifications TEXT,
    wiki_url TEXT,
    image_url TEXT,
    toy_line TEXT,  -- Original toy line it appeared in
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT  -- JSON string of full vehicle data
);

-- G.I. Joe Weapons/Equipment table
CREATE TABLE IF NOT EXISTS gijoe_weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT,  -- 'Rifle', 'Pistol', 'Launcher', 'Melee', 'Equipment'
    faction TEXT,  -- 'G.I. Joe', 'Cobra', 'Neutral'
    description TEXT,
    specifications TEXT,
    used_by TEXT,  -- Characters who commonly use this weapon
    first_appearance TEXT,
    wiki_url TEXT,
    image_url TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Locations/Bases table
CREATE TABLE IF NOT EXISTS gijoe_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT,  -- 'Base', 'City', 'Country', 'Facility', 'Vehicle'
    faction TEXT,  -- 'G.I. Joe', 'Cobra', 'Neutral'
    description TEXT,
    location TEXT,  -- Geographic location
    purpose TEXT,
    notable_features TEXT,
    first_appearance TEXT,
    wiki_url TEXT,
    image_url TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Episodes/Media table
CREATE TABLE IF NOT EXISTS gijoe_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT,  -- 'TV Episode', 'Movie', 'Comic', 'Video Game'
    series TEXT,  -- Which series/comic line
    season INTEGER,
    episode_number INTEGER,
    air_date DATE,
    description TEXT,
    characters_featured TEXT,
    vehicles_featured TEXT,
    wiki_url TEXT,
    imdb_url TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- Character-Vehicle relationships (many-to-many)
CREATE TABLE IF NOT EXISTS character_vehicle_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    vehicle_id INTEGER,
    relationship_type TEXT,  -- 'Primary Pilot', 'Secondary Pilot', 'Driver', 'Gunner'
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
    FOREIGN KEY (vehicle_id) REFERENCES gijoe_vehicles(id),
    UNIQUE(character_id, vehicle_id, relationship_type)
);

-- Character-Weapon relationships (many-to-many)
CREATE TABLE IF NOT EXISTS character_weapon_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    weapon_id INTEGER,
    relationship_type TEXT,  -- 'Primary Weapon', 'Secondary Weapon', 'Signature Weapon'
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
    FOREIGN KEY (weapon_id) REFERENCES gijoe_weapons(id),
    UNIQUE(character_id, weapon_id, relationship_type)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_characters_name ON gijoe_characters(name);
CREATE INDEX IF NOT EXISTS idx_characters_faction ON gijoe_characters(faction);
CREATE INDEX IF NOT EXISTS idx_characters_specialty ON gijoe_characters(specialty);

CREATE INDEX IF NOT EXISTS idx_vehicles_name ON gijoe_vehicles(name);
CREATE INDEX IF NOT EXISTS idx_vehicles_faction ON gijoe_vehicles(faction);
CREATE INDEX IF NOT EXISTS idx_vehicles_category ON gijoe_vehicles(category);
CREATE INDEX IF NOT EXISTS idx_vehicles_year ON gijoe_vehicles(year_introduced);

CREATE INDEX IF NOT EXISTS idx_weapons_name ON gijoe_weapons(name);
CREATE INDEX IF NOT EXISTS idx_weapons_type ON gijoe_weapons(type);
CREATE INDEX IF NOT EXISTS idx_weapons_faction ON gijoe_weapons(faction);

CREATE INDEX IF NOT EXISTS idx_locations_name ON gijoe_locations(name);
CREATE INDEX IF NOT EXISTS idx_locations_type ON gijoe_locations(type);
CREATE INDEX IF NOT EXISTS idx_locations_faction ON gijoe_locations(faction);

CREATE INDEX IF NOT EXISTS idx_media_title ON gijoe_media(title);
CREATE INDEX IF NOT EXISTS idx_media_type ON gijoe_media(type);
CREATE INDEX IF NOT EXISTS idx_media_series ON gijoe_media(series);

-- Views for common queries
CREATE VIEW IF NOT EXISTS cobra_characters AS
SELECT * FROM gijoe_characters WHERE faction = 'Cobra';

CREATE VIEW IF NOT EXISTS joe_characters AS
SELECT * FROM gijoe_characters WHERE faction = 'G.I. Joe';

CREATE VIEW IF NOT EXISTS cobra_vehicles AS
SELECT * FROM gijoe_vehicles WHERE faction = 'Cobra';

CREATE VIEW IF NOT EXISTS joe_vehicles AS
SELECT * FROM gijoe_vehicles WHERE faction = 'G.I. Joe';

CREATE VIEW IF NOT EXISTS character_vehicle_summary AS
SELECT 
    c.name as character_name,
    c.faction as character_faction,
    v.name as vehicle_name,
    v.category as vehicle_category,
    cvr.relationship_type
FROM gijoe_characters c
JOIN character_vehicle_relations cvr ON c.id = cvr.character_id
JOIN gijoe_vehicles v ON v.id = cvr.vehicle_id;
