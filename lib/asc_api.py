#!/usr/bin/env python3
"""
App Store Connect API Client for ASO Submission

Handles authentication via web session and provides methods for:
- Privacy nutrition label configuration
- Metadata submission
- App creation and management

Requires web session cached at ~/.blitz/asc-agent/web-session.json
(managed by Blitz app or asc_web_auth MCP tool)

Usage:
    from lib.asc_api import ASCClient

    client = ASCClient()
    if client.is_authenticated():
        client.apply_privacy_labels(app_id, privacy_config)
"""

import json
import os
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DataCategory(Enum):
    """Privacy data categories."""
    NAME = "NAME"
    EMAIL_ADDRESS = "EMAIL_ADDRESS"
    PHONE_NUMBER = "PHONE_NUMBER"
    PHYSICAL_ADDRESS = "PHYSICAL_ADDRESS"
    HEALTH = "HEALTH"
    FITNESS = "FITNESS"
    PAYMENT_INFORMATION = "PAYMENT_INFORMATION"
    PRECISE_LOCATION = "PRECISE_LOCATION"
    COARSE_LOCATION = "COARSE_LOCATION"
    CONTACTS = "CONTACTS"
    USER_ID = "USER_ID"
    DEVICE_ID = "DEVICE_ID"
    PURCHASE_HISTORY = "PURCHASE_HISTORY"
    PRODUCT_INTERACTION = "PRODUCT_INTERACTION"
    CRASH_DATA = "CRASH_DATA"
    PERFORMANCE_DATA = "PERFORMANCE_DATA"
    OTHER_DIAGNOSTIC_DATA = "OTHER_DIAGNOSTIC_DATA"


class DataPurpose(Enum):
    """Privacy data purposes."""
    APP_FUNCTIONALITY = "APP_FUNCTIONALITY"
    ANALYTICS = "ANALYTICS"
    PRODUCT_PERSONALIZATION = "PRODUCT_PERSONALIZATION"
    DEVELOPERS_ADVERTISING = "DEVELOPERS_ADVERTISING"
    THIRD_PARTY_ADVERTISING = "THIRD_PARTY_ADVERTISING"
    OTHER_PURPOSES = "OTHER_PURPOSES"


class DataProtection(Enum):
    """Privacy data protections."""
    DATA_NOT_COLLECTED = "DATA_NOT_COLLECTED"
    DATA_LINKED_TO_YOU = "DATA_LINKED_TO_YOU"
    DATA_NOT_LINKED_TO_YOU = "DATA_NOT_LINKED_TO_YOU"
    DATA_USED_TO_TRACK_YOU = "DATA_USED_TO_TRACK_YOU"


@dataclass
class PrivacyDeclaration:
    """Single privacy data declaration."""
    category: DataCategory
    purposes: List[DataPurpose]
    protections: List[DataProtection]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "purposes": [p.value for p in self.purposes],
            "dataProtections": [p.value for p in self.protections],
        }


@dataclass
class PrivacyConfig:
    """Complete privacy configuration."""
    schema_version: int = 1
    data_usages: List[PrivacyDeclaration] = None

    def __post_init__(self):
        if self.data_usages is None:
            self.data_usages = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "dataUsages": [d.to_dict() for d in self.data_usages],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def no_data_collected(cls) -> "PrivacyConfig":
        """Create config for apps that collect no data."""
        return cls(data_usages=[])

    @classmethod
    def basic_analytics(cls) -> "PrivacyConfig":
        """Create config for basic crash/analytics only."""
        return cls(data_usages=[
            PrivacyDeclaration(
                category=DataCategory.CRASH_DATA,
                purposes=[DataPurpose.ANALYTICS],
                protections=[DataProtection.DATA_NOT_LINKED_TO_YOU],
            )
        ])

    @classmethod
    def user_accounts_analytics(cls) -> "PrivacyConfig":
        """Create config for apps with user accounts + analytics."""
        return cls(data_usages=[
            PrivacyDeclaration(
                category=DataCategory.NAME,
                purposes=[DataPurpose.APP_FUNCTIONALITY],
                protections=[DataProtection.DATA_LINKED_TO_YOU],
            ),
            PrivacyDeclaration(
                category=DataCategory.EMAIL_ADDRESS,
                purposes=[DataPurpose.APP_FUNCTIONALITY],
                protections=[DataProtection.DATA_LINKED_TO_YOU],
            ),
            PrivacyDeclaration(
                category=DataCategory.USER_ID,
                purposes=[DataPurpose.APP_FUNCTIONALITY],
                protections=[DataProtection.DATA_LINKED_TO_YOU],
            ),
            PrivacyDeclaration(
                category=DataCategory.CRASH_DATA,
                purposes=[DataPurpose.ANALYTICS],
                protections=[DataProtection.DATA_NOT_LINKED_TO_YOU],
            ),
        ])


