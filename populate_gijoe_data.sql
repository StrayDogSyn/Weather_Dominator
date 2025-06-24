-- Sample G.I. Joe Data Insert Script
-- Insert sample data from G.I. Joe wiki to populate the database

-- Apply the schema first
.read gijoe_database_schema.sql

-- Insert sample G.I. Joe characters
INSERT OR REPLACE INTO gijoe_characters (
    name, real_name, faction, rank, specialty, birthplace, bio, 
    first_appearance, wiki_url, status
) VALUES 
('Duke', 'Conrad S. Hauser', 'G.I. Joe', 'First Sergeant', 'Field Commander', 'St. Louis, Missouri', 
 'Duke is the leader of the G.I. Joe team, known for his tactical expertise and leadership skills.', 
 '1983', 'https://gijoe.fandom.com/wiki/Duke_(RAH)', 'Active'),

('Snake Eyes', 'Classified', 'G.I. Joe', 'Staff Sergeant', 'Commando', 'Classified', 
 'Silent ninja commando and one of the most popular G.I. Joe characters.', 
 '1982', 'https://gijoe.fandom.com/wiki/Snake_Eyes_(RAH)', 'Active'),

('Cobra Commander', 'Classified', 'Cobra', 'Commander', 'Terrorist Leader', 'Unknown', 
 'The ruthless leader of the terrorist organization Cobra, bent on world domination.', 
 '1982', 'https://gijoe.fandom.com/wiki/Cobra_Commander_(RAH)', 'Active'),

('Destro', 'James McCullen Destro XXIV', 'Cobra', 'Weapons Supplier', 'Arms Dealer', 'Scotland', 
 'Leader of M.A.R.S. Industries and Cobra''s primary weapons supplier.', 
 '1983', 'https://gijoe.fandom.com/wiki/Destro_(RAH)', 'Active'),

('Scarlett', 'Shana M. O''Hara', 'G.I. Joe', 'E-5', 'Counter Intelligence', 'Atlanta, Georgia', 
 'Expert in martial arts and crossbow marksmanship, intelligence specialist.', 
 '1982', 'https://gijoe.fandom.com/wiki/Scarlett_(RAH)', 'Active'),

('Storm Shadow', 'Thomas S. Arashikage', 'Cobra', 'Ninja', 'Assassin', 'Japan', 
 'Cobra ninja assassin and rival to Snake Eyes, master of martial arts.', 
 '1984', 'https://gijoe.fandom.com/wiki/Storm_Shadow_(RAH)', 'Active'),

('Roadblock', 'Marvin F. Hinton', 'G.I. Joe', 'Staff Sergeant', 'Heavy Machine Gunner', 'Biloxi, Mississippi', 
 'Heavy weapons specialist known for his strength and cooking skills.', 
 '1984', 'https://gijoe.fandom.com/wiki/Roadblock_(RAH)', 'Active'),

('Baroness', 'Anastasia DeCobray', 'Cobra', 'Intelligence Officer', 'Espionage', 'Transylvania', 
 'Cobra intelligence officer and Destro''s romantic interest.', 
 '1984', 'https://gijoe.fandom.com/wiki/Baroness_(RAH)', 'Active'),

('Flint', 'Dashiell R. Faireborn', 'G.I. Joe', 'Warrant Officer', 'Infantry', 'Wichita, Kansas', 
 'Infantry soldier and Lady Jaye''s romantic interest.', 
 '1985', 'https://gijoe.fandom.com/wiki/Flint_(RAH)', 'Active'),

('Lady Jaye', 'Alison R. Hart-Burnett', 'G.I. Joe', 'E-6', 'Covert Operations', 'Martha''s Vineyard, Massachusetts', 
 'Covert operations specialist skilled in disguise and intelligence gathering.', 
 '1985', 'https://gijoe.fandom.com/wiki/Lady_Jaye_(RAH)', 'Active');

