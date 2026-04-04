#!/usr/bin/env python3
"""
iTunes Search API Client for ASO Research

Free, official Apple API for fetching app metadata, ratings, and competitor data.
No authentication required.

Usage:
    from lib.itunes_api import iTunesAPI

    api = iTunesAPI()
    results = api.search_apps("productivity", limit=10)
    competitor = api.get_app_by_id("572688855")
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AppData:
    """Structured app data from iTunes API."""
    app_id: str
    app_name: str
    bundle_id: str
    description: str
    rating: float
    rating_count: int
    price: float
    currency: str
    genres: List[str]
    primary_genre: str
    developer: str
    version: str
    release_date: str
    icon_url: str
    screenshots: List[str]
    app_store_url: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app_id": self.app_id,
            "app_name": self.app_name,
            "bundle_id": self.bundle_id,
            "description": self.description,
            "rating": self.rating,
            "rating_count": self.rating_count,
            "price": self.price,
            "currency": self.currency,
            "genres": self.genres,
            "primary_genre": self.primary_genre,
            "developer": self.developer,
            "version": self.version,
            "release_date": self.release_date,
            "icon_url": self.icon_url,
            "screenshots": self.screenshots,
            "app_store_url": self.app_store_url,
        }


class iTunesAPI:
    """Client for iTunes Search API."""

    BASE_URL = "https://itunes.apple.com"

    def __init__(self, country: str = "us", timeout: int = 10):
        """
        Initialize iTunes API client.

        Args:
            country: Two-letter country code (us, gb, de, etc.)
            timeout: Request timeout in seconds
        """
        self.country = country
        self.timeout = timeout

    def _request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request and return JSON response."""
        params["country"] = self.country
        query = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}/{endpoint}?{query}"

        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "ASO-Skill/1.0"
            })
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise ConnectionError(f"iTunes API request failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")

    def _parse_app(self, data: Dict[str, Any]) -> AppData:
        """Parse API response into AppData object."""
        return AppData(
            app_id=str(data.get("trackId", "")),
            app_name=data.get("trackName", ""),
            bundle_id=data.get("bundleId", ""),
            description=data.get("description", ""),
            rating=data.get("averageUserRating", 0.0),
            rating_count=data.get("userRatingCount", 0),
            price=data.get("price", 0.0),
            currency=data.get("currency", "USD"),
            genres=data.get("genres", []),
            primary_genre=data.get("primaryGenreName", ""),
            developer=data.get("artistName", ""),
            version=data.get("version", ""),
            release_date=data.get("releaseDate", ""),
            icon_url=data.get("artworkUrl512", data.get("artworkUrl100", "")),
            screenshots=data.get("screenshotUrls", []),
            app_store_url=data.get("trackViewUrl", ""),
        )

    def search_apps(
        self,
        term: str,
        limit: int = 10,
        entity: str = "software"
    ) -> List[AppData]:
        """
        Search for apps by keyword.

        Args:
            term: Search term (keyword, app name, etc.)
            limit: Max results (1-200)
            entity: software (iOS), macSoftware (Mac), iPadSoftware (iPad)

        Returns:
            List of AppData objects
        """
        response = self._request("search", {
            "term": term,
            "entity": entity,
            "limit": min(limit, 200),
        })

        return [self._parse_app(r) for r in response.get("results", [])]

    def get_app_by_id(self, app_id: str) -> Optional[AppData]:
        """
        Get app by iTunes ID.

        Args:
            app_id: iTunes app ID (e.g., "572688855" for Todoist)

        Returns:
            AppData object or None if not found
        """
        response = self._request("lookup", {"id": app_id})
        results = response.get("results", [])

        if results:
            return self._parse_app(results[0])
        return None

    def get_apps_by_ids(self, app_ids: List[str]) -> List[AppData]:
        """
        Get multiple apps by IDs.

        Args:
            app_ids: List of iTunes app IDs

        Returns:
            List of AppData objects
        """
        if not app_ids:
            return []

        response = self._request("lookup", {"id": ",".join(app_ids)})
        return [self._parse_app(r) for r in response.get("results", [])]

    def get_top_apps_in_category(
        self,
        category: str,
        limit: int = 10
    ) -> List[AppData]:
        """
        Get top apps in a category by searching category name.

        Args:
            category: Category name (e.g., "Productivity", "Health & Fitness")
            limit: Max results

        Returns:
            List of AppData objects sorted by rating count
        """
        apps = self.search_apps(category, limit=limit * 2)

        # Filter by category match and sort by rating count
        filtered = [
            app for app in apps
            if category.lower() in app.primary_genre.lower()
            or category.lower() in " ".join(app.genres).lower()
        ]

        return sorted(filtered, key=lambda x: x.rating_count, reverse=True)[:limit]

    def analyze_competitors(
        self,
        competitor_names: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze competitor apps.

        Args:
            competitor_names: List of competitor app names

        Returns:
            Analysis dict with apps, keywords, gaps, and best practices
        """
        competitors = []
        all_keywords = set()

        for name in competitor_names:
            results = self.search_apps(name, limit=3)
            if results:
                # Find best match by name similarity
                best_match = min(
                    results,
                    key=lambda x: len(set(name.lower().split()) - set(x.app_name.lower().split()))
                )
                competitors.append(best_match)

                # Extract keywords from title and description
                title_words = set(best_match.app_name.lower().split())
                desc_words = set(best_match.description.lower().split())

                # Filter common words and add to keywords
                stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "it", "your", "you", "app", "-", "&", "|"}
                keywords = (title_words | desc_words) - stop_words
                all_keywords.update(keywords)

        return {
            "competitors": [c.to_dict() for c in competitors],
            "common_keywords": list(all_keywords)[:50],
            "average_rating": sum(c.rating for c in competitors) / len(competitors) if competitors else 0,
            "average_rating_count": sum(c.rating_count for c in competitors) / len(competitors) if competitors else 0,
            "fetched_at": datetime.now().isoformat(),
        }

    def extract_keywords_from_description(
        self,
        description: str,
        min_length: int = 3
    ) -> List[str]:
        """
        Extract potential keywords from app description.

        Args:
            description: App description text
            min_length: Minimum keyword length

        Returns:
            List of extracted keywords
        """
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "it", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "must", "shall", "can", "need",
            "your", "you", "we", "our", "they", "their", "this", "that", "these",
            "those", "what", "which", "who", "whom", "when", "where", "why", "how",
            "all", "each", "every", "both", "few", "more", "most", "other", "some",
            "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
            "very", "just", "also", "now", "app", "apps", "new", "like", "get",
        }

        # Clean and tokenize
        words = description.lower()
        for char in ".,!?;:()[]{}\"'`~@#$%^&*+=<>/\\|":
            words = words.replace(char, " ")

        tokens = words.split()

        # Filter and deduplicate
        keywords = []
        seen = set()

        for word in tokens:
            if (
                len(word) >= min_length
                and word not in stop_words
                and word not in seen
                and word.isalpha()
            ):
                keywords.append(word)
                seen.add(word)

        return keywords[:100]


def main():
    """Test iTunes API client."""
    api = iTunesAPI()

    print("Testing iTunes Search API...")
    print("-" * 50)

    # Test search
    print("\n1. Searching for 'productivity' apps:")
    apps = api.search_apps("productivity", limit=5)
    for app in apps:
        print(f"   - {app.app_name}: {app.rating}★ ({app.rating_count} ratings)")

    # Test competitor analysis
    print("\n2. Analyzing competitors:")
    analysis = api.analyze_competitors(["Todoist", "Any.do", "Microsoft To Do"])
    print(f"   - Found {len(analysis['competitors'])} competitors")
    print(f"   - Average rating: {analysis['average_rating']:.1f}★")
    print(f"   - Common keywords: {analysis['common_keywords'][:10]}")

    print("\n" + "-" * 50)
    print("iTunes API test complete!")


if __name__ == "__main__":
    main()
