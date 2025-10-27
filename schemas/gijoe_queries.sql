-- G.I. Joe Database Query Examples
-- Run with: sqlite3 weather_dominator.db < gijoe_queries.sql

-- Display all characters by faction
SELECT '=== G.I. JOE CHARACTERS ===' as section;
SELECT name, real_name, rank, specialty, birthplace 
FROM gijoe_characters 
WHERE faction = 'G.I. Joe'
ORDER BY name;

SELECT '=== COBRA CHARACTERS ===' as section;
SELECT name, real_name, rank, specialty, birthplace 
FROM gijoe_characters 
WHERE faction = 'Cobra'
ORDER BY name;

-- Display vehicles by category
SELECT '=== LAND VEHICLES ===' as section;
SELECT name, faction, vehicle_type, pilot_driver, weapons
FROM gijoe_vehicles 
WHERE category = 'Land Vehicle'
ORDER BY faction, name;

SELECT '=== AIRCRAFT ===' as section;
SELECT name, faction, vehicle_type, pilot_driver, weapons
FROM gijoe_vehicles 
WHERE category = 'Aircraft'
ORDER BY faction, name;

-- Display character-vehicle relationships
SELECT '=== CHARACTER-VEHICLE RELATIONSHIPS ===' as section;
SELECT 
    c.name as character_name,
    c.faction as character_faction,
    v.name as vehicle_name,
    v.category as vehicle_category,
    cvr.relationship_type
FROM gijoe_characters c
JOIN character_vehicle_relations cvr ON c.id = cvr.character_id
JOIN gijoe_vehicles v ON v.id = cvr.vehicle_id
ORDER BY c.faction, c.name;

-- Display character-weapon relationships
SELECT '=== CHARACTER-WEAPON RELATIONSHIPS ===' as section;
SELECT 
    c.name as character_name,
    c.faction as character_faction,
    w.name as weapon_name,
    w.weapon_type,
    cwr.relationship_type
FROM gijoe_characters c
JOIN character_weapon_relations cwr ON c.id = cwr.character_id
JOIN gijoe_weapons w ON w.id = cwr.weapon_id
ORDER BY c.faction, c.name;

-- Display major bases and locations
SELECT '=== MAJOR BASES AND LOCATIONS ===' as section;
SELECT name, location_type, faction, geographic_location, purpose_function
FROM gijoe_locations
ORDER BY faction, name;

-- Summary statistics
SELECT '=== DATABASE SUMMARY ===' as section;
SELECT 'Total Characters' as category, COUNT(*) as count FROM gijoe_characters
UNION ALL
SELECT 'Total Vehicles' as category, COUNT(*) as count FROM gijoe_vehicles
UNION ALL
SELECT 'Total Weapons' as category, COUNT(*) as count FROM gijoe_weapons
UNION ALL
SELECT 'Total Locations' as category, COUNT(*) as count FROM gijoe_locations
UNION ALL
SELECT 'Character-Vehicle Relations' as category, COUNT(*) as count FROM character_vehicle_relations
UNION ALL
SELECT 'Character-Weapon Relations' as category, COUNT(*) as count FROM character_weapon_relations;
