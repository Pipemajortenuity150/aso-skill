#!/usr/bin/env python3
"""
Keyword Analysis Engine for ASO

Analyzes keywords for relevance, competition, and strategic placement.
Generates prioritized keyword lists with implementation recommendations.

Usage:
    from lib.keyword_engine import KeywordEngine

    engine = KeywordEngine()
    analysis = engine.analyze_keywords(
        seed_keywords=["task manager", "productivity"],
        app_features=["AI scheduling", "team collaboration"]
    )
"""

import re
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    """Keyword priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Placement(Enum):
    """Recommended keyword placement."""
    TITLE = "title"
    SUBTITLE = "subtitle"
    KEYWORD_FIELD = "keyword_field"
    DESCRIPTION = "description"


@dataclass
class Keyword:
    """Analyzed keyword with metrics and recommendations."""
    keyword: str
    relevance: float  # 0.0 - 1.0
    competition: str  # low, medium, high
    priority: Priority
    placements: List[Placement]
    estimated_volume: str  # low, medium, high, very_high
    word_count: int
    is_long_tail: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "relevance": self.relevance,
            "competition": self.competition,
            "priority": self.priority.value,
            "placements": [p.value for p in self.placements],
            "estimated_volume": self.estimated_volume,
            "word_count": self.word_count,
            "is_long_tail": self.is_long_tail,
        }


@dataclass
class KeywordAnalysis:
    """Complete keyword analysis result."""
    primary_keywords: List[Keyword] = field(default_factory=list)
    secondary_keywords: List[Keyword] = field(default_factory=list)
    long_tail_keywords: List[Keyword] = field(default_factory=list)
    apple_keyword_field: str = ""
    apple_title_suggestion: str = ""
    apple_subtitle_suggestion: str = ""
    google_title_suggestion: str = ""
    total_unique_keywords: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_keywords": [k.to_dict() for k in self.primary_keywords],
            "secondary_keywords": [k.to_dict() for k in self.secondary_keywords],
            "long_tail_keywords": [k.to_dict() for k in self.long_tail_keywords],
            "apple_keyword_field": self.apple_keyword_field,
            "apple_title_suggestion": self.apple_title_suggestion,
            "apple_subtitle_suggestion": self.apple_subtitle_suggestion,
            "google_title_suggestion": self.google_title_suggestion,
            "total_unique_keywords": self.total_unique_keywords,
        }


class KeywordEngine:
    """Engine for ASO keyword analysis and optimization."""

    # Character limits
    APPLE_TITLE_LIMIT = 30
    APPLE_SUBTITLE_LIMIT = 30
    APPLE_KEYWORD_LIMIT = 100
    GOOGLE_TITLE_LIMIT = 50
    GOOGLE_SHORT_LIMIT = 80

    # Common stop words to filter
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "it", "app", "apps", "best", "free", "new",
        "top", "your", "my", "our", "pro", "plus", "premium", "lite",
    }

    # High-volume category indicators
    CATEGORY_VOLUME = {
        "productivity": "high",
        "fitness": "high",
        "health": "high",
        "game": "very_high",
        "social": "very_high",
        "photo": "high",
        "music": "high",
        "finance": "medium",
        "education": "medium",
        "business": "medium",
        "utility": "medium",
        "weather": "medium",
    }

    def __init__(self):
        self._used_words: Set[str] = set()

    def analyze_keywords(
        self,
        seed_keywords: List[str],
        app_features: List[str],
        app_name: str = "",
        category: str = "",
        competitor_keywords: List[str] = None,
    ) -> KeywordAnalysis:
        """
        Analyze and prioritize keywords for ASO.

        Args:
            seed_keywords: Initial keyword ideas
            app_features: App features to extract keywords from
            app_name: App name (for title suggestions)
            category: App category (for volume estimation)
            competitor_keywords: Keywords used by competitors

        Returns:
            KeywordAnalysis with prioritized keywords and suggestions
        """
        self._used_words = set()
        competitor_keywords = competitor_keywords or []

        # Collect all potential keywords
        all_keywords = self._collect_keywords(
            seed_keywords, app_features, competitor_keywords
        )

        # Analyze each keyword
        analyzed = []
        for kw in all_keywords:
            analyzed.append(self._analyze_single_keyword(
                kw, seed_keywords, app_features, category, competitor_keywords
            ))

        # Sort by relevance and priority
        analyzed.sort(key=lambda x: (x.relevance, x.priority == Priority.CRITICAL), reverse=True)

        # Categorize keywords
        primary = [k for k in analyzed if k.priority in (Priority.CRITICAL, Priority.HIGH)][:10]
        secondary = [k for k in analyzed if k.priority == Priority.MEDIUM][:15]
        long_tail = [k for k in analyzed if k.is_long_tail][:10]

        # Generate Apple keyword field (100 chars, no spaces after commas)
        keyword_field = self._generate_keyword_field(analyzed, primary)

        # Generate title/subtitle suggestions
        title_suggestion = self._generate_title_suggestion(app_name, primary)
        subtitle_suggestion = self._generate_subtitle_suggestion(primary, title_suggestion)
        google_title = self._generate_google_title(app_name, primary)

        return KeywordAnalysis(
            primary_keywords=primary,
            secondary_keywords=secondary,
            long_tail_keywords=long_tail,
            apple_keyword_field=keyword_field,
            apple_title_suggestion=title_suggestion,
            apple_subtitle_suggestion=subtitle_suggestion,
            google_title_suggestion=google_title,
            total_unique_keywords=len(analyzed),
        )

    def _collect_keywords(
        self,
        seed_keywords: List[str],
        app_features: List[str],
        competitor_keywords: List[str],
    ) -> List[str]:
        """Collect and deduplicate all potential keywords."""
        keywords = set()

        # Add seed keywords
        for kw in seed_keywords:
            keywords.add(kw.lower().strip())

        # Extract keywords from features
        for feature in app_features:
            words = self._tokenize(feature)
            keywords.update(words)

            # Also add full feature as potential long-tail
            clean_feature = feature.lower().strip()
            if 2 <= len(clean_feature.split()) <= 4:
                keywords.add(clean_feature)

        # Add competitor keywords
        for kw in competitor_keywords:
            clean_kw = kw.lower().strip()
            if clean_kw not in self.STOP_WORDS:
                keywords.add(clean_kw)

        # Generate variations
        variations = set()
        for kw in keywords:
            # Add without 's' if present
            if kw.endswith('s') and len(kw) > 3:
                variations.add(kw[:-1])
            # Add common variations
            if "task" in kw:
                variations.add(kw.replace("task", "todo"))
            if "todo" in kw:
                variations.add(kw.replace("todo", "task"))

        keywords.update(variations)

        # Filter and return
        return [
            kw for kw in keywords
            if kw not in self.STOP_WORDS
            and len(kw) >= 2
            and kw.replace(" ", "").isalnum()
        ]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into keywords."""
        # Clean text
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)

        # Split and filter
        words = text.split()
        return [w for w in words if w not in self.STOP_WORDS and len(w) >= 2]

    def _analyze_single_keyword(
        self,
        keyword: str,
        seed_keywords: List[str],
        app_features: List[str],
        category: str,
        competitor_keywords: List[str],
    ) -> Keyword:
        """Analyze a single keyword."""
        word_count = len(keyword.split())
        is_long_tail = word_count >= 3

        # Calculate relevance
        relevance = self._calculate_relevance(
            keyword, seed_keywords, app_features
        )

        # Estimate competition
        competition = self._estimate_competition(
            keyword, competitor_keywords, word_count
        )

        # Estimate volume
        volume = self._estimate_volume(keyword, category)

        # Determine priority
        priority = self._determine_priority(relevance, competition, volume)

        # Recommend placements
        placements = self._recommend_placements(
            keyword, priority, word_count
        )

        return Keyword(
            keyword=keyword,
            relevance=relevance,
            competition=competition,
            priority=priority,
            placements=placements,
            estimated_volume=volume,
            word_count=word_count,
            is_long_tail=is_long_tail,
        )

    def _calculate_relevance(
        self,
        keyword: str,
        seed_keywords: List[str],
        app_features: List[str],
    ) -> float:
        """Calculate keyword relevance score (0.0 - 1.0)."""
        score = 0.0

        # Check if in seed keywords
        if keyword in [sk.lower() for sk in seed_keywords]:
            score += 0.5

        # Check if matches features
        feature_text = " ".join(app_features).lower()
        if keyword in feature_text:
            score += 0.3

        # Partial matches
        keyword_words = set(keyword.split())
        seed_words = set(" ".join(seed_keywords).lower().split())
        feature_words = set(feature_text.split())

        overlap_seed = len(keyword_words & seed_words) / max(len(keyword_words), 1)
        overlap_feature = len(keyword_words & feature_words) / max(len(keyword_words), 1)

        score += overlap_seed * 0.15
        score += overlap_feature * 0.15

        return min(score, 1.0)

    def _estimate_competition(
        self,
        keyword: str,
        competitor_keywords: List[str],
        word_count: int,
    ) -> str:
        """Estimate keyword competition level."""
        # Long-tail = lower competition
        if word_count >= 3:
            return "low"

        # Used by competitors = higher competition
        comp_lower = [ck.lower() for ck in competitor_keywords]
        if keyword in comp_lower:
            return "high"

        # Generic single words = high competition
        if word_count == 1 and keyword in {
            "productivity", "fitness", "health", "game", "social",
            "photo", "music", "task", "todo", "calendar", "workout",
        }:
            return "high"

        return "medium"

    def _estimate_volume(self, keyword: str, category: str) -> str:
        """Estimate keyword search volume."""
        # Check category indicators
        for cat, vol in self.CATEGORY_VOLUME.items():
            if cat in keyword or cat in category.lower():
                return vol

        # Default based on word count
        word_count = len(keyword.split())
        if word_count == 1:
            return "medium"
        elif word_count == 2:
            return "medium"
        else:
            return "low"

    def _determine_priority(
        self,
        relevance: float,
        competition: str,
        volume: str,
    ) -> Priority:
        """Determine keyword priority level."""
        # High relevance + low competition = critical
        if relevance >= 0.8 and competition == "low":
            return Priority.CRITICAL

        # High relevance = high priority
        if relevance >= 0.6:
            return Priority.HIGH

        # Medium relevance or low competition = medium
        if relevance >= 0.3 or competition == "low":
            return Priority.MEDIUM

        return Priority.LOW

    def _recommend_placements(
        self,
        keyword: str,
        priority: Priority,
        word_count: int,
    ) -> List[Placement]:
        """Recommend where to place keyword."""
        placements = []

        if priority == Priority.CRITICAL:
            placements.append(Placement.TITLE)
            placements.append(Placement.DESCRIPTION)
        elif priority == Priority.HIGH:
            if word_count <= 2:
                placements.append(Placement.SUBTITLE)
            placements.append(Placement.KEYWORD_FIELD)
            placements.append(Placement.DESCRIPTION)
        elif priority == Priority.MEDIUM:
            placements.append(Placement.KEYWORD_FIELD)
            placements.append(Placement.DESCRIPTION)
        else:
            placements.append(Placement.DESCRIPTION)

        return placements

    def _generate_keyword_field(
        self,
        all_keywords: List[Keyword],
        primary_keywords: List[Keyword],
    ) -> str:
        """Generate Apple keyword field (100 chars max, no spaces after commas)."""
        # Start with secondary keywords (primary go in title/subtitle)
        candidates = [
            k.keyword for k in all_keywords
            if k not in primary_keywords
            and Placement.KEYWORD_FIELD in k.placements
        ]

        # Build field within limit
        field_keywords = []
        current_length = 0

        for kw in candidates:
            # Calculate length with comma
            addition_length = len(kw) + (1 if field_keywords else 0)

            if current_length + addition_length <= self.APPLE_KEYWORD_LIMIT:
                field_keywords.append(kw)
                current_length += addition_length

        return ",".join(field_keywords)

    def _generate_title_suggestion(
        self,
        app_name: str,
        primary_keywords: List[Keyword],
    ) -> str:
        """Generate Apple title suggestion (30 chars max)."""
        if not app_name:
            app_name = "App"

        # Get top keyword
        top_kw = primary_keywords[0].keyword if primary_keywords else ""

        # Try formats
        formats = [
            f"{app_name} - {top_kw.title()}",
            f"{app_name}: {top_kw.title()}",
            f"{top_kw.title()} {app_name}",
            app_name,
        ]

        for fmt in formats:
            if len(fmt) <= self.APPLE_TITLE_LIMIT:
                return fmt

        # Truncate app name if needed
        return app_name[:self.APPLE_TITLE_LIMIT]

    def _generate_subtitle_suggestion(
        self,
        primary_keywords: List[Keyword],
        title: str,
    ) -> str:
        """Generate Apple subtitle suggestion (30 chars max, no overlap with title)."""
        title_words = set(title.lower().split())

        # Find keywords not in title
        available = [
            k for k in primary_keywords
            if not set(k.keyword.lower().split()) & title_words
        ]

        if not available:
            return "Smart & Simple"

        # Build subtitle
        subtitle_parts = []
        current_length = 0

        for kw in available[:3]:
            word = kw.keyword.title()
            addition = len(word) + (3 if subtitle_parts else 0)  # " & " separator

            if current_length + addition <= self.APPLE_SUBTITLE_LIMIT:
                subtitle_parts.append(word)
                current_length += addition

        return " & ".join(subtitle_parts) if subtitle_parts else "Smart & Simple"

    def _generate_google_title(
        self,
        app_name: str,
        primary_keywords: List[Keyword],
    ) -> str:
        """Generate Google Play title suggestion (50 chars max)."""
        if not app_name:
            app_name = "App"

        # Get top 2 keywords
        kw1 = primary_keywords[0].keyword.title() if primary_keywords else ""
        kw2 = primary_keywords[1].keyword.title() if len(primary_keywords) > 1 else ""

        # Try formats
        formats = [
            f"{app_name}: {kw1} & {kw2}",
            f"{app_name} - {kw1} {kw2}",
            f"{app_name}: {kw1}",
            app_name,
        ]

        for fmt in formats:
            if len(fmt) <= self.GOOGLE_TITLE_LIMIT:
                return fmt

        return app_name[:self.GOOGLE_TITLE_LIMIT]

    def validate_no_duplicates(
        self,
        title: str,
        subtitle: str,
        keywords: str,
    ) -> Tuple[bool, List[str]]:
        """
        Validate no duplicate words across Apple metadata fields.

        Returns:
            Tuple of (is_valid, list_of_duplicates)
        """
        title_words = set(title.lower().split())
        subtitle_words = set(subtitle.lower().split())
        keyword_words = set(keywords.lower().replace(",", " ").split())

        duplicates = []

        # Check title vs subtitle
        overlap_ts = title_words & subtitle_words
        if overlap_ts:
            duplicates.extend([f"title/subtitle: {w}" for w in overlap_ts])

        # Check title vs keywords
        overlap_tk = title_words & keyword_words
        if overlap_tk:
            duplicates.extend([f"title/keywords: {w}" for w in overlap_tk])

        # Check subtitle vs keywords
        overlap_sk = subtitle_words & keyword_words
        if overlap_sk:
            duplicates.extend([f"subtitle/keywords: {w}" for w in overlap_sk])

        return (len(duplicates) == 0, duplicates)


