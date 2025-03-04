---

<h1 align="center">sleepagotchiLITE_bot</h1>

<p align="center">Automate tasks in Sleepagotchi Lite to save time and boost your gameplay!</p>

---

## 🚀 About the Bot

The **sleepagotchiLITE_bot** is an advanced automation tool designed for Sleepagotchi Lite that streamlines in-game tasks so you can focus on strategy rather than repetitive actions. It features:

- **Auto Daily:** Automatically claim your daily rewards.
- **Missions & Auto Tasks:** Efficiently manage and claim mission rewards with the new auto task system.
- **Gacha Spins:** Spin the gacha automatically to win heroes and resources.
- **Hero Upgrades:** Enjoy an optimized hero upgrade system for a smoother and more responsive experience.
- **Challenges:** Deploy your heroes to challenges to earn extra rewards.
- **Shop Automation:** Automatically purchase free materials from the shop.
- **Proxy & Custom Delays:** Support for proxies and configurable delays between loops and account switches for enhanced stability.

With these features, the bot maximizes your gameplay efficiency and lets you progress effortlessly.

---

## 🌟 **Version v1.3.3**

### **Updates**

- **Optimized Mission System:** The bot can now automatically unlock additional slots if no hero is available to fill a specific mission, ensuring smoother mission deployment.

## Stay tuned for further updates and improvements! ✨

---

## 📥 **How to Register**

To start using the **sleepagotchiLITE_bot**, simply contact the bot via Telegram:

<div align="center">
  <a href="https://t.me/sleepagotchiLITE_bot/game?startapp=72633a35343338323039363434" target="_blank">
    <img src="https://img.shields.io/static/v1?message=sleepagotchiLITE_bot&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## ⚙️ **Configuration in `config.json`**

Below is a summary of the configuration options available in `config.json`:

| **Parameter**               | **Description**                                                   | **Default** |
| --------------------------- | ----------------------------------------------------------------- | ----------- |
| `task`                      | Enable automatic mission management.                              | `true`      |
| `daily`                     | Enable automatic daily reward claiming.                           | `true`      |
| `spin_gacha`                | Enable automatic gacha spins.                                     | `true`      |
| `send_heroes_to_challenges` | Enable automatic deployment of heroes to challenges.              | `true`      |
| `shop`                      | Enable automatic shop purchases.                                  | `true`      |
| `proxy`                     | Enable proxy usage (configure proxies in `proxy.txt` if enabled). | `false`     |
| `delay_loop`                | Delay (in seconds) between each automation loop.                  | `60`        |
| `delay_account_switch`      | Delay (in seconds) between switching accounts.                    | `10`        |

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/sleepagotchi-lite-bot.git
   ```

2. **Navigate to the Project Folder**  
   Change directory into the project:

   ```bash
   cd sleepagotchi-lite-bot
   ```

3. **Install Dependencies**  
   Install the required libraries using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your Query**  
   Create a file named `query.txt` and add your query data in it.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Start the bot with the following command:

   ```bash
   python main.py
   ```

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us on Telegram:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
