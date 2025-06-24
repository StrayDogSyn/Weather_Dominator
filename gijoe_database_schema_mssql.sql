-- G.I. Joe Database Extension Script for SQL Server (MSSQL)
-- Adds tables for comprehensive G.I. Joe data from gijoe.fandom.com
-- Database Type: SQL Server

-- Create database if it doesn't exist (uncomment if creating new database)
-- IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'WeatherDominatorDB')
-- BEGIN
--     CREATE DATABASE WeatherDominatorDB;
-- END;
-- GO

-- USE WeatherDominatorDB;
-- GO

-- G.I. Joe Characters table (enhanced version of character_lookups)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='gijoe_characters' AND xtype='U')
BEGIN
    CREATE TABLE gijoe_characters (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL UNIQUE,
        real_name NVARCHAR(255),
        code_name NVARCHAR(255),
        faction NVARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Independent', 'Other'
        rank NVARCHAR(100),
        specialty NVARCHAR(255),
        birthplace NVARCHAR(255),
        bio NTEXT,
        first_appearance NVARCHAR(255),
        voice_actor NVARCHAR(255),
        wiki_url NVARCHAR(500),
        image_url NVARCHAR(500),
        status NVARCHAR(50),  -- 'Active', 'Deceased', 'Missing', 'Retired'
        timestamp DATETIME2 DEFAULT GETDATE(),
        raw_data NTEXT  -- JSON string of full character data
    );
END;

-- G.I. Joe Vehicles table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='gijoe_vehicles' AND xtype='U')
BEGIN
    CREATE TABLE gijoe_vehicles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL UNIQUE,
        year_introduced INT,
        faction NVARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Other'
        category NVARCHAR(100),  -- 'Aircraft', 'Land Vehicle', 'Naval', 'Space Vehicle'
        vehicle_type NVARCHAR(100),  -- 'Tank', 'Helicopter', 'Jet', 'Boat', etc.
        description NTEXT,
        pilot_driver NVARCHAR(255),
        crew_capacity INT,
        weapons NTEXT,
        features NTEXT,
        specifications NTEXT,
        wiki_url NVARCHAR(500),
        image_url NVARCHAR(500),
        toy_line NVARCHAR(255),  -- Original toy line it appeared in
        timestamp DATETIME2 DEFAULT GETDATE(),
        raw_data NTEXT  -- JSON string of full vehicle data
    );
END;

-- G.I. Joe Weapons/Equipment table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='gijoe_weapons' AND xtype='U')
BEGIN
    CREATE TABLE gijoe_weapons (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL UNIQUE,
        type NVARCHAR(100),  -- 'Rifle', 'Pistol', 'Launcher', 'Melee', 'Equipment'
        faction NVARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Neutral'
        description NTEXT,
        specifications NTEXT,
        used_by NVARCHAR(500),  -- Characters who commonly use this weapon
        first_appearance NVARCHAR(255),
        wiki_url NVARCHAR(500),
        image_url NVARCHAR(500),
        timestamp DATETIME2 DEFAULT GETDATE(),
        raw_data NTEXT
    );
END;

-- G.I. Joe Locations/Bases table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='gijoe_locations' AND xtype='U')
BEGIN
    CREATE TABLE gijoe_locations (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL UNIQUE,
        type NVARCHAR(100),  -- 'Base', 'City', 'Country', 'Facility', 'Vehicle'
        faction NVARCHAR(50),  -- 'G.I. Joe', 'Cobra', 'Neutral'
        description NTEXT,
        location NVARCHAR(255),  -- Geographic location
        purpose NVARCHAR(255),
        notable_features NTEXT,
        first_appearance NVARCHAR(255),
        wiki_url NVARCHAR(500),
        image_url NVARCHAR(500),
        timestamp DATETIME2 DEFAULT GETDATE(),
        raw_data NTEXT
    );
END;

-- G.I. Joe Episodes/Media table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='gijoe_media' AND xtype='U')
BEGIN
    CREATE TABLE gijoe_media (
        id INT IDENTITY(1,1) PRIMARY KEY,
        title NVARCHAR(255) NOT NULL,
        type NVARCHAR(100),  -- 'TV Episode', 'Movie', 'Comic', 'Video Game'
        series NVARCHAR(255),  -- Which series/comic line
        season INT,
        episode_number INT,
        air_date DATE,
        description NTEXT,
        characters_featured NTEXT,
        vehicles_featured NTEXT,
        wiki_url NVARCHAR(500),
        imdb_url NVARCHAR(500),
        timestamp DATETIME2 DEFAULT GETDATE(),
        raw_data NTEXT
    );
END;

-- Character-Vehicle relationships (many-to-many)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='character_vehicle_relations' AND xtype='U')
BEGIN
    CREATE TABLE character_vehicle_relations (
        id INT IDENTITY(1,1) PRIMARY KEY,
        character_id INT,
        vehicle_id INT,
        relationship_type NVARCHAR(100),  -- 'Primary Pilot', 'Secondary Pilot', 'Driver', 'Gunner'
        FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
        FOREIGN KEY (vehicle_id) REFERENCES gijoe_vehicles(id),
        CONSTRAINT UQ_character_vehicle_relation UNIQUE(character_id, vehicle_id, relationship_type)
    );
