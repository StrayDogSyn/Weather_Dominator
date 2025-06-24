-- G.I. Joe Database Extension Script (Standard SQL)
-- Adds tables for comprehensive G.I. Joe data from gijoe.fandom.com
-- Compatible with: SQLite, PostgreSQL, MySQL, SQL Server (with minor adaptations)
-- Database Type: Standards-compliant SQL

-- ================================
-- CORE TABLES
-- ================================

-- G.I. Joe Characters table (enhanced version of character_lookups)
CREATE TABLE gijoe_characters (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    real_name VARCHAR(255),
    code_name VARCHAR(255),
    faction VARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Independent', 'Other'
    rank VARCHAR(100),
    specialty VARCHAR(255),
    birthplace VARCHAR(255),
    bio TEXT,
    first_appearance VARCHAR(255),
    voice_actor VARCHAR(255),
    wiki_url VARCHAR(500),
    image_url VARCHAR(500),
    status VARCHAR(50),  -- 'Active', 'Deceased', 'Missing', 'Retired'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT  -- JSON string of full character data
);

-- G.I. Joe Vehicles table
CREATE TABLE gijoe_vehicles (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    year_introduced INTEGER,
    faction VARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Other'
    category VARCHAR(100),  -- 'Aircraft', 'Land Vehicle', 'Naval', 'Space Vehicle'
    vehicle_type VARCHAR(100),  -- 'Tank', 'Helicopter', 'Jet', 'Boat', etc.
    description TEXT,
    pilot_driver VARCHAR(255),
    crew_capacity INTEGER,
    weapons TEXT,
    features TEXT,
    specifications TEXT,
    wiki_url VARCHAR(500),
    image_url VARCHAR(500),
    toy_line VARCHAR(255),  -- Original toy line it appeared in
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT  -- JSON string of full vehicle data
);

-- G.I. Joe Weapons/Equipment table
CREATE TABLE gijoe_weapons (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(100),  -- 'Rifle', 'Pistol', 'Launcher', 'Melee', 'Equipment'
    faction VARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Neutral'
    description TEXT,
    specifications TEXT,
    used_by VARCHAR(500),  -- Characters who commonly use this weapon
    first_appearance VARCHAR(255),
    wiki_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Locations/Bases table
CREATE TABLE gijoe_locations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(100),  -- 'Base', 'City', 'Country', 'Facility', 'Vehicle'
    faction VARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Neutral'
    description TEXT,
    location VARCHAR(255),  -- Geographic location
    purpose VARCHAR(255),
    notable_features TEXT,
    first_appearance VARCHAR(255),
    wiki_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- G.I. Joe Episodes/Media table
CREATE TABLE gijoe_media (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(100),  -- 'TV Episode', 'Movie', 'Comic', 'Video Game'
    series VARCHAR(255),  -- Which series/comic line
    season INTEGER,
    episode_number INTEGER,
    air_date DATE,
    description TEXT,
    characters_featured TEXT,
    vehicles_featured TEXT,
    wiki_url VARCHAR(500),
    imdb_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_data TEXT
);

-- ================================
-- RELATIONSHIP TABLES
-- ================================

-- Character-Vehicle relationships (many-to-many)
CREATE TABLE character_vehicle_relations (
    id INTEGER PRIMARY KEY,
    character_id INTEGER,
    vehicle_id INTEGER,
    relationship_type VARCHAR(100),  -- 'Primary Pilot', 'Secondary Pilot', 'Driver', 'Gunner'
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
    FOREIGN KEY (vehicle_id) REFERENCES gijoe_vehicles(id),
    UNIQUE(character_id, vehicle_id, relationship_type)
);

-- Character-Weapon relationships (many-to-many)
CREATE TABLE character_weapon_relations (
    id INTEGER PRIMARY KEY,
    character_id INTEGER,
    weapon_id INTEGER,
    relationship_type VARCHAR(100),  -- 'Primary Weapon', 'Secondary Weapon', 'Signature Weapon'
    FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
    FOREIGN KEY (weapon_id) REFERENCES gijoe_weapons(id),
    UNIQUE(character_id, weapon_id, relationship_type)
);

-- ================================
-- INDEXES FOR PERFORMANCE
-- ================================

-- Character indexes
CREATE INDEX idx_characters_name ON gijoe_characters(name);
CREATE INDEX idx_characters_faction ON gijoe_characters(faction);
CREATE INDEX idx_characters_specialty ON gijoe_characters(specialty);
CREATE INDEX idx_characters_status ON gijoe_characters(status);

-- Vehicle indexes
CREATE INDEX idx_vehicles_name ON gijoe_vehicles(name);
CREATE INDEX idx_vehicles_faction ON gijoe_vehicles(faction);
CREATE INDEX idx_vehicles_category ON gijoe_vehicles(category);
CREATE INDEX idx_vehicles_year ON gijoe_vehicles(year_introduced);
CREATE INDEX idx_vehicles_type ON gijoe_vehicles(vehicle_type);

-- Weapon indexes
CREATE INDEX idx_weapons_name ON gijoe_weapons(name);
CREATE INDEX idx_weapons_type ON gijoe_weapons(type);
CREATE INDEX idx_weapons_faction ON gijoe_weapons(faction);

-- Location indexes
CREATE INDEX idx_locations_name ON gijoe_locations(name);
CREATE INDEX idx_locations_type ON gijoe_locations(type);
CREATE INDEX idx_locations_faction ON gijoe_locations(faction);

-- Media indexes
CREATE INDEX idx_media_title ON gijoe_media(title);
CREATE INDEX idx_media_type ON gijoe_media(type);
CREATE INDEX idx_media_series ON gijoe_media(series);
CREATE INDEX idx_media_air_date ON gijoe_media(air_date);

-- Relationship indexes
CREATE INDEX idx_char_veh_relations_char ON character_vehicle_relations(character_id);
CREATE INDEX idx_char_veh_relations_veh ON character_vehicle_relations(vehicle_id);
CREATE INDEX idx_char_weap_relations_char ON character_weapon_relations(character_id);
CREATE INDEX idx_char_weap_relations_weap ON character_weapon_relations(weapon_id);

-- ================================
-- DATABASE SETUP COMPLETE
-- ================================

-- Schema creation completed successfully!
-- For database documentation and field descriptions, see: gijoe_database_documentation.md
