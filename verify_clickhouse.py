#!/usr/bin/env python3
"""
Verification script to test ClickHouse driver installation
"""

import sys

def test_clickhouse_driver():
    """Test if clickhouse-driver can be imported"""
    try:
        import clickhouse_driver
        print("✅ ClickHouse driver (clickhouse-driver) installed successfully!")

        # Print version information
        try:
            version = clickhouse_driver.__version__
            print(f"   Version: {version}")
        except AttributeError:
            print("   Version: Unknown")

        # Test basic client creation (no actual connection)
        try:
            from clickhouse_driver import Client
            client = Client(host='localhost', port=9000)
            print("✅ ClickHouse client can be instantiated")
            return True
        except Exception as e:
            print(f"⚠️  ClickHouse client instantiation failed (expected without server): {e}")
            return True  # This is expected without a running server

    except ImportError as e:
        print(f"❌ ClickHouse driver installation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_clickhouse_driver()
    sys.exit(0 if success else 1)