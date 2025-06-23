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

class GIJoeAPI:
    """G.I. Joe Fandom API integration for fetching Cobra character data"""
    
    def __init__(self):
        """Initialize G.I. Joe Fandom API client"""
        self.base_url = "https://gijoe.fandom.com/api.php"
        self.wiki_url = "https://gijoe.fandom.com/wiki"
        
        # Common Cobra characters for fallback
        self.cobra_characters = [
            "Cobra Commander", "Destro", "Baroness", "Storm Shadow", "Zartan",
            "Dr. Mindbender", "Tomax", "Xamot", "Scrap-Iron", "Firefly",
            "Wild Weasel", "Buzzer", "Ripper", "Torch", "Major Bludd",
            "Copperhead", "Viper", "Crimson Guard", "Serpentor", "Golobulus"
        ]
    
    def search_character(self, character_name: str) -> Dict[str, Any]:
        """
        Search for a character using the MediaWiki search API
        
        Args:
            character_name: Name of the character to search for
            
        Returns:
            Dictionary containing search results or error information
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": character_name,
                "srlimit": 5,
                "srprop": "snippet|titlesnippet|size"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            
            if not search_results:
                return {"error": f"No results found for '{character_name}'"}
            
            # Return the first result
            result = search_results[0]
            return {
                "title": result["title"],
                "snippet": self._clean_html(result.get("snippet", "")),
                "page_id": result["pageid"],
                "size": result["size"]
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Search error: {str(e)}"}
    
    def get_character_data(self, character_name: str) -> Dict[str, Any]:
        """
        Get detailed character data including bio, image, and links
        
        Args:
            character_name: Name of the character
            
        Returns:
            Dictionary containing character data or error information
        """
        try:
            # First, search for the character to get the exact page title
            search_result = self.search_character(character_name)
            
            if "error" in search_result:
                # Try searching from common Cobra characters
                return self._get_fallback_character(character_name)
            
            page_title = search_result["title"]
            
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
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                return {"error": f"No page data found for '{character_name}'"}
            
            # Get the first (and usually only) page
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            
            if page_id == "-1":  # Page not found
                return {"error": f"Character page not found for '{character_name}'"}
            
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
            
            return character_data
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Data retrieval error: {str(e)}"}
    
    def get_random_cobra_character(self) -> Dict[str, Any]:
        """
        Get a random Cobra character from the predefined list
        
        Returns:
            Dictionary containing character data
        """
        import random
        character = random.choice(self.cobra_characters)
        return self.get_character_data(character)
    
    def search_cobra_characters(self, query: str = "Cobra") -> List[Dict[str, Any]]:
        """
        Search for Cobra-related characters
        
        Args:
            query: Search query (default: "Cobra")
            
        Returns:
            List of character search results
        """
        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": f"{query} character",
                "srlimit": 10,
                "srprop": "snippet|titlesnippet"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
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
            
            return characters
            
        except Exception as e:
            return [{"error": f"Search error: {str(e)}"}]
    
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

# Convenience functions for easy use
def get_cobra_character(character_name: str) -> Dict[str, Any]:
    """Convenience function to get Cobra character data"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_character_data(character_name)

def get_random_cobra() -> Dict[str, Any]:
    """Convenience function to get a random Cobra character"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.get_random_cobra_character()

def search_cobra_intel(query: str) -> List[Dict[str, Any]]:
    """Convenience function to search Cobra intelligence"""
    gijoe_api = GIJoeAPI()
    return gijoe_api.search_cobra_characters(query)

# Example usage and testing
if __name__ == "__main__":
    # Test the G.I. Joe API
    gijoe_api = GIJoeAPI()
    
    # Test characters
    test_characters = ["Cobra Commander", "Destro", "Baroness", "Storm Shadow"]
    
    for character in test_characters:
        print(f"\n🐍 Testing Cobra Intel for {character}:")
        char_data = gijoe_api.get_character_data(character)
        
        if "error" in char_data:
            print(f"❌ Error: {char_data['error']}")
        else:
            print(f"✅ Name: {char_data['name']}")
            print(f"✅ Bio: {char_data['bio']}")
            print(f"✅ Is Cobra: {char_data['is_cobra']}")
            if char_data['image_url']:
                print(f"✅ Image: Available")
            print(f"✅ Wiki: {char_data['wiki_url']}")
    
    # Test random character
    print(f"\n🎲 Random Cobra Character:")
    random_char = gijoe_api.get_random_cobra_character()
    if "error" not in random_char:
        print(f"✅ {random_char['name']}: {random_char['bio']}")
    
    # Test search
    print(f"\n🔍 Searching for Cobra characters:")
    search_results = gijoe_api.search_cobra_characters("Cobra")
    for i, result in enumerate(search_results[:3]):  # Show first 3 results
        if "error" not in result:
            print(f"✅ {i+1}. {result['name']}")
        else:
            print(f"❌ {result['error']}")
