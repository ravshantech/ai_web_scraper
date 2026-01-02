import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from openai import OpenAI

# ------------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ------------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    print("Please create a .env file with: OPENAI_API_KEY=sk-...")
    exit()

client = OpenAI(api_key=api_key)

# ------------------------------------------------------------------------------
# 2. DATA CLASS
# ------------------------------------------------------------------------------
class Website:
    """
    Stores the content of a scraped website and handles summarization.
    """
    def __init__(self, url, title, body_text):
        self.url = url
        self.title = title
        self.body_text = body_text

    def get_summary(self):
        """
        Sends the website text to OpenAI to generate a summary.
        """
        # Truncate content to 4000 chars to fit standard context windows
        limit = 4000
        content_to_summarize = self.body_text[:limit]
        
        print(f"\nSending {len(content_to_summarize)} characters to OpenAI...")

        system_prompt = "You are a helpful assistant that summarizes web pages."
        user_prompt = f"Please provide a short summary of the following website content:\n\n{content_to_summarize}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

# ------------------------------------------------------------------------------
# 3. THE SCRAPER ENGINE
# ------------------------------------------------------------------------------
class WebScraper:
    """
    Uses Playwright to render the page with a real browser disguised as a human.
    """
    def scrape(self, url):
        print(f"Scraping {url}...")
        
        with sync_playwright() as p:
            # 1. Launch the browser (headless=True is invisible)
            browser = p.chromium.launch(headless=True)
            
            # 2. DISGUISE: Create a context with a real User-Agent string
            # This tricks websites into thinking you are a regular Chrome user on Windows
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            # 3. Open a new page within that context
            page = context.new_page()
            
            # 4. Go to the URL
            # We increase timeout to 60s for slow sites
            try:
                page.goto(url, timeout=60000)
            except Exception as e:
                print(f"Error loading page: {e}")
                browser.close()
                return None

            # 5. Wait for the page to fully load (JavaScript)
            print("Waiting for network activity to settle...")
            try:
                page.wait_for_load_state("networkidle", timeout=60000)
            except:
                print("Warning: Network didn't settle, but proceeding with current content.")
            
            # 6. Extract data
            title = page.title()
            html_content = page.content()
            
            browser.close()
            
            # 7. Clean the HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove scripts, styles, and meta tags to get just the human-readable text
            for element in soup(["script", "style", "header", "footer", "nav"]):
                element.extract()
                
            body_text = soup.body.get_text(separator=' ', strip=True)
            
            return Website(url, title, body_text)

# ------------------------------------------------------------------------------
# 4. MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # You can change this URL to test different sites
    target_url = "https://openai.com" 
    
    scraper = WebScraper()
    website_data = scraper.scrape(target_url)
    
    if website_data:
        print(f"\n--- Title: {website_data.title} ---")
        
        summary = website_data.get_summary()
        
        print("\n--- Summary ---")
        print(summary)
    else:
        print("Failed to scrape the website.")