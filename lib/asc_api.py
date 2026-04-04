#!/usr/bin/env python3
"""
App Store Connect API Client for ASO Submission

Handles authentication via API Key (JWT) and web session for:
- Privacy nutrition label configuration
- Metadata submission
- App creation and management

Requires credentials at ~/.aso/credentials.json

Usage:
    from lib.asc_api import ASCClient, generate_token

    token = generate_token()
    client = ASCClient(token)
    apps = client.list_apps()
"""

import json
import os
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# =============================================================================
# JWT Token Generation
# =============================================================================

def generate_token() -> str:
    """Generate JWT token for App Store Connect API."""
    try:
        import jwt
    except ImportError:
        raise ImportError("PyJWT required. Install with: pip3 install PyJWT cryptography")

    creds_path = os.path.expanduser("~/.aso/credentials.json")

    if not os.path.exists(creds_path):
        raise FileNotFoundError("No credentials found. Run /aso-setup first.")

    with open(creds_path) as f:
        creds = json.load(f)

    pk_path = os.path.expanduser(creds["privateKeyPath"])
    with open(pk_path) as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "iss": creds["issuerId"],
        "iat": now,
        "exp": now + 1200,  # 20 minutes
        "aud": "appstoreconnect-v1"
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm="ES256",
        headers={"kid": creds["keyId"], "typ": "JWT"}
    )


# =============================================================================
# Privacy Configuration
# =============================================================================

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


# =============================================================================
# API Clients
# =============================================================================

class ASCClient:
    """App Store Connect API client using JWT authentication."""

    BASE_URL = "https://api.appstoreconnect.apple.com/v1"

    def __init__(self, token: str = None):
        """
        Initialize ASC client.

        Args:
            token: JWT token for authentication
        """
        self.token = token

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Make authenticated API request."""
        if not self.token:
            self.token = generate_token()

        url = f"{self.BASE_URL}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
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
                raise AuthenticationError("Token expired or invalid. Regenerate with generate_token().")
            elif e.code == 409:
                raise ConflictError(f"Conflict: {error_body[:500]}")
            else:
                raise APIError(f"HTTP {e.code}: {error_body[:500]}")

    def list_apps(self) -> List[Dict[str, Any]]:
        """List all apps in account."""
        response = self._request("GET", "apps")
        return response.get("data", [])

    def get_app(self, app_id: str) -> Dict[str, Any]:
        """Get app details by ID."""
        return self._request("GET", f"apps/{app_id}")

    def get_app_versions(self, app_id: str) -> List[Dict[str, Any]]:
        """Get all versions for an app."""
        response = self._request("GET", f"apps/{app_id}/appStoreVersions")
        return response.get("data", [])

    def get_version_localizations(self, version_id: str) -> List[Dict[str, Any]]:
        """Get localizations for a version."""
        response = self._request("GET", f"appStoreVersions/{version_id}/appStoreVersionLocalizations")
        return response.get("data", [])

    def update_localization(self, loc_id: str, attributes: Dict[str, str]) -> Dict[str, Any]:
        """Update version localization (description, keywords, etc.)."""
        data = {
            "data": {
                "type": "appStoreVersionLocalizations",
                "id": loc_id,
                "attributes": attributes
            }
        }
        return self._request("PATCH", f"appStoreVersionLocalizations/{loc_id}", data)

    def get_app_infos(self, app_id: str) -> List[Dict[str, Any]]:
        """Get app info objects."""
        response = self._request("GET", f"apps/{app_id}/appInfos")
        return response.get("data", [])

    def get_app_info_localizations(self, app_info_id: str) -> List[Dict[str, Any]]:
        """Get app info localizations (title, subtitle)."""
        response = self._request("GET", f"appInfos/{app_info_id}/appInfoLocalizations")
        return response.get("data", [])

    def update_app_info_localization(self, loc_id: str, attributes: Dict[str, str]) -> Dict[str, Any]:
        """Update app info localization (name, subtitle, privacy URL)."""
        data = {
            "data": {
                "type": "appInfoLocalizations",
                "id": loc_id,
                "attributes": attributes
            }
        }
        return self._request("PATCH", f"appInfoLocalizations/{loc_id}", data)

    def list_iaps(self, app_id: str) -> List[Dict[str, Any]]:
        """List in-app purchases."""
        response = self._request("GET", f"apps/{app_id}/inAppPurchasesV2")
        return response.get("data", [])

    def list_subscription_groups(self, app_id: str) -> Dict[str, Any]:
        """List subscription groups with subscriptions."""
        return self._request("GET", f"apps/{app_id}/subscriptionGroups?include=subscriptions")


class IrisClient:
    """App Store Connect iris API client using web session authentication."""

    IRIS_BASE_URL = "https://appstoreconnect.apple.com/iris/v1"
    SESSION_PATH = os.path.expanduser("~/.aso/web-session.json")

    def __init__(self, session_path: str = None):
        """
        Initialize iris client.

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
            session = json.load(f)

        # Handle simple format: {"cookies": "cookie_string"}
        if "cookies" in session and isinstance(session["cookies"], str):
            self._cookies = session["cookies"]
            return

        # Handle complex format (from browser export)
        if "sessions" in session:
            sess = session['sessions'][session['last_key']]
            cookies = []
            for cookie_list in sess['cookies'].values():
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
                raise AuthenticationError("Session expired. Re-export cookies from browser.")
            elif e.code == 409:
                raise ConflictError(f"Conflict: {error_body[:500]}")
            else:
                raise APIError(f"HTTP {e.code}: {error_body[:500]}")

    def get_privacy(self, app_id: str) -> Dict[str, Any]:
        """Get privacy declarations for app."""
        return self._request("GET", f"apps/{app_id}/appPrivacy")

    def update_privacy(self, privacy_id: str, data_usages: List[Dict]) -> Dict[str, Any]:
        """Update privacy declarations."""
        data = {
            "data": {
                "type": "appPrivacies",
                "id": privacy_id,
                "attributes": {
                    "dataUsages": data_usages
                }
            }
        }
        return self._request("PATCH", f"appPrivacies/{privacy_id}", data)

    def attach_subscription(self, sub_id: str) -> Dict[str, Any]:
        """Attach subscription to next version."""
        data = {
            "data": {
                "type": "subscriptionSubmissions",
                "attributes": {"submitWithNextAppStoreVersion": True},
                "relationships": {
                    "subscription": {"data": {"type": "subscriptions", "id": sub_id}}
                }
            }
        }
        return self._request("POST", "subscriptionSubmissions", data)

    def attach_iap(self, iap_id: str) -> Dict[str, Any]:
        """Attach IAP to next version."""
        data = {
            "data": {
                "type": "inAppPurchaseSubmissions",
                "attributes": {"submitWithNextAppStoreVersion": True},
                "relationships": {
                    "inAppPurchaseV2": {"data": {"type": "inAppPurchases", "id": iap_id}}
                }
            }
        }
        return self._request("POST", "inAppPurchaseSubmissions", data)


