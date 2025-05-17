# Technical Design Document  
## Facebook Marketplace Agentic Tracker & Notifier

---

## 1. Project Overview

A Python Flask-based backend application utilizing CrewAI for agentic AI workflows to track your Facebook Marketplace account activity by scraping listings authenticated through your personal account. The system learns your item preferences over time by analyzing your saved listings and provides daily email reports and real-time push notifications (via ntfy API) for good deals and relevant new listings.

---

## 2. Objectives & Requirements

- Periodically scrape your Facebook Marketplace data, authenticated as you, to gather new item listings.
- Extract key listing attributes: title, price, description, location, images, plus AI-derived item quality meta-attribute.
- Track specific item categories; learn interest profiles from your saved listings dynamically.
- Alert you in near real-time when good deals appear (e.g., below a reasonable price threshold based on historic values).
- Generate and send daily email reports summarizing activity and opportunities.
- Store all listings indefinitely in PostgreSQL, along with rich metadata, plus optional vector store for advanced similarity search on descriptions.
- Deployable on local machine or cloud VM, designed for single-user scale.
- Use CrewAI’s ReAct agents for reasoning, decision-making, and adaptive workflows.
- Integrate push alerts via ntfy service using their REST API.

---

## 3. System Architecture

```
+------------+       +-------------+       +---------------+         +------------------+  
| Facebook   |       | Scraper &   |       | Flask Backend  |         | Notification &   |  
| Marketplace| <---> | Data Ingest | <---> | (CrewAI Agent) | <--->   | Email Service    |  
| Web Portal |       | (Python)    |       | + DB & Logic   |         | (ntfy, SMTP)     |  
+------------+       +-------------+       +---------------+         +------------------+  

                                |  
                                v  
                         +---------------+  
                         | PostgreSQL DB |  
                         +---------------+  
                                |  
                                v  
                        +----------------+  
                        | Vector DB (opt)|  
                        +----------------+  
```

### Components:

- **Facebook Marketplace Scraper (Python module):**  
  - Authenticates as your Facebook account (via cookies/session).  
  - Periodically scrapes marketplace listings from specified categories.  
  - Extracts raw listing data: title, price, description, location, image URLs.  
  - Fetches listings you have “saved” to help train the interest profile.  
  - Handles rate limiting and error resilience.
  
- **Flask Backend (API & Agent):**  
  - Core backend server running the CrewAI framework with ReAct agents.  
  - Responsible for classification, price/value analysis, quality meta-attribute extraction.  
  - Learns user preferences from saved listings over time, refining item interest models.  
  - Monitors new listings for good deals using historical pricing context.  
  - Exposes REST API endpoints for scraping triggers, report generation, status queries.
  
- **Database Layer:**  
  - **PostgreSQL:** Stores listings, user profile data, agent states, alert history.  
  - **Vector Database (optional):** For semantic similarity search on listing descriptions to improve matching and deal detection.
  
- **Notification & Reporting:**  
  - Sends real-time alerts via ntfy service API when a good deal or highly relevant item is detected.  
  - Composes and dispatches daily email summary reports (using SMTP or email-sending library).  
  - Report includes new listings, price changes, deal alerts, and interest profile insights.

---

## 4. Data Model (PostgreSQL tables)

- **`listings`**  
  - `listing_id` (PK)  
  - `title` (text)  
  - `price` (numeric)  
  - `description` (text)  
  - `location` (text)  
  - `images` (json/array of URLs)  
  - `category` (text)  
  - `quality_score` (float)  
  - `scraped_at` (timestamp)  
  - `fb_listing_url` (text)  

- **`saved_listings`**  
  - Subset mapping of listings user has saved (helps train interest profile)  

- **`user_preferences`**  
  - Stores learned interest categories, price ranges, keywords  

- **`alerts`**  
  - Records of all alerts sent  

- **`agent_state`**  
  - Saves agent reasoning memory or model states for CrewAI agents  

---

## 5. AI Workflow Design with CrewAI

- **Agent Type:** ReAct (Reasoning + Acting)  
- **Tasks:**  
  1. **Interest Learning Agent:** Scan saved listings regularly to infer preferred categories, typical price ranges, and quality traits.  
  2. **Deal Detection Agent:** Evaluate new listings for price versus historic value distributions; if a deal is detected, generate an alert.  
  3. **Quality Scoring Agent:** Use natural language processing (NLP) to analyze descriptions for signs of item condition, completeness, seller comments, etc., outputting a quality score.  
  4. **Alerting Agent:** When a deal or relevant item is detected, call ntfy API to send push notification.  
  5. **Reporting Agent:** Daily, compose the email report summarizing new/interesting listings and metrics on interest changes.

- **Integration:** CrewAI agents will interface with database, scraping module, ntfy API, and SMTP library as needed.

---

## 6. User Interface & Notification

- No dedicated UI needed initially, but possible lightweight dashboard showing summary & alert history as Flask web pages (optional future work).  
- Real-time near-instant push notifications via ntfy to configured devices/apps.  
- Daily email sent automatically at configurable time by backend scheduled task.

---

## 7. Security & Privacy Considerations

- Facebook authentication handled securely — use stored session cookies with appropriate encryption, no password storage.  
- Respect Facebook’s usage policies as much as possible (emphasize manual rate limiting, not aggressive scraping).  
- Secure storage of sensitive data (DB credentials, email server auth) via environment variables.  
- API endpoints protected behind auth (e.g., local tokens or OAuth if extended).  
- Do not expose user’s Facebook session or scraped data publicly.

---

## 8. Deployment Strategy

- Flask backend packaged with Python dependencies (requirements.txt, possibly Dockerfile for containerized deployment).  
- Scheduler (e.g., cron or APScheduler inside Flask app) triggers scraping & agent workflows.  
- Database hosted locally or remote PostgreSQL instance.  
- Endpoints accessible locally or protected on cloud VM with firewall rules.  
- Logs maintained for scraping and agent operations for debugging.

---

## 9. Development Roadmap

| Phase           | Tasks                                                  | Duration  |
|-----------------|--------------------------------------------------------|-----------|
| **Phase 1**     | Setup Flask backend, DB schema, basic scraping module with FB auth | 2 weeks   |
| **Phase 2**     | Integrate CrewAI agents for interest learning and deal detection | 3 weeks   |
| **Phase 3**     | Implement ntfy push notifications and daily email reports | 1 week    |
| **Phase 4**     | Optimize scraping reliability, add vector DB if needed, improve quality scoring | 2 weeks   |
| **Phase 5**     | Deployment setup, security hardening, testing | 1 week    |
| **Phase 6**     | Optional UI dashboard for monitoring, user controls | 2 weeks   |

---