-- Insert sample G.I. Joe vehicles
INSERT OR REPLACE INTO gijoe_vehicles (
    name, year_introduced, faction, category, vehicle_type, description, 
    pilot_driver, crew_capacity, weapons, wiki_url, toy_line
) VALUES 
('VAMP', 1982, 'G.I. Joe', 'Land Vehicle', 'Attack Vehicle', 
 'Versatile Attack Multi-Purpose vehicle, fast reconnaissance vehicle.', 
 'Clutch', 2, '7.62mm machine gun', 
 'https://gijoe.fandom.com/wiki/VAMP', 'A Real American Hero'),

('HISS Tank', 1983, 'Cobra', 'Land Vehicle', 'Tank', 
 'High Speed Sentry tank, Cobra''s primary battle tank.', 
 'HISS Driver', 1, 'Twin laser cannons', 
 'https://gijoe.fandom.com/wiki/HISS_Tank', 'A Real American Hero'),

('Skystriker', 1983, 'G.I. Joe', 'Aircraft', 'Jet Fighter', 
 'XP-14F fighter jet based on the F-14 Tomcat.', 
 'Ace', 1, 'Air-to-air missiles, cannons', 
 'https://gijoe.fandom.com/wiki/Skystriker', 'A Real American Hero'),

('Rattler', 1984, 'Cobra', 'Aircraft', 'Attack Helicopter', 
 'Ground attack helicopter used by Cobra forces.', 
 'Wild Weasel', 1, 'Missiles, machine guns', 
 'https://gijoe.fandom.com/wiki/Rattler', 'A Real American Hero'),

('Mauler M.B.T.', 1985, 'G.I. Joe', 'Land Vehicle', 'Tank', 
 'Main Battle Tank used by G.I. Joe forces.', 
 'Steeler', 2, '120mm cannon, machine guns', 
 'https://gijoe.fandom.com/wiki/Mauler', 'A Real American Hero'),

('Water Moccasin', 1984, 'Cobra', 'Naval', 'Swamp Boat', 
 'Swamp patrol boat for operations in wetland areas.', 
 'Copperhead', 2, 'Twin machine guns', 
 'https://gijoe.fandom.com/wiki/Water_Moccasin', 'A Real American Hero'),

('APC', 1983, 'G.I. Joe', 'Land Vehicle', 'Armored Personnel Carrier', 
 'Armored Personnel Carrier for transporting troops.', 
 'Steeler', 8, 'Machine gun turret', 
 'https://gijoe.fandom.com/wiki/APC_(RAH)', 'A Real American Hero'),

('Night Raven', 1986, 'Cobra', 'Aircraft', 'Stealth Fighter', 
 'Advanced stealth reconnaissance aircraft.', 
 'Strato-Viper', 1, 'Air-to-air missiles', 
 'https://gijoe.fandom.com/wiki/Night_Raven', 'A Real American Hero'),

('Whale', 1984, 'G.I. Joe', 'Naval', 'Hovercraft', 
 'Heavy duty hovercraft for amphibious operations.', 
 'Cutter', 4, 'Twin machine guns, depth charges', 
 'https://gijoe.fandom.com/wiki/Whale', 'A Real American Hero'),

('Thunder Machine', 1986, 'Cobra', 'Land Vehicle', 'Assault Vehicle', 
 'High-speed desert assault vehicle used by Dreadnoks.', 
 'Thrasher', 2, 'Machine guns, ram spikes', 
 'https://gijoe.fandom.com/wiki/Thunder_Machine', 'A Real American Hero');

-- Insert sample weapons
INSERT OR REPLACE INTO gijoe_weapons (
    name, type, faction, description, used_by, first_appearance, wiki_url
) VALUES 
('M-16 Rifle', 'Rifle', 'G.I. Joe', 'Standard assault rifle used by G.I. Joe forces.', 
 'Duke, Flint, multiple characters', '1982', 'https://gijoe.fandom.com/wiki/M-16'),

('Uzi Submachine Gun', 'Submachine Gun', 'G.I. Joe', 'Compact automatic weapon.', 
 'Scarlett, Lady Jaye', '1982', 'https://gijoe.fandom.com/wiki/Uzi'),

('Katana', 'Melee', 'Neutral', 'Traditional Japanese sword.', 
 'Snake Eyes, Storm Shadow', '1982', 'https://gijoe.fandom.com/wiki/Katana'),

