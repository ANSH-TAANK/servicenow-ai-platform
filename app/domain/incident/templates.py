"""
Incident Short Description Templates

Purpose:
- Centralize all standardized
  ServiceNow short descriptions.

Only business rules belong here.
No business logic.
"""

# ============================================================
# Short Description Templates
# ============================================================

SHORT_DESCRIPTION_TEMPLATES = {
    # --------------------------------------------------------
    # Network
    # --------------------------------------------------------
    ("network", "vpn"): "VPN Connection Failure",
    ("network", "wifi"): "Wi-Fi Connectivity Issue",
    ("network", "lan"): "Local Network Connectivity Issue",
    ("network", "dns"): "DNS Resolution Failure",
    # --------------------------------------------------------
    # Hardware
    # --------------------------------------------------------
    ("hardware", "laptop"): "Laptop Hardware Issue",
    ("hardware", "printer"): "Printer Malfunction",
    ("hardware", "monitor"): "Display Hardware Issue",
    # --------------------------------------------------------
    # Software
    # --------------------------------------------------------
    ("software", "office"): "Microsoft Office Issue",
    ("software", "browser"): "Web Browser Issue",
    ("software", "application"): "Software Application Issue",
    # --------------------------------------------------------
    # Email
    # --------------------------------------------------------
    ("email", "outlook"): "Microsoft Outlook Issue",
    ("email", "delivery"): "Email Delivery Issue",
    # --------------------------------------------------------
    # Access
    # --------------------------------------------------------
    ("access", "password"): "Password Reset Required",
    ("access", "account"): "User Account Access Issue",
}
