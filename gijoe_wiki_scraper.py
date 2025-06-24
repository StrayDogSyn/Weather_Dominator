#!/usr/bin/env python3
"""
G.I. Joe Fandom Wiki Data Scraper
Scrapes character, vehicle, and other data from gijoe.fandom.com
and populates the Weather Dominator database
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import time
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import os

class GIJoeWikiScraper:
    """Scraper for G.I. Joe Fandom Wiki data"""
    
    def __init__(self, db_path: str = "weather_dominator.db"):
        self.db_path = db_path
        self.base_url = "https://gijoe.fandom.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize database with G.I. Joe schema
        self.init_gijoe_tables()
        
        # Lists of known pages to scrape
        self.vehicle_list_urls = [
            "/wiki/List_of_G.I._Joe:_A_Real_American_Hero_vehicles",
            "/wiki/Category:G.I._Joe_vehicles",
            "/wiki/Category:Cobra_vehicles"
        ]
        
        self.character_list_urls = [
            "/wiki/List_of_G.I._Joe:_A_Real_American_Hero_characters",
            "/wiki/Category:G.I._Joe_characters",
            "/wiki/Category:Cobra_characters"
        ]
    
    def init_gijoe_tables(self):
        """Initialize G.I. Joe database tables"""
        try:
            # Read and execute the SQL schema
            schema_path = "gijoe_database_schema.sql"
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    # Execute each statement separately
                    statements = schema_sql.split(';')
                    for statement in statements:
                        statement = statement.strip()
                        if statement:
                            cursor.execute(statement)
                    conn.commit()
                    print("✅ G.I. Joe database schema initialized")
            else:
                print("⚠️ Schema file not found, creating basic tables")
                self.create_basic_tables()
                
        except Exception as e:
            print(f"❌ Error initializing G.I. Joe tables: {e}")
    
    def create_basic_tables(self):
        """Create basic G.I. Joe tables if schema file is missing"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Basic characters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gijoe_characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    real_name TEXT,
                    faction TEXT,
                    specialty TEXT,
                    bio TEXT,
                    wiki_url TEXT,
                    image_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    raw_data TEXT
                )
            """)
            
            # Basic vehicles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gijoe_vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    year_introduced INTEGER,
                    faction TEXT,
                    category TEXT,
                    description TEXT,
                    pilot_driver TEXT,
                    wiki_url TEXT,
                    image_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    raw_data TEXT
                )
            """)
            
            conn.commit()
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a wiki page"""
        try:
            if not url.startswith('http'):
                url = self.base_url + url
            
            print(f"📄 Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            time.sleep(1)  # Be respectful to the server
            return soup
            
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def scrape_vehicle_list_page(self) -> List[Dict[str, Any]]:
        """Scrape the main vehicles list page"""
        vehicles = []
        
        soup = self.get_page_content("/wiki/List_of_G.I._Joe:_A_Real_American_Hero_vehicles")
        if not soup:
            return vehicles
        
        # Find vehicle tables
        tables = soup.find_all('table', class_='wikitable')
        
        for table in tables:
            # Look for table headers to determine if this is a vehicle table
            headers = table.find('tr')
            if not headers:
                continue
            
            header_texts = [th.get_text().strip().lower() for th in headers.find_all(['th', 'td'])]
            
            # Check if this looks like a vehicle table
            if any(keyword in ' '.join(header_texts) for keyword in ['vehicle', 'name', 'year', 'pilot', 'driver']):
                vehicles.extend(self.parse_vehicle_table(table))
        
        return vehicles
    
    def parse_vehicle_table(self, table) -> List[Dict[str, Any]]:
        """Parse a vehicle table from the wiki"""
        vehicles = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            
            vehicle_data = {}
            
            # Extract basic info from first few cells
            name_cell = cells[0]
            vehicle_data['name'] = self.clean_text(name_cell.get_text())
            
            # Look for links to individual vehicle pages
            link = name_cell.find('a', href=True)
            if link:
                vehicle_data['wiki_url'] = urljoin(self.base_url, link['href'])
            
            # Try to extract year from second cell if it looks like a year
            if len(cells) > 1:
                year_text = self.clean_text(cells[1].get_text())
                year_match = re.search(r'(19|20)\d{2}', year_text)
                if year_match:
                    vehicle_data['year_introduced'] = int(year_match.group())
            
            # Extract pilot/driver info from appropriate cell
            if len(cells) > 2:
                pilot_text = self.clean_text(cells[2].get_text())
                if pilot_text and pilot_text != '-':
                    vehicle_data['pilot_driver'] = pilot_text
            
            # Determine faction based on page section or table context
            page_text = str(table.parent).lower()
            if 'cobra' in page_text:
                vehicle_data['faction'] = 'Cobra'
            elif 'joe' in page_text or 'g.i.' in page_text:
                vehicle_data['faction'] = 'G.I. Joe'
            else:
                vehicle_data['faction'] = 'Unknown'
            
            if vehicle_data['name']:
                vehicles.append(vehicle_data)
        
        return vehicles
    
    def scrape_character_list_page(self) -> List[Dict[str, Any]]:
        """Scrape character list pages"""
        characters = []
        
        soup = self.get_page_content("/wiki/List_of_G.I._Joe:_A_Real_American_Hero_characters")
        if not soup:
            return characters
        
        # Find character tables and lists
        tables = soup.find_all('table', class_='wikitable')
        
        for table in tables:
            characters.extend(self.parse_character_table(table))
        
        # Also look for character lists in sections
        sections = soup.find_all(['h2', 'h3'])
        for section in sections:
            section_text = section.get_text().lower()
            if 'character' in section_text:
                # Find lists in this section
                next_element = section.find_next_sibling()
                while next_element and next_element.name not in ['h1', 'h2', 'h3']:
                    if next_element.name == 'ul':
                        characters.extend(self.parse_character_list(next_element, section_text))
                    next_element = next_element.find_next_sibling()
        
        return characters
    
    def parse_character_table(self, table) -> List[Dict[str, Any]]:
        """Parse a character table from the wiki"""
        characters = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            
            character_data = {}
            
            # Extract name from first cell
            name_cell = cells[0]
            character_data['name'] = self.clean_text(name_cell.get_text())
            
            # Look for character page link
            link = name_cell.find('a', href=True)
            if link:
                character_data['wiki_url'] = urljoin(self.base_url, link['href'])
            
            # Extract real name if available
            if len(cells) > 1:
                real_name = self.clean_text(cells[1].get_text())
                if real_name and real_name != '-':
                    character_data['real_name'] = real_name
            
            # Extract specialty if available
            if len(cells) > 2:
                specialty = self.clean_text(cells[2].get_text())
                if specialty and specialty != '-':
                    character_data['specialty'] = specialty
            
            # Determine faction
            page_text = str(table.parent).lower()
            if 'cobra' in page_text:
                character_data['faction'] = 'Cobra'
            elif 'joe' in page_text or 'g.i.' in page_text:
                character_data['faction'] = 'G.I. Joe'
            else:
                character_data['faction'] = 'Unknown'
            
            if character_data['name']:
                characters.append(character_data)
        
        return characters
    
    def parse_character_list(self, ul_element, section_context: str) -> List[Dict[str, Any]]:
        """Parse a character list from wiki"""
        characters = []
        
        for li in ul_element.find_all('li'):
            character_data = {}
            
            # Extract character name
            link = li.find('a', href=True)
            if link:
                character_data['name'] = self.clean_text(link.get_text())
                character_data['wiki_url'] = urljoin(self.base_url, link['href'])
            else:
                # No link, try to extract name from text
                name = self.clean_text(li.get_text())
                if name:
                    character_data['name'] = name
            
            # Determine faction from section context
            if 'cobra' in section_context:
                character_data['faction'] = 'Cobra'
            elif 'joe' in section_context:
                character_data['faction'] = 'G.I. Joe'
            else:
                character_data['faction'] = 'Unknown'
            
            if character_data.get('name'):
                characters.append(character_data)
        
        return characters
    
    def enhance_vehicle_data(self, vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance vehicle data by scraping individual vehicle pages"""
        if not vehicle_data.get('wiki_url'):
            return vehicle_data
        
        soup = self.get_page_content(vehicle_data['wiki_url'])
        if not soup:
            return vehicle_data
        
        # Extract description from first paragraph
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            first_p = content_div.find('p')
            if first_p:
                description = self.clean_text(first_p.get_text())
                if description:
                    vehicle_data['description'] = description
        
        # Look for infobox
        infobox = soup.find('table', class_='infobox')
        if infobox:
            vehicle_data.update(self.parse_infobox(infobox))
        
        # Extract image URL
        image = soup.find('img', class_='thumbimage')
        if image and image.get('src'):
            vehicle_data['image_url'] = urljoin(self.base_url, image['src'])
        
        return vehicle_data
    
    def enhance_character_data(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance character data by scraping individual character pages"""
        if not character_data.get('wiki_url'):
            return character_data
        
        soup = self.get_page_content(character_data['wiki_url'])
        if not soup:
            return character_data
        
        # Extract bio from first paragraph
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            first_p = content_div.find('p')
            if first_p:
                bio = self.clean_text(first_p.get_text())
                if bio:
                    character_data['bio'] = bio
        
        # Look for infobox
        infobox = soup.find('table', class_='infobox')
        if infobox:
            character_data.update(self.parse_infobox(infobox))
        
        # Extract image URL
        image = soup.find('img', class_='thumbimage')
        if image and image.get('src'):
            character_data['image_url'] = urljoin(self.base_url, image['src'])
        
        return character_data
    
    def parse_infobox(self, infobox) -> Dict[str, Any]:
        """Parse an infobox table for additional data"""
        data = {}
        
        rows = infobox.find_all('tr')
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 2:
                key = self.clean_text(cells[0].get_text()).lower()
                value = self.clean_text(cells[1].get_text())
                
                # Map common infobox fields
                if 'real name' in key or 'birth name' in key:
                    data['real_name'] = value
                elif 'specialty' in key or 'specialties' in key:
                    data['specialty'] = value
                elif 'faction' in key or 'allegiance' in key:
                    data['faction'] = value
                elif 'rank' in key:
                    data['rank'] = value
                elif 'birthplace' in key or 'place of birth' in key:
                    data['birthplace'] = value
                elif 'first appearance' in key:
                    data['first_appearance'] = value
                elif 'voice' in key or 'voiced by' in key:
                    data['voice_actor'] = value
                elif 'pilot' in key or 'driver' in key:
                    data['pilot_driver'] = value
                elif 'crew' in key:
                    data['crew_capacity'] = value
                elif 'weapon' in key:
                    data['weapons'] = value
        
        return data
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove citation markers like [1], [2], etc.
        text = re.sub(r'\[\d+\]', '', text)
        
        # Remove other common wiki markup artifacts
        text = re.sub(r'\([^)]*edit[^)]*\)', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def save_vehicles_to_db(self, vehicles: List[Dict[str, Any]]):
        """Save vehicle data to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                saved_count = 0
                for vehicle in vehicles:
                    try:
                        cursor.execute("""
                            INSERT OR REPLACE INTO gijoe_vehicles (
                                name, year_introduced, faction, category, 
                                description, pilot_driver, wiki_url, image_url, raw_data
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            vehicle.get('name'),
                            vehicle.get('year_introduced'),
                            vehicle.get('faction'),
                            vehicle.get('category'),
                            vehicle.get('description'),
                            vehicle.get('pilot_driver'),
                            vehicle.get('wiki_url'),
                            vehicle.get('image_url'),
                            json.dumps(vehicle)
                        ))
                        saved_count += 1
                    except sqlite3.Error as e:
                        print(f"❌ Error saving vehicle {vehicle.get('name')}: {e}")
                
                conn.commit()
                print(f"✅ Saved {saved_count} vehicles to database")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def save_characters_to_db(self, characters: List[Dict[str, Any]]):
        """Save character data to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                saved_count = 0
                for character in characters:
                    try:
                        cursor.execute("""
                            INSERT OR REPLACE INTO gijoe_characters (
                                name, real_name, faction, specialty, bio, 
                                wiki_url, image_url, raw_data
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            character.get('name'),
                            character.get('real_name'),
                            character.get('faction'),
                            character.get('specialty'),
                            character.get('bio'),
                            character.get('wiki_url'),
                            character.get('image_url'),
                            json.dumps(character)
                        ))
                        saved_count += 1
                    except sqlite3.Error as e:
                        print(f"❌ Error saving character {character.get('name')}: {e}")
                
                conn.commit()
                print(f"✅ Saved {saved_count} characters to database")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def run_full_scrape(self):
        """Run complete scraping operation"""
        print("🚀 Starting G.I. Joe Wiki scraping...")
        
        # Scrape vehicles
        print("\n📋 Scraping vehicles...")
        vehicles = self.scrape_vehicle_list_page()
        print(f"Found {len(vehicles)} vehicles")
        
        # Enhance vehicle data with individual page info
        print("🔍 Enhancing vehicle data...")
        enhanced_vehicles = []
        for i, vehicle in enumerate(vehicles[:20]):  # Limit to first 20 for demo
            print(f"Enhancing vehicle {i+1}/{min(20, len(vehicles))}: {vehicle['name']}")
            enhanced_vehicle = self.enhance_vehicle_data(vehicle)
            enhanced_vehicles.append(enhanced_vehicle)
        
        self.save_vehicles_to_db(enhanced_vehicles)
        
        # Scrape characters
        print("\n👥 Scraping characters...")
        characters = self.scrape_character_list_page()
        print(f"Found {len(characters)} characters")
        
        # Enhance character data with individual page info
        print("🔍 Enhancing character data...")
        enhanced_characters = []
        for i, character in enumerate(characters[:30]):  # Limit to first 30 for demo
            print(f"Enhancing character {i+1}/{min(30, len(characters))}: {character['name']}")
            enhanced_character = self.enhance_character_data(character)
            enhanced_characters.append(enhanced_character)
        
        self.save_characters_to_db(enhanced_characters)
        
        print("\n✅ G.I. Joe data scraping complete!")
    
    def get_database_stats(self):
        """Print database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get vehicle stats
                cursor.execute("SELECT COUNT(*) FROM gijoe_vehicles")
                vehicle_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT faction, COUNT(*) FROM gijoe_vehicles GROUP BY faction")
                vehicle_factions = cursor.fetchall()
                
                # Get character stats
                cursor.execute("SELECT COUNT(*) FROM gijoe_characters")
                character_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT faction, COUNT(*) FROM gijoe_characters GROUP BY faction")
                character_factions = cursor.fetchall()
                
                print(f"\n📊 Database Statistics:")
                print(f"   Vehicles: {vehicle_count}")
                for faction, count in vehicle_factions:
                    print(f"     {faction}: {count}")
                
                print(f"   Characters: {character_count}")
                for faction, count in character_factions:
                    print(f"     {faction}: {count}")
                
        except sqlite3.Error as e:
            print(f"❌ Error getting database stats: {e}")


if __name__ == "__main__":
    scraper = GIJoeWikiScraper()
    
    print("G.I. Joe Fandom Wiki Scraper")
    print("1. Run full scrape")
    print("2. Show database stats")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        scraper.run_full_scrape()
        scraper.get_database_stats()
    elif choice == "2":
        scraper.get_database_stats()
    else:
        print("Goodbye!")
