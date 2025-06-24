#!/usr/bin/env python3
"""
G.I. Joe Database Populator
Applies the G.I. Joe schema and populates the database with sample data
"""

import sqlite3
import json
import os
from datetime import datetime

class GIJoeDBPopulator:
    """Populate Weather Dominator database with G.I. Joe data"""
    
    def __init__(self, db_path: str = "weather_dominator.db"):
        self.db_path = db_path
        print(f"🗃️ Using database: {self.db_path}")
    
    def apply_schema(self):
        """Apply the G.I. Joe database schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                print("📋 Creating G.I. Joe tables...")
                
                # G.I. Joe Characters table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gijoe_characters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        real_name TEXT,
                        code_name TEXT,
                        faction TEXT,
                        rank TEXT,
                        specialty TEXT,
                        birthplace TEXT,
                        bio TEXT,
                        first_appearance TEXT,
                        voice_actor TEXT,
                        wiki_url TEXT,
                        image_url TEXT,
                        status TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        raw_data TEXT
                    )
                """)
                
                # G.I. Joe Vehicles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gijoe_vehicles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        year_introduced INTEGER,
                        faction TEXT,
                        category TEXT,
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
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        raw_data TEXT
                    )
                """)
                
                # G.I. Joe Weapons table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gijoe_weapons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        type TEXT,
                        faction TEXT,
                        description TEXT,
                        specifications TEXT,
                        used_by TEXT,
                        first_appearance TEXT,
                        wiki_url TEXT,
                        image_url TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        raw_data TEXT
                    )
                """)
                
                # G.I. Joe Locations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS gijoe_locations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        type TEXT,
                        faction TEXT,
                        description TEXT,
                        location TEXT,
                        purpose TEXT,
                        notable_features TEXT,
                        first_appearance TEXT,
                        wiki_url TEXT,
                        image_url TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        raw_data TEXT
                    )
                """)
                
                # Character-Vehicle relationships
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS character_vehicle_relations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character_id INTEGER,
                        vehicle_id INTEGER,
                        relationship_type TEXT,
                        FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
                        FOREIGN KEY (vehicle_id) REFERENCES gijoe_vehicles(id),
                        UNIQUE(character_id, vehicle_id, relationship_type)
                    )
                """)
                
                # Character-Weapon relationships
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS character_weapon_relations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        character_id INTEGER,
                        weapon_id INTEGER,
                        relationship_type TEXT,
                        FOREIGN KEY (character_id) REFERENCES gijoe_characters(id),
                        FOREIGN KEY (weapon_id) REFERENCES gijoe_weapons(id),
                        UNIQUE(character_id, weapon_id, relationship_type)
                    )
                """)
                
                # Create indexes
                print("🔍 Creating database indexes...")
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_characters_name ON gijoe_characters(name)",
                    "CREATE INDEX IF NOT EXISTS idx_characters_faction ON gijoe_characters(faction)",
                    "CREATE INDEX IF NOT EXISTS idx_vehicles_name ON gijoe_vehicles(name)",
                    "CREATE INDEX IF NOT EXISTS idx_vehicles_faction ON gijoe_vehicles(faction)",
                    "CREATE INDEX IF NOT EXISTS idx_weapons_name ON gijoe_weapons(name)",
                    "CREATE INDEX IF NOT EXISTS idx_locations_name ON gijoe_locations(name)"
                ]
                
                for index_sql in indexes:
                    cursor.execute(index_sql)
                
                conn.commit()
                print("✅ G.I. Joe schema applied successfully!")
                
        except sqlite3.Error as e:
            print(f"❌ Error applying schema: {e}")
    
    def populate_characters(self):
        """Populate characters table with comprehensive G.I. Joe character data"""
        characters = [
            # G.I. Joe Team Members
            {
                'name': 'Duke',
                'real_name': 'Conrad S. Hauser',
                'code_name': 'Duke',
                'faction': 'G.I. Joe',
                'rank': 'First Sergeant',
                'specialty': 'Field Commander',
                'birthplace': 'St. Louis, Missouri',
                'bio': 'Duke is the field commander of the G.I. Joe team, known for his tactical expertise, leadership skills, and unwavering dedication to the mission. A natural born leader with extensive military training.',
                'first_appearance': '1983',
                'voice_actor': 'Michael Bell',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Duke_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Snake Eyes',
                'real_name': 'Classified',
                'code_name': 'Snake Eyes',
                'faction': 'G.I. Joe',
                'rank': 'Staff Sergeant',
                'specialty': 'Commando',
                'birthplace': 'Classified',
                'bio': 'Silent ninja commando and one of the most popular G.I. Joe characters. Mute due to vocal cord damage, master of martial arts and edged weapons. Sworn brother to Storm Shadow.',
                'first_appearance': '1982',
                'voice_actor': 'None (Silent)',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Snake_Eyes_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Scarlett',
                'real_name': 'Shana M. O\'Hara',
                'code_name': 'Scarlett',
                'faction': 'G.I. Joe',
                'rank': 'E-5 Sergeant',
                'specialty': 'Counter Intelligence',
                'birthplace': 'Atlanta, Georgia',
                'bio': 'Expert in martial arts and crossbow marksmanship, intelligence specialist. One of the original G.I. Joe team members and often serves as second-in-command.',
                'first_appearance': '1982',
                'voice_actor': 'B.J. Ward',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Scarlett_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Roadblock',
                'real_name': 'Marvin F. Hinton',
                'code_name': 'Roadblock',
                'faction': 'G.I. Joe',
                'rank': 'Staff Sergeant',
                'specialty': 'Heavy Machine Gunner',
                'birthplace': 'Biloxi, Mississippi',
                'bio': 'Heavy weapons specialist known for his strength, cooking skills, and ability to speak in rhymes. Expert with heavy machine guns and anti-tank weapons.',
                'first_appearance': '1984',
                'voice_actor': 'Kene Holliday',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Roadblock_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Flint',
                'real_name': 'Dashiell R. Faireborn',
                'code_name': 'Flint',
                'faction': 'G.I. Joe',
                'rank': 'Warrant Officer',
                'specialty': 'Infantry',
                'birthplace': 'Wichita, Kansas',
                'bio': 'Infantry specialist and tactician, often partners with Lady Jaye. Expert in small unit tactics and survival training.',
                'first_appearance': '1985',
                'voice_actor': 'Bill Ratner',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Flint_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Lady Jaye',
                'real_name': 'Alison R. Hart-Burnett',
                'code_name': 'Lady Jaye',
                'faction': 'G.I. Joe',
                'rank': 'Captain',
                'specialty': 'Covert Operations',
                'birthplace': 'Martha\'s Vineyard, Massachusetts',
                'bio': 'Intelligence officer specializing in covert operations and infiltration. Expert in multiple languages and disguise techniques.',
                'first_appearance': '1985',
                'voice_actor': 'Mary McDonald-Lewis',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Lady_Jaye_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Shipwreck',
                'real_name': 'Hector X. Delgado',
                'code_name': 'Shipwreck',
                'faction': 'G.I. Joe',
                'rank': 'Petty Officer First Class',
                'specialty': 'Naval Intelligence',
                'birthplace': 'Chula Vista, California',
                'bio': 'Navy specialist and seaman, known for his sailor\'s mouth and his pet parrot Polly. Expert in naval operations and underwater combat.',
                'first_appearance': '1985',
                'voice_actor': 'Neil Ross',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Shipwreck_(RAH)',
                'status': 'Active'
            },
            # Cobra Forces
            {
                'name': 'Cobra Commander',
                'real_name': 'Classified',
                'code_name': 'Cobra Commander',
                'faction': 'Cobra',
                'rank': 'Supreme Commander',
                'specialty': 'Terrorist Leader',
                'birthplace': 'Unknown',
                'bio': 'The ruthless and megalomaniacal leader of the terrorist organization Cobra, bent on world domination. Known for his distinctive helmet and serpentine hiss.',
                'first_appearance': '1982',
                'voice_actor': 'Chris Latta',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Cobra_Commander_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Destro',
                'real_name': 'James McCullen Destro XXIV',
                'code_name': 'Destro',
                'faction': 'Cobra',
                'rank': 'Weapons Supplier',
                'specialty': 'Arms Dealer',
                'birthplace': 'Callander, Scotland',
                'bio': 'Leader of M.A.R.S. Industries and Cobra\'s primary weapons supplier. Wears an ancestral metal mask and maintains a code of honor despite his villainous nature.',
                'first_appearance': '1983',
                'voice_actor': 'Arthur Burghardt',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Destro_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Baroness',
                'real_name': 'Anastasia DeCobray',
                'code_name': 'Baroness',
                'faction': 'Cobra',
                'rank': 'Intelligence Officer',
                'specialty': 'Espionage',
                'birthplace': 'Transylvania, Romania',
                'bio': 'Cobra intelligence officer and Destro\'s romantic interest. Expert in espionage, sabotage, and psychological warfare. Known for her distinctive glasses and leather outfit.',
                'first_appearance': '1984',
                'voice_actor': 'Morgan Lofting',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Baroness_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Storm Shadow',
                'real_name': 'Thomas S. Arashikage',
                'code_name': 'Storm Shadow',
                'faction': 'Cobra',
                'rank': 'Ninja Assassin',
                'specialty': 'Assassin',
                'birthplace': 'Tokyo, Japan',
                'bio': 'Cobra ninja assassin and rival to Snake Eyes, though they were once sworn brothers. Master of martial arts and traditional ninja weapons.',
                'first_appearance': '1984',
                'voice_actor': 'Keone Young',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Storm_Shadow_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Zartan',
                'real_name': 'Unknown',
                'code_name': 'Zartan',
                'faction': 'Cobra',
                'rank': 'Master of Disguise',
                'specialty': 'Assassin/Saboteur',
                'birthplace': 'Unknown',
                'bio': 'Master of disguise and leader of the Dreadnoks. Ability to change skin color like a chameleon and expert in ventriloquism and mimicry.',
                'first_appearance': '1984',
                'voice_actor': 'Zack Hoffman',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Zartan_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Dr. Mindbender',
                'real_name': 'Dr. Sidney Biggles-Jones',
                'code_name': 'Dr. Mindbender',
                'faction': 'Cobra',
                'rank': 'Master of Mind Control',
                'specialty': 'Brainwashing',
                'birthplace': 'Australian Outback',
                'bio': 'Cobra\'s chief scientist and expert in brainwashing and mind control. Former orthodontist turned evil genius.',
                'first_appearance': '1986',
                'voice_actor': 'Frank Welker',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Dr._Mindbender_(RAH)',
                'status': 'Active'
            },
            {
                'name': 'Major Bludd',
                'real_name': 'Sebastian Bludd',
                'code_name': 'Major Bludd',
                'faction': 'Cobra',
                'rank': 'Major',
                'specialty': 'Mercenary',
                'birthplace': 'Sydney, Australia',
                'bio': 'Mercenary soldier and poet who works for Cobra. Expert in guerrilla warfare and known for his military expertise and distinctive accent.',
                'first_appearance': '1983',
                'voice_actor': 'Bill Ratner',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Major_Bludd_(RAH)',
                'status': 'Active'
            }
        ]
        
        self._insert_data('gijoe_characters', characters, "characters")
    
    def populate_vehicles(self):
        """Populate vehicles table with comprehensive G.I. Joe vehicle data"""
        vehicles = [
            # G.I. Joe Land Vehicles
            {
                'name': 'VAMP',
                'year_introduced': 1982,
                'faction': 'G.I. Joe',
                'category': 'Land Vehicle',
                'vehicle_type': 'Attack Vehicle',
                'description': 'Versatile Attack Multi-Purpose vehicle, fast reconnaissance and assault vehicle.',
                'pilot_driver': 'Clutch',
                'crew_capacity': 2,
                'weapons': '7.62mm machine gun, optional missile pod',
                'features': 'Roll cage, all-terrain capability, speed 65 mph',
                'specifications': 'Length: 11 feet, Weight: 2.5 tons',
                'wiki_url': 'https://gijoe.fandom.com/wiki/VAMP',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Wolverine',
                'year_introduced': 1983,
                'faction': 'G.I. Joe',
                'category': 'Land Vehicle',
                'vehicle_type': 'Armored Fighting Vehicle',
                'description': 'Armored missile tank with twin missile launchers.',
                'pilot_driver': 'Cover Girl',
                'crew_capacity': 1,
                'weapons': 'Twin missile launchers, machine gun',
                'features': 'Heavy armor, tracked mobility',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Wolverine',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Mauler M.B.T.',
                'year_introduced': 1985,
                'faction': 'G.I. Joe',
                'category': 'Land Vehicle',
                'vehicle_type': 'Main Battle Tank',
                'description': 'Main battle tank with rotating turret and heavy armor.',
                'pilot_driver': 'Heavy Metal',
                'crew_capacity': 2,
                'weapons': '120mm main gun, coaxial machine gun',
                'features': 'Composite armor, night vision',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Mauler_M.B.T.',
                'toy_line': 'A Real American Hero'
            },
            # G.I. Joe Aircraft
            {
                'name': 'Skystriker',
                'year_introduced': 1983,
                'faction': 'G.I. Joe',
                'category': 'Aircraft',
                'vehicle_type': 'Fighter Jet',
                'description': 'XP-14F fighter jet based on the F-14 Tomcat, primary air superiority fighter.',
                'pilot_driver': 'Ace',
                'crew_capacity': 1,
                'weapons': 'Air-to-air missiles, 20mm cannon, bombs',
                'features': 'Variable-sweep wings, afterburners, ejection seat',
                'specifications': 'Max speed: Mach 2.3, Range: 2000 miles',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Skystriker',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Dragonfly',
                'year_introduced': 1983,
                'faction': 'G.I. Joe',
                'category': 'Aircraft',
                'vehicle_type': 'Helicopter',
                'description': 'XH-1 helicopter gunship for close air support and transport.',
                'pilot_driver': 'Wild Bill',
                'crew_capacity': 3,
                'weapons': 'Chain gun, rocket pods, door guns',
                'features': 'Night vision, rescue winch',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Dragonfly',
                'toy_line': 'A Real American Hero'
            },
            # Cobra Vehicles
            {
                'name': 'HISS Tank',
                'year_introduced': 1983,
                'faction': 'Cobra',
                'category': 'Land Vehicle',
                'vehicle_type': 'Tank',
                'description': 'High Speed Sentry tank, Cobra\'s primary battle tank with distinctive design.',
                'pilot_driver': 'HISS Driver',
                'crew_capacity': 1,
                'weapons': 'Twin laser cannons, machine guns',
                'features': 'High speed, stealth coating, advanced targeting',
                'specifications': 'Top speed: 80 mph, Armor: Composite',
                'wiki_url': 'https://gijoe.fandom.com/wiki/HISS_Tank',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Rattler',
                'year_introduced': 1984,
                'faction': 'Cobra',
                'category': 'Aircraft',
                'vehicle_type': 'Attack Aircraft',
                'description': 'Ground attack aircraft designed for close air support missions.',
                'pilot_driver': 'Wild Weasel',
                'crew_capacity': 1,
                'weapons': 'Missiles, bombs, nose cannon',
                'features': 'VTOL capability, armored cockpit',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Rattler',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'FANG',
                'year_introduced': 1983,
                'faction': 'Cobra',
                'category': 'Aircraft',
                'vehicle_type': 'Helicopter',
                'description': 'Fully Armed Negator Gyrocopter, one-man attack helicopter.',
                'pilot_driver': 'Cobra Pilot',
                'crew_capacity': 1,
                'weapons': 'Twin machine guns, missiles',
                'features': 'Gyrocopter design, high maneuverability',
                'wiki_url': 'https://gijoe.fandom.com/wiki/FANG',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Water Moccasin',
                'year_introduced': 1984,
                'faction': 'Cobra',
                'category': 'Naval',
                'vehicle_type': 'Swamp Boat',
                'description': 'Swamp patrol boat optimized for operations in wetland environments.',
                'pilot_driver': 'Copperhead',
                'crew_capacity': 2,
                'weapons': 'Twin machine guns, depth charges',
                'features': 'Shallow draft, silent running mode',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Water_Moccasin',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Stinger',
                'year_introduced': 1984,
                'faction': 'Cobra',
                'category': 'Land Vehicle',
                'vehicle_type': 'Jeep',
                'description': 'Fast attack vehicle for reconnaissance and hit-and-run tactics.',
                'pilot_driver': 'Cobra Officer',
                'crew_capacity': 2,
                'weapons': 'Machine gun, missile launcher',
                'features': 'High speed, off-road capability',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Stinger',
                'toy_line': 'A Real American Hero'
            },
            # Large Vehicles and Bases
            {
                'name': 'USS Flagg',
                'year_introduced': 1985,
                'faction': 'G.I. Joe',
                'category': 'Naval',
                'vehicle_type': 'Aircraft Carrier',
                'description': 'Massive aircraft carrier serving as mobile command base.',
                'pilot_driver': 'Keel Haul',
                'crew_capacity': 1000,
                'weapons': 'Defensive missile systems, deck guns',
                'features': 'Flight deck, command center, hangar bay',
                'specifications': 'Length: 7.5 feet (toy), Crew: 1000+',
                'wiki_url': 'https://gijoe.fandom.com/wiki/USS_Flagg',
                'toy_line': 'A Real American Hero'
            },
            {
                'name': 'Terrordrome',
                'year_introduced': 1986,
                'faction': 'Cobra',
                'category': 'Land Vehicle',
                'vehicle_type': 'Mobile Base',
                'description': 'Cobra\'s massive mobile command fortress and weapons platform.',
                'pilot_driver': 'Cobra Commander',
                'crew_capacity': 50,
                'weapons': 'Multiple missile batteries, laser cannons',
                'features': 'Command center, vehicle bay, communications array',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Terrordrome',
                'toy_line': 'A Real American Hero'
            }
        ]
        
        self._insert_data('gijoe_vehicles', vehicles, "vehicles")
    
    def populate_weapons(self):
        """Populate weapons table with comprehensive G.I. Joe weapons data"""
        weapons = [
            # G.I. Joe Weapons
            {
                'name': 'M-16 Rifle',
                'type': 'Assault Rifle',
                'faction': 'G.I. Joe',
                'description': 'Standard assault rifle used by G.I. Joe forces. Reliable and versatile weapon.',
                'specifications': 'Caliber: 5.56mm, Rate of fire: 700-950 rounds/min',
                'used_by': 'Duke, Flint, Multiple G.I. Joe members',
                'first_appearance': '1982',
                'wiki_url': 'https://gijoe.fandom.com/wiki/M-16'
            },
            {
                'name': 'Crossbow',
                'type': 'Ranged Weapon',
                'faction': 'G.I. Joe',
                'description': 'Silent ranged weapon with explosive and standard bolts. Scarlett\'s signature weapon.',
                'specifications': 'Draw weight: 150 lbs, Effective range: 200 yards',
                'used_by': 'Scarlett',
                'first_appearance': '1982',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Crossbow'
            },
            {
                'name': 'Katana',
                'type': 'Melee Weapon',
                'faction': 'Neutral',
                'description': 'Traditional Japanese sword used by ninja operatives.',
                'specifications': 'Blade length: 28 inches, Steel: High carbon',
                'used_by': 'Snake Eyes, Storm Shadow',
                'first_appearance': '1982',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Katana'
            },
            {
                'name': 'M2 Browning',
                'type': 'Heavy Machine Gun',
                'faction': 'G.I. Joe',
                'description': 'Heavy machine gun used by Roadblock and mounted on vehicles.',
                'specifications': 'Caliber: .50 BMG, Rate of fire: 450-575 rounds/min',
                'used_by': 'Roadblock, Heavy Metal',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/M2_Browning'
            },
            {
                'name': 'Javelin Missiles',
                'type': 'Missile System',
                'faction': 'G.I. Joe',
                'description': 'Shoulder-fired anti-tank missiles used by G.I. Joe forces.',
                'specifications': 'Range: 4.75 km, Warhead: HEAT',
                'used_by': 'Bazooka, Multiple specialists',
                'first_appearance': '1985',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Javelin_Missile'
            },
            # Cobra Weapons
            {
                'name': 'Laser Rifle',
                'type': 'Energy Weapon',
                'faction': 'Cobra',
                'description': 'High-tech energy weapon used by Cobra forces.',
                'specifications': 'Power source: Plasma cell, Range: 500 meters',
                'used_by': 'Cobra Troopers, Cobra Officers',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Laser_Rifle'
            },
            {
                'name': 'Cobra Battle Helmet',
                'type': 'Protective Gear',
                'faction': 'Cobra',
                'description': 'Standard battle helmet worn by Cobra troopers.',
                'specifications': 'Material: Composite armor, Features: HUD display',
                'used_by': 'Cobra Troopers',
                'first_appearance': '1982',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Cobra_Battle_Helmet'
            },
            {
                'name': 'Chain Gun',
                'type': 'Automatic Weapon',
                'faction': 'Cobra',
                'description': 'Externally powered automatic gun used on Cobra vehicles.',
                'specifications': 'Caliber: 25mm, Rate of fire: 625 rounds/min',
                'used_by': 'Vehicle crews, Wild Weasel',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Chain_Gun'
            },
            {
                'name': 'Destro\'s Beretta',
                'type': 'Pistol',
                'faction': 'Cobra',
                'description': 'Modified Beretta pistol used by Destro as his sidearm.',
                'specifications': 'Caliber: 9mm, Custom modifications: Gold plating',
                'used_by': 'Destro',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Destro_Beretta'
            },
            # Specialized Equipment
            {
                'name': 'Night Vision Goggles',
                'type': 'Optical Equipment',
                'faction': 'Both',
                'description': 'Standard night vision equipment used by both factions.',
                'specifications': 'Generation: III, Range: 300 meters',
                'used_by': 'Multiple operatives',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Night_Vision'
            },
            {
                'name': 'Grappling Hook',
                'type': 'Utility Equipment',
                'faction': 'G.I. Joe',
                'description': 'Climbing and infiltration tool used by special operatives.',
                'specifications': 'Range: 50 feet, Weight capacity: 300 lbs',
                'used_by': 'Snake Eyes, Alpine, multiple operatives',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Grappling_Hook'
            },
            {
                'name': 'Throwing Stars',
                'type': 'Projectile Weapon',
                'faction': 'Neutral',
                'description': 'Traditional ninja throwing weapons used by martial arts specialists.',
                'specifications': 'Material: Tempered steel, Points: 4-8',
                'used_by': 'Snake Eyes, Storm Shadow, Jinx',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Throwing_Stars'
            }
        ]
        
        self._insert_data('gijoe_weapons', weapons, "weapons")
    
    def populate_locations(self):
        """Populate locations table with comprehensive G.I. Joe locations data"""
        locations = [
            # G.I. Joe Bases
            {
                'name': 'The Pit',
                'type': 'Underground Base',
                'faction': 'G.I. Joe',
                'description': 'Underground headquarters of G.I. Joe located in the Utah desert. Multi-level facility with training areas, vehicle bays, and command centers.',
                'location': 'Utah Desert, USA',
                'purpose': 'Primary command center, training facility, and vehicle storage',
                'notable_features': 'Underground hangar, training simulator, medical bay, communications center',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/The_Pit'
            },
            {
                'name': 'USS Flagg',
                'type': 'Mobile Naval Base',
                'faction': 'G.I. Joe',
                'description': 'Massive aircraft carrier serving as G.I. Joe\'s mobile command center and primary naval base.',
                'location': 'International Waters',
                'purpose': 'Naval operations base, mobile command center, aircraft carrier',
                'notable_features': 'Flight deck, command bridge, hangar bay, crew quarters for 1000+',
                'first_appearance': '1985',
                'wiki_url': 'https://gijoe.fandom.com/wiki/USS_Flagg'
            },
            {
                'name': 'Headquarters Command Center',
                'type': 'Command Facility',
                'faction': 'G.I. Joe',
                'description': 'Above-ground command facility that serves as the administrative center for G.I. Joe operations.',
                'location': 'Classified Location, USA',
                'purpose': 'Administrative headquarters, mission planning, intelligence analysis',
                'notable_features': 'War room, communications array, briefing rooms',
                'first_appearance': '1982',
                'wiki_url': 'https://gijoe.fandom.com/wiki/GI_Joe_Headquarters'
            },
            # Cobra Facilities
            {
                'name': 'Cobra Island',
                'type': 'Island Nation',
                'faction': 'Cobra',
                'description': 'Sovereign island nation controlled by Cobra, serving as their primary headquarters and stronghold.',
                'location': 'Gulf of Mexico',
                'purpose': 'Cobra headquarters, weapons manufacturing, training facilities',
                'notable_features': 'Terrordrome, airfields, harbor facilities, industrial complexes',
                'first_appearance': '1986',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Cobra_Island'
            },
            {
                'name': 'Cobra Temple',
                'type': 'Ancient Temple Complex',
                'faction': 'Cobra',
                'description': 'Ancient temple complex used by Cobra as a secret base and ceremonial site.',
                'location': 'Various jungle locations',
                'purpose': 'Secret base, ceremonial site, weapons storage',
                'notable_features': 'Hidden passages, ancient architecture, defensive systems',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Cobra_Temple'
            },
            {
                'name': 'Extensive Enterprises',
                'type': 'Corporate Headquarters',
                'faction': 'Cobra',
                'description': 'Cobra Commander\'s legitimate business front and secret operational base.',
                'location': 'Springfield, USA',
                'purpose': 'Corporate front, money laundering, recruitment center',
                'notable_features': 'Executive offices, hidden laboratories, underground facilities',
                'first_appearance': '1985',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Extensive_Enterprises'
            },
            # M.A.R.S. Facilities
            {
                'name': 'Castle Destro',
                'type': 'Ancestral Castle',
                'faction': 'M.A.R.S./Cobra',
                'description': 'Destro\'s ancestral castle in Scotland, serving as M.A.R.S. Industries headquarters.',
                'location': 'Scottish Highlands',
                'purpose': 'M.A.R.S. headquarters, weapons development, Destro\'s residence',
                'notable_features': 'Ancient architecture, modern laboratories, weapons testing facilities',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Castle_Destro'
            },
            {
                'name': 'M.A.R.S. Industries',
                'type': 'Weapons Manufacturing',
                'faction': 'M.A.R.S./Cobra',
                'description': 'Global weapons manufacturing corporation owned by Destro\'s family.',
                'location': 'Multiple international locations',
                'purpose': 'Weapons research, development, and manufacturing',
                'notable_features': 'Advanced laboratories, testing ranges, manufacturing plants',
                'first_appearance': '1983',
                'wiki_url': 'https://gijoe.fandom.com/wiki/MARS_Industries'
            },
            # Other Notable Locations
            {
                'name': 'Arashikage Dojo',
                'type': 'Training Facility',
                'faction': 'Independent',
                'description': 'Traditional ninja training facility where Snake Eyes and Storm Shadow learned their skills.',
                'location': 'Japan',
                'purpose': 'Martial arts training, ninja education, spiritual development',
                'notable_features': 'Traditional architecture, training grounds, meditation gardens',
                'first_appearance': '1984',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Arashikage_Dojo'
            },
            {
                'name': 'Silent Castle',
                'type': 'Secret Facility',
                'faction': 'Cobra',
                'description': 'Cobra\'s secret mountain fortress used for special operations and prisoner detention.',
                'location': 'Trans-Carpathian Mountains',
                'purpose': 'Secret operations base, prisoner facility, weapons storage',
                'notable_features': 'Mountain fortification, dungeons, hidden entrances',
                'first_appearance': '1985',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Silent_Castle'
            },
            {
                'name': 'Benzheen',
                'type': 'Oil-Rich Nation',
                'faction': 'Independent',
                'description': 'Oil-rich Middle Eastern nation often caught between G.I. Joe and Cobra conflicts.',
                'location': 'Middle East',
                'purpose': 'Oil production, strategic location, frequent battleground',
                'notable_features': 'Oil fields, royal palace, strategic importance',
                'first_appearance': '1985',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Benzheen'
            },
            {
                'name': 'Millville',
                'type': 'Small Town',
                'faction': 'Cobra-controlled',
                'description': 'Small American town secretly controlled by Cobra as a recruitment and indoctrination center.',
                'location': 'USA (various states)',
                'purpose': 'Recruitment center, indoctrination facility, civilian cover',
                'notable_features': 'Seemingly normal town, hidden Cobra facilities, brainwashed residents',
                'first_appearance': '1986',
                'wiki_url': 'https://gijoe.fandom.com/wiki/Millville'
            }
        ]
        
        self._insert_data('gijoe_locations', locations, "locations")
    
    def _insert_data(self, table_name: str, data_list: list, data_type: str):
        """Generic method to insert data into tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                inserted_count = 0
                for item in data_list:
                    try:
                        # Build dynamic INSERT statement
                        columns = list(item.keys())
                        placeholders = ', '.join(['?' for _ in columns])
                        values = [item[col] for col in columns]
                        
                        sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(columns)}, raw_data) VALUES ({placeholders}, ?)"
                        values.append(json.dumps(item))
                        
                        cursor.execute(sql, values)
                        inserted_count += 1
                        
                    except sqlite3.Error as e:
                        print(f"❌ Error inserting {item.get('name', 'unknown')}: {e}")
                
                conn.commit()
                print(f"✅ Inserted {inserted_count} {data_type}")
                
        except sqlite3.Error as e:
            print(f"❌ Database error inserting {data_type}: {e}")
    
    def create_relationships(self):
        """Create character-vehicle and character-weapon relationships"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Character-Vehicle relationships
                relationships = [
                    ('Duke', 'VAMP', 'Primary Driver'),
                    ('Cobra Commander', 'HISS Tank', 'Primary Driver'),
                    ('Scarlett', 'VAMP', 'Secondary Driver')
                ]
                
                for char_name, vehicle_name, relationship in relationships:
                    cursor.execute("""
                        INSERT OR REPLACE INTO character_vehicle_relations 
                        (character_id, vehicle_id, relationship_type)
                        VALUES (
                            (SELECT id FROM gijoe_characters WHERE name = ?),
                            (SELECT id FROM gijoe_vehicles WHERE name = ?),
                            ?
                        )
                    """, (char_name, vehicle_name, relationship))
                
                # Character-Weapon relationships
                weapon_relationships = [
                    ('Duke', 'M-16 Rifle', 'Primary Weapon'),
                    ('Scarlett', 'Crossbow', 'Signature Weapon'),
                    ('Snake Eyes', 'Katana', 'Signature Weapon'),
                    ('Storm Shadow', 'Katana', 'Primary Weapon')
                ]
                
                for char_name, weapon_name, relationship in weapon_relationships:
                    cursor.execute("""
                        INSERT OR REPLACE INTO character_weapon_relations 
                        (character_id, weapon_id, relationship_type)
                        VALUES (
                            (SELECT id FROM gijoe_characters WHERE name = ?),
                            (SELECT id FROM gijoe_weapons WHERE name = ?),
                            ?
                        )
                    """, (char_name, weapon_name, relationship))
                
                conn.commit()
                print("✅ Created character relationships")
                
        except sqlite3.Error as e:
            print(f"❌ Error creating relationships: {e}")
    
    def get_database_stats(self):
        """Display database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                print("\n📊 G.I. Joe Database Statistics:")
                
                # Characters by faction
                cursor.execute("SELECT faction, COUNT(*) FROM gijoe_characters GROUP BY faction")
                char_stats = cursor.fetchall()
                print("   Characters by Faction:")
                for faction, count in char_stats:
                    print(f"     {faction}: {count}")
                
                # Vehicles by faction
                cursor.execute("SELECT faction, COUNT(*) FROM gijoe_vehicles GROUP BY faction")
                vehicle_stats = cursor.fetchall()
                print("   Vehicles by Faction:")
                for faction, count in vehicle_stats:
                    print(f"     {faction}: {count}")
                
                # Total counts
                cursor.execute("SELECT COUNT(*) FROM gijoe_characters")
                char_total = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM gijoe_vehicles")
                vehicle_total = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM gijoe_weapons")
                weapon_total = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM gijoe_locations")
                location_total = cursor.fetchone()[0]
                
                print(f"\n   Total Records:")
                print(f"     Characters: {char_total}")
                print(f"     Vehicles: {vehicle_total}")
                print(f"     Weapons: {weapon_total}")
                print(f"     Locations: {location_total}")
                
        except sqlite3.Error as e:
            print(f"❌ Error getting statistics: {e}")
    
    def run_full_population(self):
        """Run complete database population"""
        print("🚀 Starting G.I. Joe database population...")
        
        self.apply_schema()
        self.populate_characters()
        self.populate_vehicles()
        self.populate_weapons()
        self.populate_locations()
        self.create_relationships()
        
        print("\n✅ G.I. Joe database population complete!")
        self.get_database_stats()


if __name__ == "__main__":
    populator = GIJoeDBPopulator()
    
    print("G.I. Joe Database Populator")
    print("1. Run full population")
    print("2. Apply schema only")
    print("3. Show database stats")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        populator.run_full_population()
    elif choice == "2":
        populator.apply_schema()
    elif choice == "3":
        populator.get_database_stats()
    else:
        print("Goodbye!")
