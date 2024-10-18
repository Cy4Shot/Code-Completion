print()
import logging
from rich.logging import RichHandler
logging.basicConfig(
    level="INFO", format="%(message)s", datefmt=" ", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
log.info("[MAIN] Starting...")

import mapper
import matplotlib.pyplot as plt
mapper.log = log

log.info("[MAIN] Creating background map...")
fig = mapper.create_map_snapshot(debug=False)
plt.xlim(-0.5328, 0.2506)
plt.ylim(51.3452, 51.7189)
plt.show()