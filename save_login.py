from playwright.sync_api import sync_playwright
from utils.config_loader import load_config

def save_login(env="qa"):
    config = load_config(env)
    base_url = config["baseUrl"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(base_url)

        print("Duo MFA")
        input("press enter to continue...")

        context.storage_state(path=f"crm_state_{env}.json")
        print("saved to crm_state_{env}.json")

        browser.close()

if __name__ == "__main__":
    save_login("stage")
