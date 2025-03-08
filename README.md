# # QueueQueen

QueueQueen is a Telegram bot for managing queues efficiently. Built with **Aiogram**, **FastAPI**, and **SQLAlchemy**, it allows users to create, join, and manage queues in group chats.

## Features

- **Create and manage queues** – Users can start and maintain queues effortlessly.
- **Isolation** – each chat can have its own queue
- **Join and quit queues** – Simple commands to join or quit queues.
- **Queue position tracking** – Users can check their current position.
- **Admin controls** – Admins can clear queues.
- **High performance** – Built with **FastAPI** for webhook and **Async SQLAlchemy**.

## Tech Stack

- **Python** (3.12+)
- **Aiogram** – Asynchronous Telegram bot framework
- **FastAPI** – Webhook-based interaction
- **SQLAlchemy + Alembic** – Database ORM and migrations
- **SQLite** – Primary database (**Postgresql** is also supported if necessary)
- **Docker & Docker Compose** – Containerized deployment (Optional)

## Installation

To set up the project, follow the instructions in the [Installation Guide](docs/Installation.md).

### Prerequisites

- Python 3.12+
- PostgreSQL database (optional)
- Redis (optional, for caching)
- Docker & Docker Compose (for production deployment, optional)

### Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/Czertilla/QueueQueen.git
   cd QueueQueen
   ```
2. **Create a virtual environment** (optional but recommended)

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   - Create a `.env` file in the project root. You can check [.env-exmpl](.env-exmpl)

   ```
   APP_NAME = 

   DB_NAME = 

   BOT_TG_TOKEN = 
   BOT_TG_WEBHOOK = 

   ```
5. **Run database migrations**

   ```sh
   alembic upgrade head
   ```

## Running the Bot

### Locally

#### Long Polling

if [long polling](https://core.telegram.org/bots/api#getupdates) is sufficient for your needs, you can run the corresponding module in the tests package

```sh
python tests/bot/polling.py
```

#### Webhook

if you need a [webhook](https://core.telegram.org/bots/api#setwebhook), then before pre-configuring proxying, for example using [ngrok](https://ngrok.com/), get your https and update the environment variable `BOT_TG_WEBHOOK` with it. After that, you can start the unicorn server

```sh
uvicorn main:app --reload --host localhost --port 8080 --log-config src/loggers/config.json
```

### Using Docker

```sh
docker-compose up --build
```

## Usage

Invite the bot to a group and use the following commands:

| Command    | Description                                |
| ---------- | ------------------------------------------ |
| `/start` | Admin-only (in chats): Create new queue    |
| `/start` | (in presonal): Start bot for notifications |
| `/join`  | Join the current queue                     |
| `/quit`  | Leave the queue                            |
| `/check` | Show list of position in queue             |
| `/clear` | Admin-only: Clear the queue                |

## Documentation

For full documentation, refer to the [Wiki](docs/Home.md).

Key sections:

- [Getting Started](docs/Installation.md)
- [Architecture](docs/Architecture.md)
- [Modules](docs/Modules.md)
- [Contribution Guide](docs/CONTRIBUTING.md)

## Deployment

For production, deploy using **Docker** and set up a webhook with **FastAPI**:

1. **setup .env-non-dev file**

   ```
   APP_NAME = 

   DB_NAME = 

   BOT_TG_TOKEN = 
   BOT_TG_WEBHOOK = 

   ```
2. **Build and run the containers**

   ```sh
   docker-compose up --build
   ```

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING](docs/CONTRIBUTING.md) guide for more details.
For quck start, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your fork (`git push origin feature-branch`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Czertilla/QueueQueen/blob/main/LICENSE "MIT License") file for details.

---

Developed with ❤️ by [Czertilla](https://github.com/Czertilla)