END;

-- Character-Weapon relationships (many-to-many)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='character_weapon_relations' AND xtype='U')
BEGIN
    CREATE TABLE character_weapon_relations (
        id INT IDENTITY(1,1) PRIMARY KEY,
        character_id INT,
        weapon_id INT,
        relationship_type NVARCHAR(100),  -- 'Primary Weapon', 'Secondary Weapon', 'Signature Weapon'
        FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
        FOREIGN KEY (weapon_id) REFERENCES gijoe_weapons(id),
        CONSTRAINT UQ_character_weapon_relation UNIQUE(character_id, weapon_id, relationship_type)
    );
END;

-- Create indexes for better performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_characters_name')
    CREATE INDEX idx_characters_name ON gijoe_characters(name);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_characters_faction')
    CREATE INDEX idx_characters_faction ON gijoe_characters(faction);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_characters_specialty')
    CREATE INDEX idx_characters_specialty ON gijoe_characters(specialty);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_vehicles_name')
    CREATE INDEX idx_vehicles_name ON gijoe_vehicles(name);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_vehicles_faction')
    CREATE INDEX idx_vehicles_faction ON gijoe_vehicles(faction);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_vehicles_category')
    CREATE INDEX idx_vehicles_category ON gijoe_vehicles(category);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_vehicles_year')
    CREATE INDEX idx_vehicles_year ON gijoe_vehicles(year_introduced);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_weapons_name')
    CREATE INDEX idx_weapons_name ON gijoe_weapons(name);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_weapons_type')
    CREATE INDEX idx_weapons_type ON gijoe_weapons(type);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_weapons_faction')
    CREATE INDEX idx_weapons_faction ON gijoe_weapons(faction);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_locations_name')
    CREATE INDEX idx_locations_name ON gijoe_locations(name);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_locations_type')
    CREATE INDEX idx_locations_type ON gijoe_locations(type);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_locations_faction')
    CREATE INDEX idx_locations_faction ON gijoe_locations(faction);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_media_title')
    CREATE INDEX idx_media_title ON gijoe_media(title);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_media_type')
    CREATE INDEX idx_media_type ON gijoe_media(type);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_media_series')
    CREATE INDEX idx_media_series ON gijoe_media(series);

-- Views for common queries
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'cobra_characters')
BEGIN
    EXEC('CREATE VIEW cobra_characters AS
    SELECT * FROM gijoe_characters WHERE faction = ''Cobra''');
END;

IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'joe_characters')
BEGIN
    EXEC('CREATE VIEW joe_characters AS
    SELECT * FROM gijoe_characters WHERE faction = ''G.I. Joe''');
END;

IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'cobra_vehicles')
BEGIN
    EXEC('CREATE VIEW cobra_vehicles AS
    SELECT * FROM gijoe_vehicles WHERE faction = ''Cobra''');
END;

IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'joe_vehicles')
BEGIN
    EXEC('CREATE VIEW joe_vehicles AS
    SELECT * FROM gijoe_vehicles WHERE faction = ''G.I. Joe''');
END;

IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'character_vehicle_summary')
BEGIN
    EXEC('CREATE VIEW character_vehicle_summary AS
    SELECT 
        c.name as character_name,
        c.faction as character_faction,
        v.name as vehicle_name,
        v.category as vehicle_category,
        cvr.relationship_type
    FROM gijoe_characters c
    JOIN character_vehicle_relations cvr ON c.id = cvr.character_id
    JOIN gijoe_vehicles v ON v.id = cvr.vehicle_id');
END;

-- Stored procedures for common operations
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'GetCharactersByFaction')
    DROP PROCEDURE GetCharactersByFaction;
GO

CREATE PROCEDURE GetCharactersByFaction
    @faction NVARCHAR(50)
AS
BEGIN
    SELECT * FROM gijoe_characters 
    WHERE faction = @faction
    ORDER BY name;
END;
GO

IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'GetVehiclesByCategory')
    DROP PROCEDURE GetVehiclesByCategory;
GO

CREATE PROCEDURE GetVehiclesByCategory
    @category NVARCHAR(100)
AS
BEGIN
    SELECT * FROM gijoe_vehicles 
    WHERE category = @category
    ORDER BY name;
END;
GO

IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'GetCharacterWeapons')
    DROP PROCEDURE GetCharacterWeapons;
GO

CREATE PROCEDURE GetCharacterWeapons
    @character_name NVARCHAR(255)
AS
BEGIN
    SELECT 
        c.name as character_name,
        w.name as weapon_name,
        w.type as weapon_type,
        cwr.relationship_type
    FROM gijoe_characters c
    JOIN character_weapon_relations cwr ON c.id = cwr.character_id
    JOIN gijoe_weapons w ON w.id = cwr.weapon_id
    WHERE c.name = @character_name
    ORDER BY cwr.relationship_type, w.name;
END;
GO

PRINT 'G.I. Joe database schema (MSSQL) created successfully!';