# =============================================================================
# Exceptions
# =============================================================================

class AuthenticationError(Exception):
    """Raised when session is invalid or expired."""
    pass


class ConflictError(Exception):
    """Raised when there's a conflict (e.g., duplicate app)."""
    pass


class APIError(Exception):
    """Raised for general API errors."""
    pass


# =============================================================================
# Utility Functions
# =============================================================================

def check_credentials() -> Dict[str, bool]:
    """Check what credentials are configured."""
    return {
        "api_key": os.path.exists(os.path.expanduser("~/.aso/credentials.json")),
        "web_session": os.path.exists(os.path.expanduser("~/.aso/web-session.json")),
    }


def main():
    """Test ASC API client."""
    print("Testing ASC API Client...")
    print("-" * 50)

    # Check credentials
    print("\n1. Checking credentials...")
    creds = check_credentials()
    print(f"   API Key: {'✅' if creds['api_key'] else '❌'}")
    print(f"   Web Session: {'✅' if creds['web_session'] else '❌'}")

    # Test JWT generation
    if creds['api_key']:
        print("\n2. Testing JWT generation...")
        try:
            token = generate_token()
            print(f"   ✅ Token generated ({len(token)} chars)")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Test API connection
    if creds['api_key']:
        print("\n3. Testing API connection...")
        try:
            client = ASCClient()
            apps = client.list_apps()
            print(f"   ✅ Connected! Found {len(apps)} app(s)")
            for app in apps[:3]:
                print(f"      - {app['attributes']['name']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Sample privacy configs
    print("\n4. Sample Privacy Configurations:")

    print("\n   No data collected:")
    config_none = PrivacyConfig.no_data_collected()
    print(f"   {config_none.to_json()}")

    print("\n   Basic analytics:")
    config_basic = PrivacyConfig.basic_analytics()
    print(f"   {config_basic.to_json()}")

    print("\n" + "-" * 50)
    print("ASC API Client test complete!")


if __name__ == "__main__":
    main()
