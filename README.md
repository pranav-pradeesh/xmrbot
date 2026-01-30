![XMR BOT](https://raw.githubusercontent.com/pranav-pradeesh/xmrbot/main/banner.png)

# XMRBOT
## 🚨🚨🚨 This Bot Works only for SupportXmr pool 🚨🚨🚨
> **NOTE:** In the config.json inside the XMRIG file, change the HTTP rule as following
```bash
"http": {
        "enabled": true,
        "host": "127.0.0.1",
        "port": 18000,
        "access-token": null,
        "restricted": true
    }
```
## How to run the bot
to run the bot, follow the steps
### Enter the folder that have xmrig in your device and clone this repository

```bash
git clone https://github.com/pranav-pradeesh/xmrbot.git
```
#### then install the required lbraries

```bash
pip install telebot
pip install selenium
```
### if you are mining from a cloud platform:

```bash
sudo apt update
sudo apt install -y wget unzip xvfb

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
```
## Bot Setup

### To setup a bot,

- open telegram
- search for
  ```bash
  @BotFather
  ```
- type:
  ```bash
  /newbot
  ```
- Enter name of your bot name
- Enter bot username that ends with "bot"
  eg:
  newbot
  new_bot
  new-bot
- copy the HTTP API
- paste here
  ```bash
  BOT_TOKEN = "<YOUR_BOT_TOKEN>"
  ```
- make a group and add the bot (if you have multiple machines running)
- In telegram search for
  ```bash
  @userinfobot
  ```
- Choose "Group" option
- chooose your group
- copy the id
- paste it here
  ```bash
  CHAT_ID = "<YOUR_CHAT_ID>"
  ```
- type your wallet address here
  ```bash
  WALLET = "<WALLET_ADDRESS>"
  ```
### Run The Bot...

### Output

                ✅ Share accepted!
                ⚡ Hashrate: 1655.27 H/s
                📊 Accepted shares: 28
                💰 Pending: 0.00013857 XMR
                💵 Pending INR: ₹6.07
                💸 Paid: 0.00000000 XMR
                🔗 Check supportxmr.com for details
