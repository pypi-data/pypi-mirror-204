import sys

import np_config
import np_logging

logger = np_logging.get_logger(__name__)

CONFIG: dict = np_config.fetch('/projects/np_tools/config')
"""Package config dict with paths etc."""

ON_WINDOWS: bool = 'win' in sys.platform
"""True if running on Windows."""