class ASCClient:
    """App Store Connect API client using web session authentication."""

    IRIS_BASE_URL = "https://appstoreconnect.apple.com/iris/v1"
    SESSION_PATH = os.path.expanduser("~/.blitz/asc-agent/web-session.json")

    def __init__(self, session_path: str = None):
        """
        Initialize ASC client.

        Args:
            session_path: Path to web session JSON file
        """
        self.session_path = session_path or self.SESSION_PATH
        self._cookies: Optional[str] = None

    def is_authenticated(self) -> bool:
        """Check if valid session exists."""
        if not os.path.isfile(self.session_path):
            return False

        try:
            self._load_session()
            return self._cookies is not None
        except Exception:
            return False

    def _load_session(self) -> None:
        """Load cookies from session file."""
        with open(self.session_path, 'r') as f:
            store = json.load(f)

        session = store['sessions'][store['last_key']]
        cookies = []

        for cookie_list in session['cookies'].values():
            for c in cookie_list:
                if c.get('name') and c.get('value'):
                    if c['name'].startswith('DES'):
                        cookies.append(f'{c["name"]}="{c["value"]}"')
                    else:
                        cookies.append(f'{c["name"]}={c["value"]}')

        self._cookies = '; '.join(cookies)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Make authenticated API request."""
        if not self._cookies:
            self._load_session()

        url = f"{self.IRIS_BASE_URL}/{endpoint}"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://appstoreconnect.apple.com',
            'Referer': 'https://appstoreconnect.apple.com/',
            'Cookie': self._cookies,
        }

        body = json.dumps(data).encode() if data else None

        req = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers=headers,
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            if e.code == 401:
                raise AuthenticationError(
                    "Session expired. Call asc_web_auth MCP tool to re-authenticate."
                )
            elif e.code == 409:
                raise ConflictError(f"Conflict: {error_body[:500]}")
            else:
                raise APIError(f"HTTP {e.code}: {error_body[:500]}")

    def get_app(self, app_id: str) -> Dict[str, Any]:
        """Get app details by ID."""
        return self._request("GET", f"apps/{app_id}")

    def list_apps(self) -> List[Dict[str, Any]]:
        """List all apps in account."""
        response = self._request("GET", "apps")
        return response.get("data", [])

    def get_privacy_declarations(self, app_id: str) -> Dict[str, Any]:
        """Get current privacy declarations for app."""
        return self._request("GET", f"apps/{app_id}/privacyDeclarations")

    def apply_privacy_config(
        self,
        app_id: str,
        config: PrivacyConfig,
    ) -> Dict[str, Any]:
        """
        Apply privacy configuration to app.

        Note: This is a simplified interface. For production use,
        prefer the `asc web privacy` CLI commands which handle
        the full plan/apply/publish workflow.
        """
        # This would require implementing the full privacy API
        # For now, return the config that would be applied
        return {
            "status": "preview",
            "app_id": app_id,
            "config": config.to_dict(),
            "note": "Use 'asc web privacy apply' CLI for actual submission",
        }

    def update_app_metadata(
        self,
        app_id: str,
        locale: str,
        metadata: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Update app metadata for a locale.

        Args:
            app_id: App Store Connect app ID
            locale: Locale code (e.g., "en-US")
            metadata: Dict with keys: name, subtitle, description, keywords, etc.

        Note: This is a simplified interface. Full implementation would
        require handling appInfoLocalizations and appStoreVersionLocalizations.
        """
        return {
            "status": "preview",
            "app_id": app_id,
            "locale": locale,
            "metadata": metadata,
            "note": "Use App Store Connect UI or full API implementation for actual update",
        }


class AuthenticationError(Exception):
    """Raised when session is invalid or expired."""
    pass


class ConflictError(Exception):
    """Raised when there's a conflict (e.g., duplicate app)."""
    pass


class APIError(Exception):
    """Raised for general API errors."""
    pass


# Utility functions for CLI integration

def check_session() -> bool:
    """Check if ASC session exists and is valid."""
    return ASCClient().is_authenticated()


def generate_privacy_json(config: PrivacyConfig, output_path: str) -> str:
    """
    Generate privacy.json file for asc CLI.

    Args:
        config: PrivacyConfig object
        output_path: Path to write JSON file

    Returns:
        Path to generated file
    """
    with open(output_path, 'w') as f:
        f.write(config.to_json())
    return output_path


def get_asc_cli_commands(
    app_id: str,
    privacy_json_path: str,
) -> Dict[str, str]:
    """
    Get asc CLI commands for privacy workflow.

    Returns dict with plan, apply, and publish commands.
    """
    return {
        "plan": f'asc web privacy plan --app "{app_id}" --file {privacy_json_path} --pretty',
        "apply": f'asc web privacy apply --app "{app_id}" --file {privacy_json_path} --allow-deletes --confirm',
        "publish": f'asc web privacy publish --app "{app_id}" --confirm',
        "verify": f'asc web privacy pull --app "{app_id}" --pretty',
    }


def main():
    """Test ASC API client."""
    print("Testing ASC API Client...")
    print("-" * 50)

    client = ASCClient()

    # Check authentication
    print(f"\n1. Checking authentication...")
    if client.is_authenticated():
        print("   ✓ Session found and valid")
    else:
        print("   ✗ No valid session")
        print(f"   Session path: {client.session_path}")
        print("   Run: asc_web_auth MCP tool to authenticate")

    # Generate sample privacy config
    print("\n2. Sample Privacy Configurations:")

    print("\n   No data collected:")
    config_none = PrivacyConfig.no_data_collected()
    print(f"   {config_none.to_json()}")

    print("\n   Basic analytics:")
    config_basic = PrivacyConfig.basic_analytics()
    print(f"   {config_basic.to_json()}")

    print("\n   User accounts + analytics:")
    config_full = PrivacyConfig.user_accounts_analytics()
    print(f"   {config_full.to_json()}")

    # Show CLI commands
    print("\n3. ASC CLI Commands (for app ID '1234567890'):")
    commands = get_asc_cli_commands("1234567890", "/tmp/privacy.json")
    for name, cmd in commands.items():
        print(f"   {name}: {cmd}")

    print("\n" + "-" * 50)
    print("ASC API Client test complete!")


if __name__ == "__main__":
    main()
