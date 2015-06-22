"""
This module contains common definitions and functions used within the
test suite.
"""
import logging
from fedex.config import FedexConfig

def get_test_config():
    """
    Returns a basic FedexConfig to test with.
    """

    try:
        import test_settings
        return test_settings.get_test_config()
    except ImportError:
        logging.warn("Returning fallback nonsense config.")
    # Test server (Enter your credentials here)
    return FedexConfig(key='xxxxxxxxxxxxxxxxx',
                       password='xxxxxxxxxxxxxxxxxxxxxxxxx',
                       account_number='xxxxxxxxx',
                       meter_number='xxxxxxxxxx',
                       use_test_server=True)