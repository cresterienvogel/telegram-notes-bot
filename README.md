# 🗒️ Telegram Notes Bot  

<p>
  <img src="https://img.shields.io/badge/Aiogram-3.13.1-blue?&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-316192?&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?&logo=docker&logoColor=white" />
</p>

## 📌 Overview

**Telegram Notes Bot** is a minimalist note-taking bot.  
It allows you to create, view, and delete notes directly in Telegram.

- No reminders
- No unnecessary logic
- Clean and understandable UX

## ✨ Features

| Feature | Description |
|-------------|----------|
| Notes creation | User sends text and the bot saves it |
| Notes listing | Displaying all saved notes as a list |
| Notes deletion | Convenient inline list for deletion |
| Automatic profile creation | By the first `/start` |
| PostgreSQL | Data is under secure protection |
| Docker-ready | One command deployment |

## 🧰 Tech stack

| Component | Tech |
|-----------|------|
| Telegram API | Aiogram 3.13.1 |
| Database | PostgreSQL 16 |
| Driver | asyncpg |
| ORM | SQLAlchemy 2 |
| Runtime | Python 3.12 |
| Deployment | Docker |

## 🚀 Quick Start

### 1. Clone repository

```bash
git clone https://github.com/cresterienvogel/telegram-notes-bot.git
cd telegram-notes-bot
```

### 2. Create `.env` and fill it

```bash
cp .env.example .env
```

### 3. Run in Docker

```bash
docker compose up -d --build
```
