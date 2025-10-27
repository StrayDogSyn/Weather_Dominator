"""
data/gijoe_api.py - G.I. Joe Fandom API integration
Write a function that searches for a Cobra character on gijoe.fandom.com using the MediaWiki API.
Return the character bio summary, image URL, and related links.
"""

import requests
import json
from typing import Dict, List, Optional, Any
import re
from urllib.parse import quote

from src.logger import get_logger
from src.exceptions import APIError
from src.constants import GIJOE_FANDOM_API, GIJOE_WIKI_URL, APIConfig

# Initialize logger for this module
logger = get_logger(__name__)

class GIJoeAPI:
    """G.I. Joe Fandom API integration for fetching Cobra character data"""
    
    def __init__(self):
        """Initialize G.I. Joe Fandom API client"""
        logger.debug("Initializing GIJoeAPI client")
        
        self.base_url = GIJOE_FANDOM_API
        self.wiki_url = GIJOE_WIKI_URL
        self.image_base_url = "https://static.wikia.nocookie.net/gijoe/images"
        
        logger.debug(f"API initialized: base_url={self.base_url}, wiki_url={self.wiki_url}")
        
        # Expanded Cobra character database with detailed information
        self.cobra_characters = [
            "Cobra Commander", "Destro", "Baroness", "Storm Shadow", "Zartan",
            "Dr. Mindbender", "Tomax", "Xamot", "Scrap-Iron", "Firefly",
            "Wild Weasel", "Buzzer", "Ripper", "Torch", "Major Bludd",
            "Copperhead", "Viper", "Crimson Guard", "Serpentor", "Golobulus",
            "Nemesis Enforcer", "Crystal Ball", "Croc Master", "Overlord",
            "Big Boa", "Iron Grenadier", "Range-Viper", "Techno-Viper",
            "Tele-Viper", "Night-Viper", "Alley-Viper", "Snow Serpent",
            "Desert Scorpion", "Hydro-Viper", "Aero-Viper", "Ast-Viper",
            "Cesspool", "Gnawgahyde", "Road Pig", "Skull Buster",
            "Headhunter", "Darklon", "Voltar", "Python Patrol"
        ]
        
        # Cobra vehicle and weapon data
        self.cobra_vehicles = [
            "HISS Tank", "Cobra Flight Pod", "Rattler", "Mamba", "Stinger",
            "Ferret ATV", "Water Moccasin", "Moray Hydrofoil", "Devilfish",
            "Terror Drome", "Firebat", "Night Raven", "Conquest X-30",
            "Phantom X-19", "Hammerhead", "Bugg", "Pogo", "ASP"
        ]
        
        # Cobra organization structure
        self.cobra_hierarchy = {
            "Supreme Leader": ["Cobra Commander", "Serpentor"],
            "High Command": ["Destro", "Baroness", "Dr. Mindbender"],
            "Field Commanders": ["Major Bludd", "Firefly", "Storm Shadow"],
            "Specialists": ["Zartan", "Tomax", "Xamot", "Wild Weasel"],
            "Troops": ["Viper", "Crimson Guard", "Alley-Viper", "Range-Viper"]
        }
        
        # Cobra base locations
        self.cobra_bases = [
            "Cobra Island", "Terror Drome", "Silent Castle", "Cobra Mountain",
            "Extensive Enterprises", "M.A.R.S. Industries", "Trans-Carpathian"
        ]
    
    def search_character(self, character_name: str) -> Dict[str, Any]:
        """
        Search for a character using the MediaWiki search API
        
        Args:
            character_name: Name of the character to search for
            
        Returns:
            Dictionary containing search results or error information
            
        Raises:
            APIError: If the search request fails
        """
        logger.info(f"Searching for character: {character_name}")
        
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": character_name,
                "srlimit": 5,
                "srprop": "snippet|titlesnippet|size"
            }
            
            logger.debug(f"Making search request to {self.base_url}")
            response = requests.get(self.base_url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            
            if not search_results:
                logger.warning(f"No results found for '{character_name}'")
                raise APIError(f"No results found for '{character_name}'")
            
            # Return the first result
            result = search_results[0]
            logger.info(f"Found character: {result['title']}")
            return {
                "title": result["title"],
                "snippet": self._clean_html(result.get("snippet", "")),
                "page_id": result["pageid"],
                "size": result["size"]
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout searching for '{character_name}'")
            raise APIError(f"Request timeout while searching for '{character_name}'")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error searching for '{character_name}': {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error searching for '{character_name}': {e}")
            raise APIError(f"Network error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error searching for '{character_name}'")
            raise APIError(f"Search error: {str(e)}")
    
    def get_character_data(self, character_name: str) -> Dict[str, Any]:
        """
        Get detailed character data including bio, image, and links
        
        Args:
            character_name: Name of the character
            
        Returns:
            Dictionary containing character data or error information
            
        Raises:
            APIError: If character data retrieval fails
        """
        logger.info(f"Fetching detailed character data for: {character_name}")
        
        try:
            # First, search for the character to get the exact page title
            try:
                search_result = self.search_character(character_name)
                page_title = search_result["title"]
            except APIError:
                # Try searching from common Cobra characters
                logger.warning(f"Search failed, trying fallback for '{character_name}'")
                return self._get_fallback_character(character_name)
            
            # Get page content
            params = {
                "action": "query",
                "format": "json",
                "titles": page_title,
                "prop": "extracts|pageimages|info",
                "exintro": True,
                "explaintext": True,
                "exsectionformat": "plain",
                "piprop": "original",
                "inprop": "url"
            }
            
            logger.debug(f"Fetching page content for: {page_title}")
            response = requests.get(self.base_url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                logger.error(f"No page data found for '{character_name}'")
                raise APIError(f"No page data found for '{character_name}'")
            
            # Get the first (and usually only) page
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            
            if page_id == "-1":  # Page not found
                logger.error(f"Character page not found for '{character_name}'")
                raise APIError(f"Character page not found for '{character_name}'")
            
            # Extract character information
            character_data = {
                "name": page_data.get("title", character_name),
                "bio": self._extract_bio(page_data.get("extract", "")),
                "full_bio": page_data.get("extract", ""),
                "image_url": self._get_image_url(page_data),
                "wiki_url": page_data.get("fullurl", f"{self.wiki_url}/{quote(page_title)}"),
                "page_id": page_data.get("pageid"),
                "is_cobra": self._is_cobra_character(page_data.get("extract", ""))
            }
            
            logger.info(f"Successfully retrieved data for character: {character_data['name']}")
            return character_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for character '{character_name}'")
            raise APIError(f"Request timeout while fetching character data for '{character_name}'")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for character '{character_name}': {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for character '{character_name}': {e}")
            raise APIError(f"Network error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error retrieving character '{character_name}'")
            raise APIError(f"Data retrieval error: {str(e)}")
    
    def get_random_cobra_character(self) -> Dict[str, Any]:
        """
        Get a random Cobra character from the predefined list
        
        Returns:
            Dictionary containing character data
            
        Raises:
            APIError: If character data retrieval fails
        """
        import random
        character = random.choice(self.cobra_characters)
        logger.info(f"Getting random Cobra character: {character}")
        return self.get_character_data(character)
    
    def search_cobra_characters(self, query: str = "Cobra") -> List[Dict[str, Any]]:
        """
        Search for Cobra-related characters
        
        Args:
            query: Search query (default: "Cobra")
            
        Returns:
            List of character search results
            
        Raises:
            APIError: If search request fails
        """
        logger.info(f"Searching for Cobra characters with query: {query}")
        
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": f"{query} character",
                "srlimit": 10,
                "srprop": "snippet|titlesnippet"
            }
            
            logger.debug(f"Making Cobra search request")
            response = requests.get(self.base_url, params=params, timeout=APIConfig.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            
            characters = []
            for result in search_results:
                if self._looks_like_character(result["title"]):
                    characters.append({
                        "name": result["title"],
                        "snippet": self._clean_html(result.get("snippet", "")),
                        "wiki_url": f"{self.wiki_url}/{quote(result['title'])}"
                    })
            
            logger.info(f"Found {len(characters)} Cobra characters")
            return characters
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout searching for Cobra characters")
            raise APIError(f"Request timeout while searching for Cobra characters")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error searching for Cobra characters: {e}")
            raise APIError(f"HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error searching for Cobra characters: {e}")
            raise APIError(f"Network error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error searching for Cobra characters")
            raise APIError(f"Search error: {str(e)}")
    
    def _get_fallback_character(self, character_name: str) -> Dict[str, Any]:
        """Get a fallback character if search fails"""
        # Try to find a similar character name
        character_name_lower = character_name.lower()
        
        for cobra_char in self.cobra_characters:
            if character_name_lower in cobra_char.lower() or cobra_char.lower() in character_name_lower:
                return self.get_character_data(cobra_char)
        
        # Return a default Cobra Commander if nothing matches
        return {
            "name": "Cobra Commander",
            "bio": "The ruthless leader of the terrorist organization known as Cobra. His identity remains a mystery, hidden behind his distinctive metal mask.",
            "full_bio": "Cobra Commander is the supreme leader of the terrorist organization Cobra and the main antagonist of the G.I. Joe franchise. He is a ruthless dictator who rules Cobra with an iron fist and dreams of world domination.",
            "image_url": None,
            "wiki_url": f"{self.wiki_url}/Cobra_Commander",
            "page_id": None,
            "is_cobra": True,
            "fallback": True
        }
    
    def _extract_bio(self, full_text: str) -> str:
        """Extract a concise bio from the full page text"""
        if not full_text:
            return "No bio available"
        
        # Take the first paragraph or first 200 characters
        paragraphs = full_text.split('\n\n')
        bio = paragraphs[0] if paragraphs else full_text
        
        # Truncate if too long
        if len(bio) > 200:
            bio = bio[:200] + "..."
        
        return bio.strip()
    
    def _get_image_url(self, page_data: Dict[str, Any]) -> Optional[str]:
        """Extract image URL from page data"""
        original = page_data.get("original")
        if original:
            return original.get("source")
        return None
    
    def _is_cobra_character(self, text: str) -> bool:
        """Check if the character is associated with Cobra"""
        if not text:
            return False
        
        text_lower = text.lower()
        cobra_keywords = ["cobra", "terrorist", "villain", "enemy", "bad guy", "antagonist"]
        
        return any(keyword in text_lower for keyword in cobra_keywords)
    
    def _looks_like_character(self, title: str) -> bool:
        """Check if a search result looks like a character page"""
        # Filter out non-character pages
        exclude_keywords = ["category:", "file:", "template:", "user:", "episode", "series", "toy"]
        title_lower = title.lower()
        
        return not any(keyword in title_lower for keyword in exclude_keywords)
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean up text"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        
        return clean_text
    
    def get_cobra_intel_package(self, character_name: str) -> Dict[str, Any]:
        """
        Get comprehensive Cobra intelligence package for a character
        
        Args:
            character_name: Name of the character
            
        Returns:
            Comprehensive character intelligence package
        """
        base_data = self.get_character_data(character_name)
        
        if "error" in base_data:
            return base_data
        
        # Enhance with additional intelligence
        intel_package = base_data.copy()
        intel_package.update({
            "rank": self._get_cobra_rank(character_name),
            "specialties": self._get_character_specialties(base_data.get("full_bio", "")),
            "vehicles": self._get_associated_vehicles(character_name),
            "allies": self._get_character_allies(character_name),
            "threat_level": self._assess_threat_level(base_data.get("full_bio", "")),
            "base_of_operations": self._get_base_operations(character_name),
            "first_appearance": self._extract_first_appearance(base_data.get("full_bio", "")),
            "image_gallery": self._get_character_images(character_name),
            "cobra_classification": self._classify_cobra_member(character_name, base_data.get("full_bio", ""))
        })
        
        return intel_package
    
    def get_cobra_vehicle_data(self, vehicle_name: str) -> Dict[str, Any]:
        """
        Get detailed information about Cobra vehicles and equipment
        
        Args:
            vehicle_name: Name of the vehicle
            
        Returns:
            Vehicle data dictionary
        """
        try:
            # Search for vehicle information
            params = {
                "action": "query",
                "format": "json",
                "titles": vehicle_name,
                "prop": "extracts|pageimages|info",
                "exintro": True,
                "explaintext": True,
                "piprop": "original",
                "inprop": "url"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                return {"error": f"No vehicle data found for '{vehicle_name}'"}
            
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            
            if page_id == "-1":
                return {"error": f"Vehicle not found: '{vehicle_name}'"}
            
            vehicle_data = {
                "name": page_data.get("title", vehicle_name),
                "description": self._extract_bio(page_data.get("extract", "")),
                "full_description": page_data.get("extract", ""),
                "image_url": self._get_image_url(page_data),
                "wiki_url": page_data.get("fullurl", f"{self.wiki_url}/{quote(vehicle_name)}"),
                "vehicle_type": self._classify_vehicle_type(page_data.get("extract", "")),
                "crew_size": self._extract_crew_info(page_data.get("extract", "")),
                "armament": self._extract_armament_info(page_data.get("extract", "")),
                "specifications": self._extract_specifications(page_data.get("extract", ""))
            }
            
            return vehicle_data
            
        except Exception as e:
            return {"error": f"Vehicle data error: {str(e)}"}
    
    def get_cobra_hierarchy_data(self) -> Dict[str, Any]:
        """
        Get complete Cobra organization hierarchy
        
        Returns:
            Cobra hierarchy with character details
        """
        hierarchy_with_details = {}
        
        for rank, characters in self.cobra_hierarchy.items():
            hierarchy_with_details[rank] = []
            
            for character in characters:
                char_data = self.get_character_data(character)
                if "error" not in char_data:
                    hierarchy_with_details[rank].append({
                        "name": char_data["name"],
                        "bio": char_data["bio"],
                        "image_url": char_data.get("image_url"),
                        "wiki_url": char_data["wiki_url"],
                        "specialties": self._get_character_specialties(char_data.get("full_bio", ""))
                    })
        
        return {
            "hierarchy": hierarchy_with_details,
            "total_members": sum(len(chars) for chars in hierarchy_with_details.values()),
            "organization_structure": "Terrorist Organization",
            "primary_goal": "World Domination",
            "headquarters": "Cobra Island"
        }
    
    def get_multiple_character_images(self, character_names: List[str]) -> Dict[str, List[str]]:
        """
        Get multiple images for multiple characters
        
        Args:
            character_names: List of character names
            
        Returns:
            Dictionary mapping character names to lists of image URLs
        """
        character_images = {}
        
        for character in character_names:
            character_images[character] = self._get_character_images(character)
        
        return character_images
    
    def get_cobra_mission_briefing(self, scenario: str = "weather_domination") -> Dict[str, Any]:
        """
        Generate a Cobra mission briefing based on scenario
        
        Args:
            scenario: Type of mission scenario
            
        Returns:
            Mission briefing data
        """
        mission_templates = {
            "weather_domination": {
                "mission_name": "Operation Weather Dominator",
                "objective": "Deploy weather control technology to achieve global supremacy",
                "primary_agents": ["Cobra Commander", "Dr. Mindbender", "Destro"],
                "support_units": ["Techno-Viper", "Crimson Guard", "Viper"],
                "vehicles": ["Weather Dominator", "HISS Tank", "Rattler"],
                "target_locations": ["Major Population Centers", "Military Installations"],
                "threat_assessment": "MAXIMUM",
                "countermeasures": "G.I. Joe Response Expected"
            },
            "infiltration": {
                "mission_name": "Operation Silent Strike",
                "objective": "Infiltrate enemy installations and gather intelligence",
                "primary_agents": ["Storm Shadow", "Firefly", "Zartan"],
                "support_units": ["Night-Viper", "Alley-Viper"],
                "vehicles": ["Night Raven", "Ferret ATV"],
                "target_locations": ["Government Facilities", "Military Bases"],
                "threat_assessment": "HIGH",
                "countermeasures": "Stealth Operations Required"
            }
        }
        
        template = mission_templates.get(scenario, mission_templates["weather_domination"])
        
        # Add character details to the briefing
        enhanced_briefing = template.copy()
        enhanced_briefing["agent_profiles"] = []
        
        for agent in template["primary_agents"]:
            agent_data = self.get_character_data(agent)
            if "error" not in agent_data:
                enhanced_briefing["agent_profiles"].append({
                    "name": agent_data["name"],
                    "role": self._get_cobra_rank(agent),
                    "bio": agent_data["bio"],
                    "image_url": agent_data.get("image_url"),
                    "specialties": self._get_character_specialties(agent_data.get("full_bio", ""))
                })
        
        return enhanced_briefing

    def _get_character_images(self, character_name: str) -> List[str]:
        """
        Get multiple images for a character from the wiki
        
        Args:
            character_name: Name of the character
            
        Returns:
            List of image URLs
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "titles": character_name,
                "prop": "images",
                "imlimit": 10
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                return []
            
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            
            if page_id == "-1":
                return []
            
            images = page_data.get("images", [])
            image_urls = []
            
            # Get image details for each image
            for image in images[:5]:  # Limit to 5 images
                image_title = image["title"]
                image_url = self._get_image_url_from_title(image_title)
                if image_url and self._is_character_image(image_title, character_name):
                    image_urls.append(image_url)
            
            return image_urls
            
        except Exception as e:
            return []
    
    def _get_image_url_from_title(self, image_title: str) -> Optional[str]:
        """Get direct image URL from image title"""
        try:
            params = {
                "action": "query",
                "format": "json",
                "titles": image_title,
                "prop": "imageinfo",
                "iiprop": "url"
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if pages:
                page_id = list(pages.keys())[0]
                page_data = pages[page_id]
                imageinfo = page_data.get("imageinfo", [])
                
                if imageinfo:
                    return imageinfo[0].get("url")
            
            return None
            
        except Exception:
            return None
    
    def _is_character_image(self, image_title: str, character_name: str) -> bool:
        """Check if image is related to the character"""
        image_lower = image_title.lower()
        char_lower = character_name.lower()
        
        # Check if character name is in image title
        if any(word in image_lower for word in char_lower.split()):
            return True
        
        # Exclude common non-character images
        exclude_terms = ["logo", "symbol", "icon", "banner", "template"]
        return not any(term in image_lower for term in exclude_terms)
    
    def _get_cobra_rank(self, character_name: str) -> str:
        """Determine Cobra rank/position for a character"""
        for rank, characters in self.cobra_hierarchy.items():
            if character_name in characters:
                return rank
        return "Unknown Operative"
    
    def _get_character_specialties(self, bio_text: str) -> List[str]:
        """Extract character specialties from bio text"""
        specialties = []
        bio_lower = bio_text.lower()
        
        specialty_keywords = {
            "Combat": ["combat", "fighting", "warrior", "soldier", "martial"],
            "Technology": ["technology", "tech", "scientist", "engineer", "computer"],
            "Espionage": ["spy", "infiltration", "stealth", "intelligence", "covert"],
            "Leadership": ["leader", "command", "commander", "director", "chief"],
            "Weapons": ["weapons", "armament", "arsenal", "explosive", "demolition"],
            "Vehicles": ["pilot", "driver", "vehicle", "aircraft", "tank"],
            "Medical": ["doctor", "medical", "surgeon", "health", "mind"],
            "Disguise": ["disguise", "impersonation", "shapeshifter", "mimic"],
            "Assassination": ["assassin", "killer", "elimination", "sniper"],
            "Sabotage": ["sabotage", "destruction", "disruption", "chaos"]
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in bio_lower for keyword in keywords):
                specialties.append(specialty)
        
        return specialties[:3]  # Limit to top 3 specialties
    
    def _get_associated_vehicles(self, character_name: str) -> List[str]:
        """Get vehicles associated with a character"""
        vehicle_associations = {
            "Cobra Commander": ["HISS Tank", "Rattler", "Terror Drome"],
            "Destro": ["HISS Tank", "Iron Grenadier vehicles"],
            "Wild Weasel": ["Rattler", "Conquest X-30"],
            "Copperhead": ["Water Moccasin", "Moray Hydrofoil"],
            "Storm Shadow": ["Night Raven", "Phantom X-19"],
            "Firefly": ["Devilfish", "Saboteur vehicles"],
            "Major Bludd": ["HISS Tank", "Military vehicles"]
        }
        
        return vehicle_associations.get(character_name, [])
    
    def _get_character_allies(self, character_name: str) -> List[str]:
        """Get known allies for a character"""
        ally_networks = {
            "Cobra Commander": ["Destro", "Baroness", "Dr. Mindbender"],
            "Destro": ["Cobra Commander", "Baroness", "Iron Grenadiers"],
            "Baroness": ["Destro", "Cobra Commander", "Zartan"],
            "Storm Shadow": ["Snake Eyes", "Hard Master", "Zartan"],
            "Tomax": ["Xamot", "Crimson Guard"],
            "Xamot": ["Tomax", "Crimson Guard"],
            "Dr. Mindbender": ["Cobra Commander", "Serpentor", "B.A.T.s"]
        }
        
        return ally_networks.get(character_name, [])
    
    def _assess_threat_level(self, bio_text: str) -> str:
        """Assess threat level based on character description"""
        bio_lower = bio_text.lower()
        
        high_threat_terms = ["commander", "leader", "deadly", "dangerous", "ruthless", "supreme"]
        medium_threat_terms = ["skilled", "trained", "experienced", "specialist"]
        
        if any(term in bio_lower for term in high_threat_terms):
            return "MAXIMUM"
        elif any(term in bio_lower for term in medium_threat_terms):
            return "HIGH"
        else:
            return "MODERATE"
    
    def _get_base_operations(self, character_name: str) -> str:
        """Get primary base of operations for character"""
        base_assignments = {
            "Cobra Commander": "Cobra Island",
            "Destro": "Castle Destro, Scotland",
            "Baroness": "Trans-Carpathian Castle",
            "Dr. Mindbender": "Cobra Laboratory Complex",
            "Serpentor": "Cobra Temple",
            "Storm Shadow": "Silent Castle, Japan"
        }
        
        return base_assignments.get(character_name, "Unknown Location")
    
    def _extract_first_appearance(self, bio_text: str) -> str:
        """Extract first appearance information from bio"""
        # Look for patterns like "first appeared in" or "introduced in"
        patterns = [
            r"first appeared in ([^.]+)",
            r"introduced in ([^.]+)",
            r"debuted in ([^.]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, bio_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown"
    
    def _classify_cobra_member(self, character_name: str, bio_text: str) -> Dict[str, str]:
        """Classify the type of Cobra member"""
        classification = {
            "category": "Unknown",
            "division": "General Forces",
            "loyalty": "Cobra"
        }
        
        bio_lower = bio_text.lower()
        name_lower = character_name.lower()
        
        # Determine category
        if any(term in name_lower for term in ["commander", "leader"]):
            classification["category"] = "Leadership"
        elif any(term in bio_lower for term in ["scientist", "doctor", "engineer"]):
            classification["category"] = "Scientific Division"
        elif any(term in name_lower for term in ["viper", "guard", "trooper"]):
            classification["category"] = "Infantry"
        elif any(term in bio_lower for term in ["pilot", "driver"]):
            classification["category"] = "Vehicle Operations"
        elif any(term in bio_lower for term in ["spy", "infiltrator", "assassin"]):
            classification["category"] = "Special Operations"
          # Determine division
        if "destro" in bio_lower or "iron grenadier" in bio_lower:
            classification["division"] = "Iron Grenadiers"
        elif "dreadnok" in bio_lower:
            classification["division"] = "Dreadnoks"
        elif "crimson guard" in name_lower:
            classification["division"] = "Crimson Guard"
        
        return classification
    
    def _classify_vehicle_type(self, description: str) -> str:
        """Classify vehicle type from description"""
        desc_lower = description.lower()
        
        if any(term in desc_lower for term in ["aircraft", "plane", "jet", "helicopter"]):
            return "Aircraft"
        elif any(term in desc_lower for term in ["tank", "armor", "tracked"]):
            return "Armored Vehicle"
        elif any(term in desc_lower for term in ["boat", "ship", "submarine", "water"]):
            return "Naval Vessel"
        elif any(term in desc_lower for term in ["base", "installation", "complex"]):
            return "Installation"
        else:
            return "Ground Vehicle"
    
    def _extract_crew_info(self, description: str) -> str:
        """Extract crew size information"""
        patterns = [
            r"crew of (\d+)",
            r"(\d+) crew members",
            r"operated by (\d+)",
            r"single pilot",
            r"pilot"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                if "single pilot" in match.group(0).lower():
                    return "1 (Pilot)"
                elif "pilot" in match.group(0).lower() and not match.groups():
                    return "1 (Pilot)"
                else:
                    return match.group(1) if match.groups() else match.group(0)
        
        return "Unknown"
    
    def _extract_armament_info(self, description: str) -> List[str]:
        """Extract armament information"""
        armaments = []
        desc_lower = description.lower()
        
        weapon_terms = [
            "laser", "missile", "cannon", "gun", "rocket", "torpedo",
            "plasma", "energy weapon", "machinegun", "autocannon"
        ]
        
        for weapon in weapon_terms:
            if weapon in desc_lower:
                armaments.append(weapon.title())
        
        return armaments[:5]  # Limit to 5 weapons
    
    def _extract_specifications(self, description: str) -> Dict[str, str]:
        """Extract technical specifications"""
        specs = {}
        
        # Look for speed, range, etc.
        speed_match = re.search(r"speed of ([^.]+)", description, re.IGNORECASE)
        if speed_match:
            specs["max_speed"] = speed_match.group(1).strip()
        
        range_match = re.search(r"range of ([^.]+)", description, re.IGNORECASE)
        if range_match:
            specs["range"] = range_match.group(1).strip()
        
        return specs

# Enhanced Convenience functions for easy use
def get_cobra_character(character_name: str) -> Dict[str, Any]:
    """Enhanced convenience function to get Cobra character data"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_character_data(character_name)

def get_cobra_intel_package(character_name: str) -> Dict[str, Any]:
    """Get comprehensive Cobra intelligence package"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_cobra_intel_package(character_name)

def get_random_cobra() -> Dict[str, Any]:
    """Convenience function to get a random Cobra character"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_random_cobra_character()

def get_cobra_vehicle_intel(vehicle_name: str) -> Dict[str, Any]:
    """Get Cobra vehicle intelligence data"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_cobra_vehicle_data(vehicle_name)

def get_cobra_hierarchy() -> Dict[str, Any]:
    """Get complete Cobra organization hierarchy"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_cobra_hierarchy_data()

def get_mission_briefing(scenario: str = "weather_domination") -> Dict[str, Any]:
    """Generate Cobra mission briefing"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_cobra_mission_briefing(scenario)

def search_cobra_intel(query: str) -> List[Dict[str, Any]]:
    """Convenience function to search Cobra intelligence"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.search_cobra_characters(query)

def get_cobra_image_gallery(characters: List[str]) -> Dict[str, List[str]]:
    """Get image galleries for multiple Cobra characters"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_multiple_character_images(characters)

# Example usage and testing
if __name__ == "__main__":
    # Test the Enhanced G.I. Joe API
    logger.info("Starting GIJoeAPI test")
    gijoe_api = GIJoeAPI()
    
    logger.info("=" * 60)
    
    # Test enhanced character data
    test_character = "Cobra Commander"
    logger.info(f"Testing Enhanced Intel Package for {test_character}")
    
    try:
        intel_package = gijoe_api.get_cobra_intel_package(test_character)
        logger.info(f"Name: {intel_package['name']}")
        logger.info(f"Rank: {intel_package['rank']}")
        logger.info(f"Threat Level: {intel_package['threat_level']}")
        logger.info(f"Base of Operations: {intel_package['base_of_operations']}")
        logger.info(f"Specialties: {', '.join(intel_package['specialties'])}")
        logger.info(f"Vehicles: {', '.join(intel_package['vehicles'])}")
        logger.info(f"Classification: {intel_package['cobra_classification']['category']}")
        if intel_package['image_gallery']:
            logger.info(f"Images Available: {len(intel_package['image_gallery'])}")
    except APIError as e:
        logger.error(f"Error fetching intel package: {e}")
    
    # Test vehicle data
    logger.info("Testing Vehicle Intelligence for HISS Tank")
    try:
        vehicle_data = gijoe_api.get_cobra_vehicle_data("HISS Tank")
        logger.info(f"Vehicle: {vehicle_data['name']}")
        logger.info(f"Type: {vehicle_data['vehicle_type']}")
        logger.info(f"Crew: {vehicle_data['crew_size']}")
        logger.info(f"Armament: {', '.join(vehicle_data['armament'])}")
    except APIError as e:
        logger.error(f"Error fetching vehicle data: {e}")
    
    # Test hierarchy data
    logger.info("Testing Cobra Organization Hierarchy")
    hierarchy = gijoe_api.get_cobra_hierarchy_data()
    
    logger.info(f"Organization: {hierarchy['organization_structure']}")
    logger.info(f"Primary Goal: {hierarchy['primary_goal']}")
    logger.info(f"Total Members: {hierarchy['total_members']}")
    logger.info(f"Headquarters: {hierarchy['headquarters']}")
    
    for rank, members in hierarchy['hierarchy'].items():
        if members:
            logger.info(f"{rank}: {len(members)} members")
    
    # Test mission briefing
    logger.info("Testing Mission Briefing Generation")
    mission = gijoe_api.get_cobra_mission_briefing("weather_domination")
    
    logger.info(f"Mission: {mission['mission_name']}")
    logger.info(f"Objective: {mission['objective']}")
    logger.info(f"Threat Assessment: {mission['threat_assessment']}")
    logger.info(f"Primary Agents: {', '.join(mission['primary_agents'])}")
    logger.info(f"Agent Profiles: {len(mission['agent_profiles'])} detailed profiles")
    
    # Test random character
    logger.info("Testing Random Cobra Character")
    try:
        random_char = gijoe_api.get_random_cobra_character()
        logger.info(f"Random Selection: {random_char['name']}")
        logger.info(f"Bio: {random_char['bio']}")
    except APIError as e:
        logger.error(f"Error fetching random character: {e}")
    
    # Test image gallery
    logger.info("Testing Image Gallery for Top Characters")
    top_characters = ["Cobra Commander", "Destro", "Baroness"]
    image_gallery = gijoe_api.get_multiple_character_images(top_characters)
    
    for char, images in image_gallery.items():
        logger.info(f"{char}: {len(images)} images available")
    
    logger.info("COBRA Intelligence System Test Complete!")
