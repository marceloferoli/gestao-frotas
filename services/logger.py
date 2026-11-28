import os
import logging

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/sistema.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("FleetControl")
