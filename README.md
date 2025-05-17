# MarketBot

MarketBot is an intelligent agentic AI tool designed to monitor your Facebook Marketplace activity, learn your item preferences over time, and notify you in real-time about good deals and relevant listings. Built with a Python Flask backend and leveraging the CrewAI framework, MarketBot automates scraping, analysis, alerting, and reporting to help you never miss a bargain.

---

## Features

- **Authenticated Scraping**: Logs into your Facebook Marketplace account to scrape listings securely.
- **Interest Learning**: Learns your preferred item categories based on your saved listings.
- **Price & Quality Analysis**: Analyzes item price vs. historical value and description quality using AI.
- **Real-time Alerts**: Sends push notifications for good deals through ntfy API integration.
- **Daily Email Reports**: Summarizes new listings, deals, and insights in an email report each day.
- **Persistent Storage**: Stores all listings and user preferences indefinitely using PostgreSQL.
- **CrewAI-Powered**: Uses CrewAI’s ReAct agents for reasoning, decision-making, and adaptive workflows.

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL database
- Facebook account with active Marketplace usage
- ntfy-compatible notification endpoint
- SMTP email account for sending reports

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/marketbot.git
   cd marketbot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables. Create a `.env` file or export variables:

   ```env
   FACEBOOK_SESSION_COOKIE=your_facebook_cookie_here
   DATABASE_URL=postgresql://user:password@localhost:5432/marketbot_db
   NTFY_API_ENDPOINT=https://ntfy.example.com/your-topic
   NTFY_API_KEY=your_ntfy_api_key
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@example.com
   SMTP_PASSWORD=your_email_password
   EMAIL_FROM=your_email@example.com
   EMAIL_TO=recipient@example.com
   ```

5. Initialize the database:

   ```bash
   flask db upgrade
   ```

### Running the Application

Run the Flask backend server:

```bash
flask run
```

---

## Usage

- The scraper will periodically fetch new listings from your Facebook Marketplace account.
- The CrewAI agents will process listings to learn your preferences and detect deals.
- When a good deal is found, ntfy push notifications are sent immediately.
- A daily email summary will be sent automatically at configured time.

---

## Configuration

- Configure the scheduler interval for scraping and reporting inside the Flask app config.
- Define categories of interest to track inside the user preferences or allow the AI to learn them over time.
- Customize push notifications and email templates as needed.

---

## Architecture Overview

- **Scraper Module:** Authenticates to Facebook account and extracts marketplace listings.
- **CrewAI Agents:** Manage interest learning, deal detection, quality scoring, alerting, and reporting.
- **Database:** PostgreSQL for listings and metadata; optional vector DB for semantic search.
- **Notification Layer:** ntfy for push notifications, SMTP for sending email reports.
- **Backend:** Flask REST API coordinating the workflow.

---

## Security

- Facebook authentication is managed via session cookies. Keep credentials secure.
- Database credentials and API keys are stored in environment variables.
- The backend serves authenticated endpoints for local use only.

---

## Future Work

- Add a web dashboard to view listing summaries and agent insights interactively.
- Integrate a vector database for enhanced similarity searches.
- Improve NLP models for more accurate item quality scoring.
- Add multi-user support and granular user preference controls.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---


