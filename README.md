# AI Web Scraper 🕷️🤖

A robust Python web scraper that extracts content from dynamic, JavaScript-heavy websites using **Playwright** and generates concise summaries using **OpenAI's GPT-4o**.

## 🚀 Features

- **Dynamic Scraping:** Uses `Playwright` to run a real, headless Chromium browser, allowing it to scrape sites that rely on JavaScript (React, Vue, etc.).
- **AI Power:** Integrates with OpenAI (GPT-4o-mini) to clean and summarize scraped content into digestible insights.
- **Bot Evasion:** Includes User-Agent spoofing and human-like delays (`networkidle`) to bypass basic anti-bot protections.
- **Secure:** Uses `.env` environment variables to keep API keys safe and out of version control.

## 🛠️ Prerequisites

- Python 3.8+
- An OpenAI API Key

## 📥 Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/YOUR_USERNAME/ai-web-scraper.git](https://github.com/YOUR_USERNAME/ai-web-scraper.git)
    cd ai-web-scraper
    ```

2.  **Create a Virtual Environment (Recommended)**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: If you don't have a requirements file yet, install manually: `pip install playwright beautifulsoup4 openai python-dotenv`)_

4.  **Install Playwright Browsers**
    This is a required step to download the actual browser binaries.
    ```bash
    playwright install
    # OR if that fails:
    python -m playwright install
    ```

## ⚙️ Configuration

1.  Create a file named `.env` in the root directory of the project.
2.  Add your OpenAI API key to it:

    ```text
    OPENAI_API_KEY=sk-proj-123456...
    ```

3.  **Important:** Ensure `.env` is listed in your `.gitignore` file to prevent leaking your key.

## 🏃 Usage

Run the scraper script:

```bash
python scraper.py
```

## To scrape a different website, modify the target_url variable inside scraper.py.
