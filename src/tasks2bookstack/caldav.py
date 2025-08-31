from dataclasses import dataclass, field
from typing import Optional

from caldav import DAVClient, Todo
from icalendar import Calendar

from tasks2bookstack.config import CaldavConfig
from tasks2bookstack.log import get_logger

logger = get_logger(name=__name__)


@dataclass
class Task:
    uid: str
    summary: str
    is_completed: bool
    parent_uid: Optional[str] = None
    children: list["Task"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Task(summary={self.summary}, children={len(self.children)})"


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

    def get_tasks(self) -> list[Todo]:
        """
        Gets all tasks from the configured calendar.
        """
        logger.info(f"fetching tasks from calendar '{self.config.calendar}'")
        principal = self.client.principal()
        calendar = principal.calendar(cal_id=self.config.calendar)
        todos = calendar.todos(include_completed=True)
        logger.info(f"found {len(todos)} tasks in calendar '{self.config.calendar}'")
        return todos

    def parse_task(self, todo: Todo) -> Optional[Task]:
        """
        Parse a Todo object into a Task dataclass.
        """
        cal = Calendar.from_ical(todo.data)
        for component in cal.walk():
            if component.name == "VTODO":
                uid = component.get("uid")
                summary = component.get("summary")
                related_to = component.get("related-to")

                # Check if task is completed
                status = component.get("status")
                is_completed = status and status.upper() == "COMPLETED"

                parent_uid = None
                if related_to and related_to.params.get("RELTYPE") == "PARENT":
                    parent_uid = related_to.to_ical().decode()

                return Task(uid=str(uid), summary=str(summary), is_completed=is_completed, parent_uid=parent_uid)
        return None

    def format_task(self, task: Task, level: int) -> str:
        """
        Format a task as markdown with proper indentation and checkbox.
        """
        indent = "  " * level
        checkbox = "[x]" if task.is_completed else "[ ]"
        markdown = f"{indent}- {checkbox} {task.summary}\n"
        for child in task.children:
            markdown += self.format_task(child, level + 1)
        return markdown

    def as_markdown(self, todos: list[Todo]) -> str:
        """
        Converts a list of tasks to a markdown string, with open tasks first and completed tasks after.
        """
        # Parse all tasks
        all_tasks: list[Task] = []
        for todo in todos:
            task = self.parse_task(todo)
            if task is not None:
                all_tasks.append(task)

        # Separate open and completed tasks
        open_tasks: list[Task] = []
        completed_tasks: list[Task] = []

        for task in all_tasks:
            if task.is_completed:
                completed_tasks.append(task)
            else:
                open_tasks.append(task)

        logger.info(f"found {len(open_tasks)} open tasks and {len(completed_tasks)} completed tasks")

        # Combine with open tasks first
        sorted_tasks = open_tasks + completed_tasks

        # Build parent-child relationships
        tasks_by_uid: dict[str, Task] = {}
        for task in sorted_tasks:
            tasks_by_uid[task.uid] = task

        root_tasks: list[Task] = []
        for task in sorted_tasks:
            if task.parent_uid and task.parent_uid in tasks_by_uid:
                tasks_by_uid[task.parent_uid].children.append(task)
            else:
                root_tasks.append(task)

        # Format tasks as markdown
        markdown = ""
        for task in root_tasks:
            markdown += self.format_task(task, 0)

        return markdown