def main():
    """Test keyword engine."""
    engine = KeywordEngine()

    print("Testing Keyword Engine...")
    print("-" * 50)

    analysis = engine.analyze_keywords(
        seed_keywords=["task manager", "productivity", "todo list"],
        app_features=[
            "AI-powered task prioritization",
            "Team collaboration",
            "Calendar integration",
            "Smart reminders",
        ],
        app_name="TaskFlow",
        category="Productivity",
        competitor_keywords=["todo", "organize", "planner", "schedule"],
    )

    print("\nPrimary Keywords:")
    for kw in analysis.primary_keywords[:5]:
        print(f"  - {kw.keyword}: relevance={kw.relevance:.2f}, competition={kw.competition}")

    print(f"\nApple Keyword Field ({len(analysis.apple_keyword_field)}/100 chars):")
    print(f"  {analysis.apple_keyword_field}")

    print(f"\nTitle Suggestion: {analysis.apple_title_suggestion}")
    print(f"Subtitle Suggestion: {analysis.apple_subtitle_suggestion}")
    print(f"Google Title: {analysis.google_title_suggestion}")

    # Validate
    valid, dupes = engine.validate_no_duplicates(
        analysis.apple_title_suggestion,
        analysis.apple_subtitle_suggestion,
        analysis.apple_keyword_field,
    )
    print(f"\nValidation: {'PASS' if valid else 'FAIL'}")
    if dupes:
        print(f"  Duplicates: {dupes}")

    print("\n" + "-" * 50)
    print("Keyword Engine test complete!")


if __name__ == "__main__":
    main()
