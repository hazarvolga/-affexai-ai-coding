"""
Property-based tests for HTTPS enforcement in the AI Coding Platform.

These tests verify that all web services exposed through Traefik properly
enforce HTTPS and redirect HTTP requests to HTTPS.
"""

import pytest
import requests
from hypothesis import given, settings, strategies as st
from typing import List, Tuple
from urllib.parse import urlparse


# ============================================================================
# Configuration
# ============================================================================

# Domain configuration for the AI Coding Platform
PLATFORM_DOMAIN = "ai-code.affexai.tr"
PLATFORM_HTTPS_URL = f"https://{PLATFORM_DOMAIN}"
PLATFORM_HTTP_URL = f"http://{PLATFORM_DOMAIN}"

# Valid HTTP redirect status codes
# 301: Moved Permanently
# 302: Found (temporary redirect)
# 307: Temporary Redirect (preserves method)
# 308: Permanent Redirect (preserves method)
VALID_REDIRECT_CODES = [301, 302, 307, 308]


# ============================================================================
# Helper Functions
# ============================================================================

def is_https_url(url: str) -> bool:
    """
    Check if a URL uses HTTPS protocol.
    
    Args:
        url: URL to check
        
    Returns:
        True if URL uses HTTPS, False otherwise
    """
    parsed = urlparse(url)
    return parsed.scheme == "https"


def check_http_redirects_to_https(http_url: str, timeout: int = 10) -> Tuple[bool, str, int]:
    """
    Check if an HTTP URL redirects to HTTPS.
    
    Args:
        http_url: HTTP URL to test
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (redirects_to_https, location_header, status_code)
    """
    try:
        # Make request without following redirects
        response = requests.get(
            http_url,
            allow_redirects=False,
            timeout=timeout,
            verify=True
        )
        
        # Check if response is a redirect
        if response.status_code in VALID_REDIRECT_CODES:
            location = response.headers.get("Location", "")
            redirects_to_https = is_https_url(location)
            return redirects_to_https, location, response.status_code
        else:
            # Not a redirect - HTTPS not enforced
            return False, "", response.status_code
            
    except requests.exceptions.RequestException as e:
        # Network error - cannot verify
        pytest.skip(f"Cannot connect to {http_url}: {e}")


def verify_https_accessible(https_url: str, timeout: int = 10) -> Tuple[bool, int]:
    """
    Verify that an HTTPS URL is accessible and has valid certificate.
    
    Args:
        https_url: HTTPS URL to test
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (accessible, status_code)
    """
    try:
        response = requests.get(
            https_url,
            timeout=timeout,
            verify=True  # Verify SSL certificate
        )
        return True, response.status_code
    except requests.exceptions.SSLError as e:
        pytest.fail(f"SSL certificate error for {https_url}: {e}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to {https_url}: {e}")


# ============================================================================
# Hypothesis Strategies
# ============================================================================

# Strategy for URL paths to test
# Generate various paths that might be accessed on the platform
url_paths = st.sampled_from([
    "/",
    "/api",
    "/health",
    "/status",
    "/docs",
    "/settings",
])

# Strategy for query parameters
query_params = st.sampled_from([
    "",
    "?test=1",
    "?page=1&limit=10",
    "?redirect=true",
])


# ============================================================================
# Property-Based Tests
# ============================================================================

# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement
@settings(max_examples=100, deadline=None)
@given(
    path=url_paths,
    query=query_params
)
def test_http_redirects_to_https(path: str, query: str) -> None:
    """
    Property 6: HTTPS Enforcement
    
    For any web service exposed through Traefik, the service should be
    accessible via HTTPS and HTTP requests should be redirected to HTTPS.
    
    This property verifies that:
    1. HTTP requests return redirect status codes (301, 302, 307, 308)
    2. The Location header points to an HTTPS URL
    3. The redirect preserves the path and query parameters
    
    Validates: Requirements 9.1
    
    Args:
        path: URL path to test
        query: Query parameters to append
    """
    # Construct full HTTP URL
    http_url = f"{PLATFORM_HTTP_URL}{path}{query}"
    
    # Test HTTP redirect
    redirects, location, status_code = check_http_redirects_to_https(http_url)
    
    # Property: HTTP request should return a redirect status code
    assert status_code in VALID_REDIRECT_CODES, \
        f"HTTP request to {http_url} returned status {status_code}, " \
        f"expected one of {VALID_REDIRECT_CODES}"
    
    # Property: Location header should start with https://
    assert location.startswith("https://"), \
        f"Redirect location '{location}' does not use HTTPS protocol"
    
    # Property: Should redirect to HTTPS
    assert redirects, \
        f"HTTP request to {http_url} did not redirect to HTTPS. " \
        f"Location: {location}, Status: {status_code}"
    
    # Property: Redirect should preserve the path
    parsed_location = urlparse(location)
    assert parsed_location.path == path or parsed_location.path == path + "/", \
        f"Redirect changed path from '{path}' to '{parsed_location.path}'"
    
    # Property: Redirect should preserve query parameters (if any)
    if query:
        expected_query = query.lstrip("?")
        assert parsed_location.query == expected_query, \
            f"Redirect lost query parameters: expected '{expected_query}', " \
            f"got '{parsed_location.query}'"


# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement
def test_https_accessible_with_valid_certificate() -> None:
    """
    Property 6: HTTPS Enforcement (Certificate Validation)
    
    The HTTPS endpoint should be accessible with a valid SSL certificate.
    
    Validates: Requirements 9.1, 9.2
    """
    # Test HTTPS accessibility
    accessible, status_code = verify_https_accessible(PLATFORM_HTTPS_URL)
    
    # Property: HTTPS should be accessible
    assert accessible, \
        f"HTTPS URL {PLATFORM_HTTPS_URL} is not accessible"
    
    # Property: Should return successful status code
    assert 200 <= status_code < 400, \
        f"HTTPS URL returned status {status_code}, expected 2xx or 3xx"


# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement (Edge Case)
def test_https_redirect_preserves_method() -> None:
    """
    Edge case: HTTPS redirect should preserve HTTP method when possible.
    
    Status codes 307 and 308 preserve the HTTP method, while 301 and 302
    may change POST to GET. This test verifies the redirect behavior.
    
    Validates: Requirements 9.1
    """
    http_url = PLATFORM_HTTP_URL
    
    try:
        # Test GET request
        response_get = requests.get(
            http_url,
            allow_redirects=False,
            timeout=10
        )
        
        assert response_get.status_code in VALID_REDIRECT_CODES, \
            f"GET request did not redirect, status: {response_get.status_code}"
        
        location = response_get.headers.get("Location", "")
        assert location.startswith("https://"), \
            f"GET redirect location does not use HTTPS: {location}"
        
        # Test HEAD request
        response_head = requests.head(
            http_url,
            allow_redirects=False,
            timeout=10
        )
        
        assert response_head.status_code in VALID_REDIRECT_CODES, \
            f"HEAD request did not redirect, status: {response_head.status_code}"
        
        location_head = response_head.headers.get("Location", "")
        assert location_head.startswith("https://"), \
            f"HEAD redirect location does not use HTTPS: {location_head}"
        
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to {http_url}: {e}")


# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement (Edge Case)
def test_https_redirect_with_port() -> None:
    """
    Edge case: HTTP requests with explicit port 80 should also redirect to HTTPS.
    
    Validates: Requirements 9.1
    """
    http_url_with_port = f"http://{PLATFORM_DOMAIN}:80/"
    
    try:
        response = requests.get(
            http_url_with_port,
            allow_redirects=False,
            timeout=10
        )
        
        # Property: Should redirect
        assert response.status_code in VALID_REDIRECT_CODES, \
            f"HTTP request with port 80 did not redirect, status: {response.status_code}"
        
        # Property: Should redirect to HTTPS
        location = response.headers.get("Location", "")
        assert location.startswith("https://"), \
            f"Redirect location does not use HTTPS: {location}"
        
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to {http_url_with_port}: {e}")


# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement (Edge Case)
def test_https_hsts_header() -> None:
    """
    Edge case: HTTPS response should include HSTS header for enhanced security.
    
    HSTS (HTTP Strict Transport Security) tells browsers to always use HTTPS.
    
    Validates: Requirements 9.1
    """
    try:
        response = requests.get(
            PLATFORM_HTTPS_URL,
            timeout=10,
            verify=True
        )
        
        # Check for HSTS header (optional but recommended)
        hsts_header = response.headers.get("Strict-Transport-Security", "")
        
        if hsts_header:
            # If HSTS is present, verify it's properly configured
            assert "max-age=" in hsts_header.lower(), \
                f"HSTS header present but missing max-age: {hsts_header}"
            
            # Extract max-age value
            for part in hsts_header.split(";"):
                if "max-age=" in part.lower():
                    max_age_str = part.split("=")[1].strip()
                    max_age = int(max_age_str)
                    # Recommended: at least 6 months (15768000 seconds)
                    assert max_age > 0, \
                        f"HSTS max-age should be positive, got {max_age}"
        else:
            # HSTS not present - this is acceptable but not ideal
            # We'll just note it rather than fail
            pytest.skip("HSTS header not present (optional but recommended)")
            
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to {PLATFORM_HTTPS_URL}: {e}")


# Feature: self-hosted-ai-coding-platform, Property 6: HTTPS Enforcement
def test_https_certificate_expiry() -> None:
    """
    Property 6: HTTPS Enforcement (Certificate Validity)
    
    The SSL certificate should be valid and not expired.
    
    Validates: Requirements 9.1, 9.2
    """
    try:
        # requests library will raise SSLError if certificate is expired
        response = requests.get(
            PLATFORM_HTTPS_URL,
            timeout=10,
            verify=True  # This checks certificate validity
        )
        
        # If we get here, certificate is valid
        assert response.status_code < 500, \
            f"HTTPS endpoint returned server error: {response.status_code}"
        
    except requests.exceptions.SSLError as e:
        pytest.fail(f"SSL certificate is invalid or expired: {e}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot connect to {PLATFORM_HTTPS_URL}: {e}")


# ============================================================================
# Integration Tests
# ============================================================================

def test_complete_https_workflow() -> None:
    """
    Integration test: Complete workflow from HTTP to HTTPS.
    
    This test verifies the entire redirect chain:
    1. HTTP request is made
    2. Server responds with redirect
    3. Client follows redirect to HTTPS
    4. HTTPS page loads successfully
    
    Validates: Requirements 9.1
    """
    http_url = PLATFORM_HTTP_URL
    
    try:
        # Make request with redirect following enabled
        response = requests.get(
            http_url,
            allow_redirects=True,  # Follow redirects
            timeout=10,
            verify=True
        )
        
        # Property: Final URL should be HTTPS
        assert response.url.startswith("https://"), \
            f"Final URL after redirects is not HTTPS: {response.url}"
        
        # Property: Should successfully load the page
        assert response.status_code == 200, \
            f"HTTPS page did not load successfully, status: {response.status_code}"
        
        # Property: Response should have content
        assert len(response.content) > 0, \
            "HTTPS page returned empty content"
        
        # Property: Should have at least one redirect in history
        assert len(response.history) > 0, \
            "No redirects occurred from HTTP to HTTPS"
        
        # Property: First redirect should be from HTTP
        first_request = response.history[0]
        assert first_request.url.startswith("http://"), \
            f"First request was not HTTP: {first_request.url}"
        
        # Property: First redirect should have valid status code
        assert first_request.status_code in VALID_REDIRECT_CODES, \
            f"First redirect had invalid status code: {first_request.status_code}"
        
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Cannot complete HTTPS workflow test: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
