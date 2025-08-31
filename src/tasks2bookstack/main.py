import argparse
from pathlib import Path

from tasks2bookstack.bookstack import BookStackClient
from tasks2bookstack.caldav import CalDavClient
from tasks2bookstack.config import Config
from tasks2bookstack.log import get_logger

logger = get_logger(name=__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync CalDAV tasks to a Bookstack page.")
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="the path to the configuration file",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"configuration file not found at {config_path.resolve()}")
        return

    config = Config.from_yaml(config_path)

    logger.info("fetching tasks from caldav server")
    caldav_client = CalDavClient(config.caldav)
    tasks = caldav_client.get_tasks()

    if not tasks:
        logger.info("no tasks found, nothing to do")
        return

    content = "# Tasks\n\n" + "\n".join(f"- [ ] {task}" for task in tasks)

    bookstack_client = BookStackClient(config.bookstack)
    bookstack_client.update_page(content)
