import logging
import config.logging_config

logger = logging.getLogger(__name__)

logger.info("Testing logger")

print("Handlers:", logging.getLogger().handlers)
print("Level:", logging.getLogger().level)