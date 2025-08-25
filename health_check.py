#!/usr/bin/env python3
"""
Health check script for the Study App
This script can be used to verify the application is running correctly
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def health_check():
    """Perform basic health checks on the application"""
    checks = []

    # Check if main.py can be imported
    try:
        import main

        checks.append(("✓", "Main application module loads successfully"))
    except Exception as e:
        checks.append(("✗", f"Failed to import main module: {e}"))
        return False, checks

    # Check if database_manager can be imported
    try:
        import database_manager

        checks.append(("✓", "Database manager module loads successfully"))
    except Exception as e:
        checks.append(("✗", f"Failed to import database_manager: {e}"))
        return False, checks

    # Check if database file exists
    if os.path.exists("database/data_source.db"):
        checks.append(("✓", "Database file exists"))
    else:
        checks.append(("✗", "Database file not found"))
        return False, checks

    # Check if Flask app can be created
    try:
        app = main.app
        if app:
            checks.append(("✓", "Flask application created successfully"))
        else:
            checks.append(("✗", "Flask application is None"))
            return False, checks
    except Exception as e:
        checks.append(("✗", f"Failed to create Flask app: {e}"))
        return False, checks

    return True, checks


if __name__ == "__main__":
    print("Running health check for Study App...")
    print("-" * 50)

    success, checks = health_check()

    for status, message in checks:
        print(f"{status} {message}")

    print("-" * 50)
    if success:
        print("✓ All health checks passed!")
        sys.exit(0)
    else:
        print("✗ Some health checks failed!")
        sys.exit(1)
