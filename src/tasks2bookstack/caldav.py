from caldav import DAVClient

from tasks2bookstack.config import CaldavConfig
from tasks2bookstack.log import get_logger

logger = get_logger(name=__name__)


class CalDavClient:
    """
    A client for the Caldav server.
    """

    def __init__(self, config: CaldavConfig):
        self.config = config
        self.client = DAVClient(
            url=self.config.url,
            username=self.config.username,
            password=self.config.password,
        )

    def get_tasks(self) -> list[str]:
        """
        Gets all tasks from the configured calendar.
        """
        logger.info(f"fetching tasks from calendar '{self.config.calendar}'")
        principal = self.client.principal()
        calendar = principal.calendar(cal_name=self.config.calendar)
        todos = calendar.todos(include_completed=False)
        tasks = [str(todo.data) for todo in todos]
        logger.info(f"found {len(tasks)} tasks in calendar '{self.config.calendar}'")
        return tasks