('Crossbow', 'Ranged', 'G.I. Joe', 'Silent ranged weapon with explosive bolts.', 
 'Scarlett', '1982', 'https://gijoe.fandom.com/wiki/Crossbow'),

('Laser Rifle', 'Energy Weapon', 'Cobra', 'High-tech energy weapon.', 
 'Cobra Troopers', '1983', 'https://gijoe.fandom.com/wiki/Laser_Rifle');

-- Insert sample locations
INSERT OR REPLACE INTO gijoe_locations (
    name, type, faction, description, location, purpose, wiki_url
) VALUES 
('The Pit', 'Base', 'G.I. Joe', 'Underground headquarters of G.I. Joe.', 
 'Utah, USA', 'Command center and training facility', 
 'https://gijoe.fandom.com/wiki/The_Pit'),

('Cobra Island', 'Island Base', 'Cobra', 'Sovereign nation controlled by Cobra.', 
 'Gulf of Mexico', 'Cobra''s primary headquarters', 
 'https://gijoe.fandom.com/wiki/Cobra_Island'),

('Cobra Temple', 'Base', 'Cobra', 'Ancient temple used as Cobra headquarters.', 
 'Various locations', 'Religious and command center', 
 'https://gijoe.fandom.com/wiki/Cobra_Temple'),

('USS Flagg', 'Mobile Base', 'G.I. Joe', 'Aircraft carrier serving as mobile command.', 
 'International waters', 'Naval operations base', 
 'https://gijoe.fandom.com/wiki/USS_Flagg');

-- Insert character-vehicle relationships
INSERT OR REPLACE INTO character_vehicle_relations (
    character_id, vehicle_id, relationship_type
) VALUES 
((SELECT id FROM gijoe_characters WHERE name = 'Duke'), 
 (SELECT id FROM gijoe_vehicles WHERE name = 'VAMP'), 'Primary Driver'),
 
((SELECT id FROM gijoe_characters WHERE name = 'Cobra Commander'), 
 (SELECT id FROM gijoe_vehicles WHERE name = 'HISS Tank'), 'Primary Driver'),
 
((SELECT id FROM gijoe_characters WHERE name = 'Scarlett'), 
 (SELECT id FROM gijoe_vehicles WHERE name = 'VAMP'), 'Secondary Driver');

-- Insert character-weapon relationships
INSERT OR REPLACE INTO character_weapon_relations (
    character_id, weapon_id, relationship_type
) VALUES 
((SELECT id FROM gijoe_characters WHERE name = 'Duke'), 
 (SELECT id FROM gijoe_weapons WHERE name = 'M-16 Rifle'), 'Primary Weapon'),
 
((SELECT id FROM gijoe_characters WHERE name = 'Scarlett'), 
 (SELECT id FROM gijoe_weapons WHERE name = 'Crossbow'), 'Signature Weapon'),
 
((SELECT id FROM gijoe_characters WHERE name = 'Snake Eyes'), 
 (SELECT id FROM gijoe_weapons WHERE name = 'Katana'), 'Signature Weapon'),
 
((SELECT id FROM gijoe_characters WHERE name = 'Storm Shadow'), 
 (SELECT id FROM gijoe_weapons WHERE name = 'Katana'), 'Primary Weapon');

-- Display summary statistics
SELECT 'Characters by Faction:' as summary;
SELECT faction, COUNT(*) as count FROM gijoe_characters GROUP BY faction;

SELECT 'Vehicles by Faction:' as summary;
SELECT faction, COUNT(*) as count FROM gijoe_vehicles GROUP BY faction;

SELECT 'Vehicles by Category:' as summary;
SELECT category, COUNT(*) as count FROM gijoe_vehicles GROUP BY category;

SELECT 'Total Records:' as summary;
SELECT 
    (SELECT COUNT(*) FROM gijoe_characters) as characters,
    (SELECT COUNT(*) FROM gijoe_vehicles) as vehicles,
    (SELECT COUNT(*) FROM gijoe_weapons) as weapons,
    (SELECT COUNT(*) FROM gijoe_locations) as locations;
