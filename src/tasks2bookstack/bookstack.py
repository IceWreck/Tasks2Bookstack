import httpx

from tasks2bookstack.config import BookstackConfig
from tasks2bookstack.log import get_logger

logger = get_logger(name=__name__)


class BookStackClient:
    """
    A client for the Bookstack API.
    """

    def __init__(self, config: BookstackConfig):
        self.config = config
        self.client = httpx.Client(
            base_url=self.config.url,
            headers={
                "Authorization": f"Token {self.config.token_id}:{self.config.token_secret}",
                "Content-Type": "application/json",
            },
        )

    def update_page(self, content: str) -> None:
        """
        Updates a page in Bookstack.
        """
        logger.info(f"updating page {self.config.page_id}")
        response = self.client.put(
            f"/api/pages/{self.config.page_id}",
            json={"markdown": content},
        )
        response.raise_for_status()
        logger.info(f"page {self.config.page_id} updated successfully")
