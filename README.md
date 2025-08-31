# Tasks2Bookstack

This tool syncs tasks from a CalDAV server to a page in the Bookstack wiki software. It fetches all tasks (both open and completed) and displays them in Bookstack with open tasks appearing first, followed by completed tasks.

## Prerequisites

- Python 3.11+ (or a container engine like podman or docker)
- A CalDAV server (e.g., Nextcloud, Radicale)
- A Bookstack instance with API access

## Configuration

Create a `config.yaml` file based on the `config.example.yaml`:

```yaml
bookstack:
  # The URL of your Bookstack instance (e.g., https://bookstack.example.com)
  url: ""

  # Your Bookstack API Token ID
  token_id: ""

  # Your Bookstack API Token Secret
  token_secret: ""

  # The ID of the page you want to update with your tasks
  page_id: 0

caldav:
  # The URL of your CalDAV server (e.g., https://caldav.example.com)
  url: ""

  # Your CalDAV username
  username: ""

  # Your CalDAV password
  password: ""

  # The id of the calendar you want to sync tasks from
  calendar: ""
```

## Usage

```
podman run --rm -it \
    --name tasks2bookstack \
    -v /path/to/your/config.yaml:/app/config.yaml:ro,z \
    $(IMAGE_NAME)
```
