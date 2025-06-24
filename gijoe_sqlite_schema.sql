-- SQLite Database Schema for G.I. Joe Data
-- Compatible with SQLite database engine
-- Run with: sqlite3 weather_dominator.db < gijoe_sqlite_schema.sql

PRAGMA foreign_keys = ON;

-- G.I. Joe Characters table
CREATE TABLE IF NOT EXISTS gijoe_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    real_name TEXT,
    code_name TEXT,
    faction TEXT CHECK (faction IN ('G.I. Joe', 'Cobra', 'Independent', 'Other')),
    rank_title TEXT,
    specialty TEXT,
    birthplace TEXT,
    bio TEXT,
    first_appearance TEXT,
    voice_actor TEXT,
    wiki_url TEXT,
    image_url TEXT,
    status TEXT CHECK (status IN ('Active', 'Deceased', 'Missing', 'Retired')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Vehicles table  
CREATE TABLE IF NOT EXISTS gijoe_vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    year_introduced INTEGER,
    faction TEXT CHECK (faction IN ('G.I. Joe', 'Cobra', 'Independent', 'Other')),
    category TEXT CHECK (category IN ('Aircraft', 'Land Vehicle', 'Naval', 'Space', 'Other')),
    vehicle_type TEXT,
    description TEXT,
    pilot_driver TEXT,
    crew_capacity INTEGER,
    weapons TEXT,
    features TEXT,
    specifications TEXT,
    wiki_url TEXT,
    image_url TEXT,
    toy_line TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Weapons table
CREATE TABLE IF NOT EXISTS gijoe_weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    weapon_type TEXT,
    faction TEXT CHECK (faction IN ('G.I. Joe', 'Cobra', 'Independent', 'Neutral')),
    description TEXT,
    specifications TEXT,
    used_by TEXT,
    first_appearance TEXT,
    wiki_url TEXT,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Locations table
CREATE TABLE IF NOT EXISTS gijoe_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    location_type TEXT,
    faction TEXT CHECK (faction IN ('G.I. Joe', 'Cobra', 'Independent', 'Neutral')),
    description TEXT,
    geographic_location TEXT,
    purpose_function TEXT,
    notable_features TEXT,
    first_appearance TEXT,
    wiki_url TEXT,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- Character-Vehicle relationships
CREATE TABLE IF NOT EXISTS character_vehicle_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    relationship_type TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES gijoe_vehicles(id) ON DELETE CASCADE,
    UNIQUE(character_id, vehicle_id, relationship_type)
);

-- Character-Weapon relationships  
CREATE TABLE IF NOT EXISTS character_weapon_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    weapon_id INTEGER NOT NULL,
    relationship_type TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id) ON DELETE CASCADE,
    FOREIGN KEY (weapon_id) REFERENCES gijoe_weapons(id) ON DELETE CASCADE,
    UNIQUE(character_id, weapon_id, relationship_type)
);

-- Database indexes for performance
CREATE INDEX IF NOT EXISTS idx_characters_name ON gijoe_characters(name);
CREATE INDEX IF NOT EXISTS idx_characters_faction ON gijoe_characters(faction);
CREATE INDEX IF NOT EXISTS idx_characters_specialty ON gijoe_characters(specialty);

CREATE INDEX IF NOT EXISTS idx_vehicles_name ON gijoe_vehicles(name);  
CREATE INDEX IF NOT EXISTS idx_vehicles_faction ON gijoe_vehicles(faction);
CREATE INDEX IF NOT EXISTS idx_vehicles_category ON gijoe_vehicles(category);
CREATE INDEX IF NOT EXISTS idx_vehicles_year ON gijoe_vehicles(year_introduced);

CREATE INDEX IF NOT EXISTS idx_weapons_name ON gijoe_weapons(name);
CREATE INDEX IF NOT EXISTS idx_weapons_type ON gijoe_weapons(weapon_type);
CREATE INDEX IF NOT EXISTS idx_weapons_faction ON gijoe_weapons(faction);

CREATE INDEX IF NOT EXISTS idx_locations_name ON gijoe_locations(name);
CREATE INDEX IF NOT EXISTS idx_locations_type ON gijoe_locations(location_type);
CREATE INDEX IF NOT EXISTS idx_locations_faction ON gijoe_locations(faction);

-- Views for easier data access
CREATE VIEW IF NOT EXISTS gijoe_team_members AS
SELECT 
    name, real_name, rank_title, specialty, birthplace, status
FROM gijoe_characters 
WHERE faction = 'G.I. Joe' AND status = 'Active';

CREATE VIEW IF NOT EXISTS cobra_forces AS
SELECT 
    name, real_name, rank_title, specialty, status
FROM gijoe_characters 
WHERE faction = 'Cobra' AND status = 'Active';

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

-- Insert trigger to update timestamp
CREATE TRIGGER IF NOT EXISTS update_character_timestamp 
    AFTER UPDATE ON gijoe_characters
BEGIN
    UPDATE gijoe_characters SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_vehicle_timestamp 
    AFTER UPDATE ON gijoe_vehicles  
BEGIN
    UPDATE gijoe_vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_weapon_timestamp 
    AFTER UPDATE ON gijoe_weapons
BEGIN
    UPDATE gijoe_weapons SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_location_timestamp 
    AFTER UPDATE ON gijoe_locations
BEGIN
    UPDATE gijoe_locations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
