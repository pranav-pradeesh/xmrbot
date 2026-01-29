import time
import re
import requests
import telebot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =================== YOUR SETTINGS ===================
BOT_TOKEN = "<YOUR_BOT_TOKEN>"
CHAT_ID = "<YOUR_CHAT_ID>"   # your Telegram GROUP chat ID

XMRIG_API = "http://127.0.0.1:18000/api.json"

# YOUR MONERO WALLET (same as in XMRig)
WALLET = "<WALLET_ADDRESS"
# ====================================================

bot = telebot.TeleBot(BOT_TOKEN)
last_accepted = 0


def get_xmr_to_inr_rate():
    """Fetch current XMR to INR exchange rate with multiple fallbacks"""
    
    # Method 1: Try CoinGecko (most reliable for INR)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=inr"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "monero" in data and "inr" in data["monero"]:
            print(f"✓ Got price from CoinGecko: ₹{data['monero']['inr']}")
            return data["monero"]["inr"]
    except Exception as e:
        print(f"CoinGecko failed: {e}")
    
    # Method 2: Try Binance (XMR/USDT) × USD/INR conversion
    try:
        # Get XMR price in USDT
        url_xmr = "https://api.binance.com/api/v3/ticker/price?symbol=XMRUSDT"
        xmr_response = requests.get(url_xmr, timeout=10).json()
        
        if 'price' in xmr_response:
            xmr_usdt = float(xmr_response['price'])
            
            # Use fixed USD to INR rate (~83-84) or get from another API
            # You can also fetch live USD/INR rate from forex API
            usd_inr = 83.5  # Approximate rate, update manually if needed
            
            xmr_inr = xmr_usdt * usd_inr
            print(f"✓ Got price from Binance: ₹{xmr_inr}")
            return xmr_inr
    except Exception as e:
        print(f"Binance failed: {e}")
    
    # Method 3: Try CryptoCompare
    try:
        url = "https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=INR"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "INR" in data:
            print(f"✓ Got price from CryptoCompare: ₹{data['INR']}")
            return data['INR']
    except Exception as e:
        print(f"CryptoCompare failed: {e}")
    
    print("❌ All price APIs failed")
    return None


def get_pending_and_paid_xmr():
    """Headless Selenium scraper tailored to YOUR SupportXMR layout"""

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # ---- 1) Open SupportXMR ----
        driver.get("https://supportxmr.com")

        # ---- 2) Wait for the search box (dynamic page) ----
        search = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )

        # ---- 3) Type wallet and press ENTER ----
        search.clear()
        search.send_keys(WALLET)
        search.send_keys(Keys.RETURN)

        # ---- 4) Wait for results to load ----
        time.sleep(10)

        # ---- 5) Read full visible text ----
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # ---- 6) Extract first two XMR numbers ----
        matches = re.findall(r"\b0\.\d+\b", page_text)

        if len(matches) >= 2:
            pending = matches[0]   # FIRST number after wallet = pending
            paid = matches[1]      # SECOND number = paid
        elif len(matches) == 1:
            pending = matches[0]
            paid = "0.00000000"
        else:
            pending = "not found"
            paid = "not found"

        driver.quit()
        return pending, paid

    except Exception as e:
        print("Selenium error:", e)
        driver.quit()
        return "error", "error"


while True:
    try:
        # ---- XMRig stats ----
        data = requests.get(XMRIG_API, timeout=5).json()

        hashrate = data["hashrate"]["total"][0]
        accepted = data["results"]["shares_good"]

        # ---- SupportXMR stats ----
        pending_xmr, paid_xmr = get_pending_and_paid_xmr()
        
        # ---- Get XMR to INR exchange rate ----
        xmr_inr_rate = get_xmr_to_inr_rate()

        # Notify only when a new share is accepted
        if accepted > last_accepted:
            msg = (
                f"✅ Share accepted!\n"
                f"⚡ Hashrate: {hashrate:.2f} H/s\n"
                f"📊 Accepted shares: {accepted}\n"
                f"💰 Pending: {pending_xmr} XMR\n"
            )
            
            # Add INR conversion line if valid
            if xmr_inr_rate and pending_xmr not in ["not found", "error"]:
                try:
                    pending_float = float(pending_xmr)
                    pending_inr = pending_float * xmr_inr_rate
                    msg += f"💵 Pending INR: ₹{pending_inr:,.2f}\n"
                except ValueError:
                    pass
            
            msg += (
                f"💸 Paid: {paid_xmr} XMR\n"
                f"🔗 Check supportxmr.com for details"
            )

            bot.send_message(CHAT_ID, msg)
            last_accepted = accepted

    except Exception as e:
        print("Bot error:", e)

    time.sleep(60)
