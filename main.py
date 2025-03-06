from datetime import datetime
import json
import time
from colorama import Fore
import requests
from math import pow
import random

class sleepagotchi:
    BASE_URL = "https://telegram-api.sleepagotchi.com/v1/tg/"
    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://tgcf.sleepagotchi.com",
        "referer": "https://tgcf.sleepagotchi.com/",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.config = self.load_config()
        self.token = None
        self.gachaPoint = 0
        self.green_stones = 0
        self.purple_stones = 0
        self.coin = 0
        self.gem = 0

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Sleepagotchi LITE Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode('utf-8', 'backslashreplace').decode('utf-8')
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔒 Attempting to log in...", Fore.GREEN)

        # Validate the index input
        if index >= len(self.query_list):
            self.log(
                "❌ Invalid login index. Please check your input and try again.",
                Fore.RED,
            )
            return

        # Retrieve token and construct the new API URL
        token = self.query_list[index]
        req_url = f"{self.BASE_URL}getUserData?{token}"
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        headers = {**self.HEADERS}

        try:
            self.log("📡 Sending request to fetch user data...", Fore.CYAN)
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Check if the login is verified
            if data.get("verified", False):
                # Save token for later use
                self.token = token

                username = data.get("username", "Unknown")
                user_id = data.get("userId", "Unknown")

                # Retrieve important resource details from the player data
                resources = data.get("player", {}).get("resources", {})
                gold = resources.get("gold", {}).get("amount", 0)
                gem = resources.get("gem", {}).get("amount", 0)
                green_stones = resources.get("greenStones", {}).get("amount", 0)
                purple_stones = resources.get("purpleStones", {}).get("amount", 0)
                orb = resources.get("orb", {}).get("amount", 0)
                gacha = resources.get("gacha", {}).get("amount", 0)
                points = resources.get("points", {}).get("amount", 0)

                self.gachaPoint = gacha
                self.green_stones = green_stones
                self.purple_stones = purple_stones
                self.coin = gold
                self.gem = gem

                # Display a user-friendly success message with emojis
                self.log("✅ Login successful! Welcome aboard!", Fore.GREEN)
                self.log(f"👤 Username: {username}", Fore.LIGHTGREEN_EX)
                self.log(f"🆔 User ID: {user_id}", Fore.LIGHTBLUE_EX)
                self.log("💰 Resources:", Fore.CYAN)
                self.log(f"    💰 Gold: {gold}", Fore.CYAN)
                self.log(f"    💎 Gems: {gem}", Fore.CYAN)
                self.log(f"    💚 Green Stones: {green_stones}", Fore.CYAN)
                self.log(f"    💜 Purple Stones: {purple_stones}", Fore.CYAN)
                self.log(f"    🔮 Orb: {orb}", Fore.CYAN)
                self.log(f"    🎰 Gacha: {gacha}", Fore.CYAN)
                self.log(f"    🎯 Points: {points}", Fore.CYAN)
            else:
                self.log(
                    "⚠️ Login failed: Verification unsuccessful. Please check your token.",
                    Fore.YELLOW,
                )

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ JSON decode error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Missing expected data: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

    def spin_gacha(self) -> None:
        """
        Perform a series of gacha spins using different strategies:
        - Paid gacha spins (using self.gachaPoint)
        - Gem-based gacha spins (if self.gem >= 500)
        - One free gacha spin
        """
        # --- Paid Gacha Spins ---
        while self.gachaPoint > 0:
            self.log("🎰 Initiating paid gacha spin...", Fore.GREEN)
            url = f"{self.BASE_URL}spendGacha?{self.token}"
            headers = self.HEADERS.copy()
            payload = {"amount": 1, "strategy": "gacha"}

            try:
                self.log("📡 Sending paid gacha request...", Fore.CYAN)
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                heroes = data.get("heroes", [])
                if heroes:
                    self.log(
                        "🎉 Paid gacha spin successful! You've received the following heroes:",
                        Fore.GREEN,
                    )
                    for hero in heroes:
                        name = hero.get("name", "Unknown")
                        hero_type = hero.get("heroType", "Unknown")
                        hero_class = hero.get("class", "Unknown")
                        rarity = hero.get("rarity", "Unknown")
                        power = hero.get("power", "Unknown")
                        self.log(
                            f"🦸 Name: {name} | 🏷️ Type: {hero_type} | 🛡️ Class: {hero_class} | ⭐ Rarity: {rarity} | ⚡ Power: {power}",
                            Fore.LIGHTGREEN_EX,
                        )
                else:
                    self.log(
                        "⚠️ Paid gacha spin failed: No heroes received.", Fore.YELLOW
                    )

                self.gachaPoint -= 1
                self.log(f"🔄 Remaining paid gacha spins: {self.gachaPoint}", Fore.CYAN)

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Request error during paid gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except ValueError as e:
                self.log(f"❌ JSON decode error during paid gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except KeyError as e:
                self.log(
                    f"❌ Missing expected data during paid gacha spin: {e}", Fore.RED
                )
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except Exception as e:
                self.log(f"❌ Unexpected error during paid gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break

        if self.gachaPoint <= 0:
            self.log(
                "😢 No more paid gacha spins left. Please try again later!", Fore.YELLOW
            )

        # --- Gem Gacha Spins ---
        while self.gem >= 500:
            self.log("🎰 Initiating gem gacha spin...", Fore.GREEN)
            url = f"{self.BASE_URL}spendGacha?{self.token}"
            headers = self.HEADERS.copy()
            payload = {"amount": 1, "strategy": "gem"}

            try:
                self.log("📡 Sending gem gacha request...", Fore.CYAN)
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                heroes = data.get("heroes", [])
                if heroes:
                    self.log(
                        "🎉 Gem gacha spin successful! You've received the following heroes:",
                        Fore.GREEN,
                    )
                    for hero in heroes:
                        name = hero.get("name", "Unknown")
                        hero_type = hero.get("heroType", "Unknown")
                        hero_class = hero.get("class", "Unknown")
                        rarity = hero.get("rarity", "Unknown")
                        power = hero.get("power", "Unknown")
                        self.log(
                            f"🦸 Name: {name} | 🏷️ Type: {hero_type} | 🛡️ Class: {hero_class} | ⭐ Rarity: {rarity} | ⚡ Power: {power}",
                            Fore.LIGHTGREEN_EX,
                        )
                else:
                    self.log(
                        "⚠️ Gem gacha spin failed: No heroes received.", Fore.YELLOW
                    )

                # Adjust the paid gacha spin counter or gems as needed by your game logic.
                self.gachaPoint -= 1
                self.log(f"🔄 Remaining paid gacha spins: {self.gachaPoint}", Fore.CYAN)

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Request error during gem gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except ValueError as e:
                self.log(f"❌ JSON decode error during gem gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except KeyError as e:
                self.log(
                    f"❌ Missing expected data during gem gacha spin: {e}", Fore.RED
                )
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except Exception as e:
                self.log(f"❌ Unexpected error during gem gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break

        # --- Free Gacha Spin ---
        self.log("🎰 Initiating free gacha spin...", Fore.GREEN)
        free_url = f"{self.BASE_URL}spendGacha?{self.token}"
        free_payload = {"amount": 1, "strategy": "free"}

        try:
            self.log("📡 Sending free gacha request...", Fore.CYAN)
            free_response = requests.post(
                free_url, headers=self.HEADERS, json=free_payload
            )
            free_response.raise_for_status()
            free_data = free_response.json()

            free_heroes = free_data.get("heroes", [])
            if free_heroes:
                self.log(
                    "🎉 Free gacha spin successful! You've received the following heroes:",
                    Fore.GREEN,
                )
                for hero in free_heroes:
                    name = hero.get("name", "Unknown")
                    hero_type = hero.get("heroType", "Unknown")
                    hero_class = hero.get("class", "Unknown")
                    rarity = hero.get("rarity", "Unknown")
                    power = hero.get("power", "Unknown")
                    self.log(
                        f"🦸 Name: {name} | 🏷️ Type: {hero_type} | 🛡️ Class: {hero_class} | ⭐ Rarity: {rarity} | ⚡ Power: {power}",
                        Fore.LIGHTGREEN_EX,
                    )
            else:
                self.log("⚠️ Free gacha spin failed: No heroes received.", Fore.YELLOW)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error during free gacha spin: {e}", Fore.RED)
            self.log(f"📄 Response content: {free_response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ JSON decode error during free gacha spin: {e}", Fore.RED)
            self.log(f"📄 Response content: {free_response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Missing expected data during free gacha spin: {e}", Fore.RED)
            self.log(f"📄 Response content: {free_response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error during free gacha spin: {e}", Fore.RED)
            self.log(f"📄 Response content: {free_response.text}", Fore.RED)

    def send_heroes_to_challenges(self) -> None:
        self.log("🚀 Initiating mission deployment...", Fore.GREEN)
        headers = {**self.HEADERS}

        # Fungsi helper untuk melakukan request dengan mekanisme retry saat timeout
        def request_with_retry(method: str, url: str, headers: dict, json_payload=None, timeout=5):
            import time
            while True:
                try:
                    if method.lower() == "get":
                        response = requests.get(url, headers=headers, timeout=timeout)
                    elif method.lower() == "post":
                        response = requests.post(url, headers=headers, json=json_payload, timeout=timeout)
                    response.raise_for_status()
                    return response
                except requests.exceptions.Timeout:
                    self.log(f"⏳ Timeout occurred Retrying...", Fore.YELLOW)
                    time.sleep(1)
                    continue
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Request error for {url}: {e}", Fore.RED)
                    raise e

        # Helper function to evaluate an upgrade formula
        def evaluate_formula(formula: str, level: float, star: float) -> float:
            safe_formula = formula.replace("^", "**")
            try:
                result = eval(safe_formula, {"__builtins__": {}}, {"level": level, "star": star})
                return int(result)
            except Exception as e:
                self.log(f"❌ Error evaluating formula '{formula}': {e}", Fore.RED)
                return 0

        # Get user data (heroes & resources)
        try:
            heroes_url = f"{self.BASE_URL}getUserData?{self.token}"
            hero_response = request_with_retry("get", heroes_url, headers, timeout=5)
            user_data = hero_response.json()
            player = user_data.get("player", {})
            available_heroes = player.get("heroes", [])
            if not available_heroes:
                self.log("⚠️ No heroes in your collection!", Fore.YELLOW)
                return
            # Juga ambil hero cards yang digunakan untuk upgrade bintang
            resources = player.get("resources", {})
            hero_cards = resources.get("heroCard", {})
            self.log(f"🤩 Found {len(available_heroes)} heroes from user data.", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching hero data: {e}", Fore.RED)
            self.log(f"📄 Response: {hero_response.text if 'hero_response' in locals() else 'No response'}", Fore.RED)
            return

        # Fetch hero definitions needed for upgrades and mission requirements
        try:
            self.log("🔍 Fetching hero definitions for upgrades...", Fore.GREEN)
            url_all = f"{self.BASE_URL}getAllHeroes?{self.token}"
            response_all = request_with_retry("get", url_all, headers, timeout=5)
            hero_definitions = response_all.json()
            if not hero_definitions:
                self.log("⚠️ No hero definitions found!", Fore.YELLOW)
                return

            # Fetch missions (constellations)
            constellations = []
            mission_ids = set()
            start_index = 0
            while True:
                payload = {"startIndex": start_index, "amount": 6}
                constellations_url = f"{self.BASE_URL}getConstellations?{self.token}"
                response = request_with_retry("post", constellations_url, headers, json_payload=payload, timeout=5)
                data = response.json()
                mission_list = data.get("constellations", [])
                if not mission_list:
                    self.log("⚠️ No more missions available.", Fore.YELLOW)
                    break

                batch_has_locked = False
                for mission in mission_list:
                    mandatory_slots_unlocked = True
                    # Cek setiap challenge slot di mission
                    for challenge in mission.get("challenges", []):
                        for idx, slot in enumerate(challenge.get("orderedSlots", [])):
                            if not slot.get("optional", False) and not slot.get("unlocked", True):
                                self.log(f"🔒 Mandatory slot {idx} in mission '{mission.get('name', 'Unknown')}' is locked.", Fore.YELLOW)
                                mandatory_slots_unlocked = False
                                break
                        if not mandatory_slots_unlocked:
                            break

                    if not mandatory_slots_unlocked:
                        self.log(f"🔒 Mission '{mission.get('name', 'Unknown')}' has locked mandatory slots. Stopping mission fetch.", Fore.YELLOW)
                        batch_has_locked = True
                        break

                    unique_id = mission.get("id", mission.get("name"))
                    if unique_id not in mission_ids:
                        constellations.append(mission)
                        mission_ids.add(unique_id)
                        self.log(f"✨ Found mission: {mission.get('name', 'Unknown')}.", Fore.CYAN)

                if batch_has_locked:
                    break
                start_index += len(mission_list)

            if not constellations:
                self.log("⚠️ No missions with all mandatory slots unlocked.", Fore.YELLOW)
                return

            self.log(f"✨ Found {len(constellations)} missions.", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching missions: {e}", Fore.RED)
            self.log(f"📄 Response: {response.text if 'response' in locals() else 'No response'}", Fore.RED)
            return

        # Helper function: Upgrade hero (both star and level) to meet the challenge requirements
        def upgrade_hero_for_challenge(hero: dict, required_level: int, required_stars: int) -> dict:
            hero_type = hero.get("heroType")
            matching_def = next((d for d in hero_definitions if d.get("heroType") == hero_type), None)
            if not matching_def:
                self.log(f"⚠️ No hero definition found for heroType: {hero_type}", Fore.YELLOW)
                return hero

            # --- Upgrade Star if needed ---
            while hero.get("stars", 1) < required_stars:
                # Check if the hero card for this hero is available
                card_available = None
                if isinstance(hero_cards, dict):
                    for key, card in hero_cards.items():
                        if card.get("heroType") == hero_type:
                            card_available = card
                            break
                else:
                    for card in hero_cards:
                        if card.get("heroType") == hero_type:
                            card_available = card
                            break
                if not card_available:
                    self.log(f"⚠️ No hero card available for star upgrade for hero '{hero.get('name')}'.", Fore.YELLOW)
                    break

                available_amount = card_available.get("amount", 0)
                cost_star = hero.get("costStar", 0)
                if available_amount < cost_star:
                    self.log(f"⚠️ Not enough hero cards for star upgrade for hero '{hero.get('name')}' (Required: {cost_star}, Available: {available_amount}).", Fore.YELLOW)
                    break

                star_upgrade_url = f"{self.BASE_URL}starUpHero?{self.token}"
                payload = {"heroType": hero_type}
                try:
                    self.log(f"⬆️ Attempting star upgrade for hero '{hero.get('name')}'...", Fore.CYAN)
                    star_response = request_with_retry("post", star_upgrade_url, headers, json_payload=payload, timeout=5)
                    star_data = star_response.json()
                    if star_data.get("success", False):
                        # Assume the response returns updated hero data (with increased stars)
                        hero = star_data.get("hero", hero)
                        card_available["amount"] = available_amount - cost_star
                        self.log(f"🎉 Star upgrade successful: Hero '{hero.get('name')}' now has {hero.get('stars', '?')} stars.", Fore.GREEN)
                    else:
                        self.log(f"⚠️ Star upgrade failed for hero '{hero.get('name')}': {star_data.get('message', 'Unknown error')}", Fore.YELLOW)
                        break
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Request error during star upgrade for hero '{hero.get('name')}': {e}", Fore.RED)
                    break

            # --- Upgrade Level if needed ---
            upgrade_url = f"{self.BASE_URL}levelUpHero?{self.token}"
            upgrade_count = 0
            while hero.get("level", 1) < required_level:
                cost_gold = evaluate_formula(matching_def.get("costLevelGoldFormula", "0"), hero.get("level", 1), hero.get("stars", 1))
                cost_green = evaluate_formula(matching_def.get("costLevelGreenFormula", "0"), hero.get("level", 1), hero.get("stars", 1))
                cost_purple = 0  # Add purple formula if applicable

                if self.coin < cost_gold or self.green_stones < cost_green or self.purple_stones < cost_purple:
                    self.log(f"⚠️ Not enough resources to upgrade level for hero '{hero.get('name')}'.", Fore.YELLOW)
                    break

                payload = {"heroType": hero_type, "strategy": "one"}
                try:
                    self.log(f"⬆️ Attempting level upgrade for hero '{hero.get('name')}'...", Fore.CYAN)
                    upgrade_response = request_with_retry("post", upgrade_url, headers, json_payload=payload, timeout=5)
                    upgrade_data = upgrade_response.json()

                    spent_gold = upgrade_data.get("spentGold", 0)
                    spent_green = upgrade_data.get("spentGreenStones", 0)
                    spent_purple = upgrade_data.get("spentPurpleStones", 0)

                    self.coin -= spent_gold
                    self.green_stones -= spent_green
                    self.purple_stones -= spent_purple

                    hero = upgrade_data.get("hero", hero)
                    upgrade_count += 1
                    self.log(f"✅ Level upgrade #{upgrade_count} successful for hero '{hero.get('name')}' (Level: {hero.get('level')}).", Fore.GREEN)
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Request error during level upgrade for hero '{hero.get('name')}': {e}", Fore.RED)
                    break
            if upgrade_count > 0:
                self.log(f"ℹ️ Total level upgrades for hero '{hero.get('name')}': {upgrade_count}", Fore.CYAN)
            return hero

        # Set untuk melacak hero yang sudah digunakan agar tidak dipakai lagi
        used_heroes = set()

        # Process each mission
        for constellation in constellations:
            constellation_name = constellation.get("name", "Unknown Mission")
            self.log(f"🔸 Processing mission: {constellation_name}", Fore.CYAN)

            # Ambil data hero yang sudah digunakan dari challenge yang sudah berjalan,
            # tapi jangan skip seluruh misi jika ada sebagian challenge yang kosong.
            for challenge in constellation.get("challenges", []):
                for slot in challenge.get("orderedSlots", []):
                    if slot.get("unlocked", True):
                        assigned = slot.get("occupiedBy", "").strip()
                        if assigned and assigned.lower() != "empty":
                            used_heroes.add(assigned)

            # Claim rewards untuk refresh status mission
            try:
                claim_url = f"{self.BASE_URL}claimChallengesRewards?{self.token}"
                claim_response = request_with_retry("get", claim_url, headers, timeout=5)
                self.log(f"🔄 Claimed challenge rewards for mission '{constellation_name}'.", Fore.CYAN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Error claiming rewards for mission '{constellation_name}': {e}", Fore.RED)
                self.log("📄 (Response not shown)", Fore.RED)

            challenges = constellation.get("challenges", [])
            mission_started = False

            # Process setiap challenge dalam misi
            for challenge in challenges:
                challenge_type = challenge.get("challengeType", "UnknownType")
                challenge_name = challenge.get("name", "Unnamed Challenge")
                received = challenge.get("received", 0)
                value = challenge.get("value", 0)

                if received >= value:
                    self.log(f"⚠️ Challenge '{challenge_name}' is complete (received: {received}, required: {value}). Skipping.", Fore.YELLOW)
                    continue

                ordered_slots = challenge.get("orderedSlots", [])
                # Cek apakah ada slot yang unlocked dan sudah terisi
                if any(slot.get("occupiedBy", "").strip().lower() != "empty" for slot in ordered_slots if slot.get("unlocked", True)):
                    self.log(f"⚠️ Challenge '{challenge_name}' is already in progress. Skipping.", Fore.YELLOW)
                    for slot in ordered_slots:
                        if slot.get("unlocked", True):
                            assigned = slot.get("occupiedBy", "").strip()
                            if assigned and assigned.lower() != "empty":
                                used_heroes.add(assigned)
                    continue

                # Ambil slot pertama yang unlocked sebagai referensi untuk persyaratan
                unlocked_slots = [slot for slot in ordered_slots if slot.get("unlocked", True)]
                if not unlocked_slots:
                    self.log(f"⚠️ No unlocked slots available for challenge '{challenge_name}'.", Fore.YELLOW)
                    continue
                reference_slot = unlocked_slots[0]
                required_class = reference_slot.get("heroClass", "").lower()
                required_level = challenge.get("minLevel", 1)
                required_stars = challenge.get("minStars", 1)

                candidate = None
                # Cari candidate hero yang sesuai dan belum digunakan
                for hero in available_heroes:
                    hero_identifier = hero.get("heroType")
                    if hero_identifier in used_heroes:
                        continue
                    if hero.get("class", "").lower() != required_class:
                        continue
                    # Jika hero sudah memenuhi persyaratan, gunakan langsung
                    if hero.get("level", 1) >= required_level and hero.get("stars", 1) >= required_stars:
                        candidate = hero
                        break
                    # Jika belum, jadikan hero tersebut candidate untuk diupgrade
                    candidate = hero
                    break

                if candidate:
                    self.log(f"ℹ️ Candidate found for challenge '{challenge_name}': {candidate.get('name')} (Type: {candidate.get('heroType')}).", Fore.CYAN)
                    candidate = upgrade_hero_for_challenge(candidate, required_level, required_stars)
                    if candidate.get("level", 1) < required_level or candidate.get("stars", 1) < required_stars:
                        self.log(f"⚠️ Hero '{candidate.get('name')}' failed to meet the requirements for challenge '{challenge_name}' after upgrades.", Fore.YELLOW)
                        candidate = None

                if candidate:
                    # Cari slot yang unlocked dan masih kosong untuk assignment
                    slot_id = None
                    for idx, slot in enumerate(ordered_slots):
                        if slot.get("unlocked", True) and slot.get("occupiedBy", "").strip().lower() == "empty":
                            slot_id = idx
                            break
                    if slot_id is None:
                        self.log(f"⚠️ No available unlocked slot found for challenge '{challenge_name}'.", Fore.YELLOW)
                        continue

                    assignment = {"slotId": slot_id, "heroType": candidate.get("heroType")}
                    self.log(f"✅ Assigned hero '{candidate.get('name')}' for challenge '{challenge_name}' in slot {slot_id}.", Fore.LIGHTGREEN_EX)
                    used_heroes.add(candidate.get("heroType"))
                    send_payload = {"challengeType": challenge_type, "heroes": [assignment]}
                    try:
                        self.log(f"🚀 Sending hero for challenge '{challenge_name}'...", Fore.CYAN)
                        send_url = f"{self.BASE_URL}sendToChallenge?{self.token}"
                        send_response = request_with_retry("post", send_url, headers, json_payload=send_payload, timeout=5)
                        send_data = send_response.json()
                        if send_data.get("success", False):
                            self.log(f"🎉 Challenge '{challenge_name}' initiated with 1 hero.", Fore.GREEN)
                            mission_started = True
                        else:
                            self.log(f"⚠️ Challenge '{challenge_name}' failed to initiate.", Fore.YELLOW)
                    except requests.exceptions.RequestException as e:
                        if "error_challenge_in_progress" in str(e) or ("error_challenge_in_progress" in send_response.text):
                            self.log(f"⚠️ Challenge '{challenge_name}' is already in progress. Skipping.", Fore.YELLOW)
                        else:
                            self.log(f"❌ Error sending hero for challenge '{challenge_name}': {e}", Fore.RED)
                            self.log("📄 Sending failed due to server error.", Fore.RED)
                else:
                    # Fallback: Jika tidak ada candidate dan masih ada slot yang terkunci (unlocked == False)
                    if any(not slot.get("unlocked", True) for slot in ordered_slots):
                        self.log(f"⚠️ No suitable candidate found for challenge '{challenge_name}'. Attempting to open locked slot...", Fore.YELLOW)
                        open_payload = {"challengeType": challenge_type}
                        self.log(f"challenge type: {challenge_type}", Fore.CYAN)
                        try:
                            self.log(f"🚀 Attempting to open locked slot for challenge '{challenge_name}'...", Fore.CYAN)
                            open_slot_url = f"{self.BASE_URL}openSlotChallenge?{self.token}"
                            open_response = request_with_retry("post", open_slot_url, headers, json_payload=open_payload, timeout=15)
                            # Jika response content sudah panjang atau response success bernilai true,
                            # anggap pembukaan slot berhasil.
                            if len(open_response.text) > 200 or open_response.json().get("success", False):
                                self.log(f"🎉 Locked slot opened successfully for challenge '{challenge_name}'.", Fore.GREEN)
                            else:
                                self.log(f"⚠️ Failed to open locked slot for challenge '{challenge_name}': {open_response.json().get('message', 'Unknown error')}", Fore.YELLOW)
                                self.log(f"📄 Response content: {open_response.text}", Fore.RED)
                        except requests.exceptions.RequestException as e:
                            self.log(f"❌ Request error while opening locked slot for challenge '{challenge_name}': {e}", Fore.RED)
                            self.log(f"📄 Response content: {open_response.text if 'open_response' in locals() else 'No response'}", Fore.RED)

            self.log(f"🔄 Finished processing challenges for mission '{constellation_name}'.", Fore.CYAN)
            if mission_started:
                self.log(f"✅ Mission '{constellation_name}' initiated successfully.", Fore.GREEN)
            else:
                self.log(f"⚠️ No challenge in mission '{constellation_name}' could be started.", Fore.YELLOW)

        self.log("🏁 Mission deployment completed!", Fore.GREEN)

    def shop(self) -> None:
        self.log("🛒 Initiating free material purchase...", Fore.GREEN)
        url = f"{self.BASE_URL}buyShop?{self.token}"
        payload = {"slotType": "free"}

        try:
            self.log("💳 Sending purchase request to the shop...", Fore.CYAN)
            response = requests.post(url, headers=self.HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ok":
                self.log(
                    "✅ Purchase successful! Enjoy your free materials!", Fore.GREEN
                )
            else:
                self.log("⚠️ Purchase failed: Unexpected response status.", Fore.YELLOW)
                self.log("📄 Please try again later.", Fore.YELLOW)

        except requests.exceptions.RequestException:
            self.log(
                "❌ Purchase failed due to a network error. Please try again later.",
                Fore.RED,
            )
        except ValueError:
            self.log(
                "❌ Purchase failed due to a data processing error. Please try again later.",
                Fore.RED,
            )
        except Exception:
            self.log(
                "❌ An unexpected error occurred during the purchase. Please try again later.",
                Fore.RED,
            )

    def daily(self) -> None:
        """
        Retrieve and claim the daily reward:
        - Retrieve daily rewards from the API endpoint.
        - Find the reward with state "available" and display its type, amount, and day.
        - Claim the daily reward using the claim API endpoint.
        """
        # --- Retrieve Daily Rewards ---
        self.log("📅 Retrieving daily rewards...", Fore.GREEN)
        url = f"{self.BASE_URL}getDailyRewards?{self.token}"
        headers = self.HEADERS.copy()

        try:
            self.log("📡 Sending request to get daily rewards...", Fore.CYAN)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            rewards_list = data.get("rewards", [])

            # Find rewards with state "available"
            available_rewards = [
                r for r in rewards_list if r.get("state") == "available"
            ]
            if available_rewards:
                for reward in available_rewards:
                    reward_type = reward.get("rewardType", "Unknown")
                    reward_amount = reward.get("rewardAmount", "Unknown")
                    reward_day = reward.get("rewardDay", "Unknown")
                    self.log(
                        f"🎁 Available Reward: Type: {reward_type}, Amount: {reward_amount}, Day: {reward_day}",
                        Fore.LIGHTGREEN_EX,
                    )
            else:
                self.log("⚠️ No available daily rewards found.", Fore.YELLOW)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error while retrieving daily rewards: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return
        except ValueError as e:
            self.log(
                f"❌ JSON decode error while retrieving daily rewards: {e}", Fore.RED
            )
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return
        except KeyError as e:
            self.log(
                f"❌ Missing expected data while retrieving daily rewards: {e}",
                Fore.RED,
            )
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return
        except Exception as e:
            self.log(
                f"❌ Unexpected error while retrieving daily rewards: {e}", Fore.RED
            )
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return

        # --- Claim Daily Reward ---
        self.log("📅 Claiming daily reward...", Fore.GREEN)
        claim_url = f"{self.BASE_URL}claimDailyRewards?{self.token}"
        try:
            self.log("📡 Sending request to claim daily reward...", Fore.CYAN)
            claim_response = requests.get(claim_url, headers=headers)
            claim_response.raise_for_status()
            claim_data = claim_response.json()
            claimed_reward = claim_data.get("rewards", {})
            reward_type = claimed_reward.get("rewardType", "Unknown")
            reward_amount = claimed_reward.get("rewardAmount", "Unknown")
            reward_day = claimed_reward.get("rewardDay", "Unknown")
            self.log(
                f"🎉 Daily reward claimed: Type: {reward_type}, Amount: {reward_amount}, Day: {reward_day}",
                Fore.LIGHTGREEN_EX,
            )
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error while claiming daily reward: {e}", Fore.RED)
            self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ JSON decode error while claiming daily reward: {e}", Fore.RED)
            self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
        except KeyError as e:
            self.log(
                f"❌ Missing expected data while claiming daily reward: {e}", Fore.RED
            )
            self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error while claiming daily reward: {e}", Fore.RED)
            self.log(f"📄 Response content: {claim_response.text}", Fore.RED)

    def task(self) -> None:
        self.log("🔍 Fetching missions...", Fore.GREEN)
        missions_url = f"{self.BASE_URL}getMissions?{self.token}"
        try:
            response = requests.get(missions_url, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()
            missions = data.get("missions", [])
            if not missions:
                self.log("⚠️ No missions found!", Fore.YELLOW)
                return
            self.log(f"✨ Retrieved {len(missions)} missions.", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching missions: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return
        except ValueError as e:
            self.log(f"❌ JSON decode error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            return

        # List each mission for the user.
        for mission in missions:
            mission_key = mission.get("missionKey", "Unknown")
            claimed = mission.get("claimed", False)
            progress = mission.get("progress", 0)
            availible = mission.get("availible", False)
            rewards = mission.get("rewards", [])
            link = mission.get("link", "")
            self.log(
                f"📋 Mission: {mission_key} | Claimed: {claimed} | Progress: {progress} | Available: {availible} | Rewards: {rewards} | Link: {link}",
                Fore.LIGHTGREEN_EX,
            )

        # For each mission, attempt to start and then claim if available.
        for mission in missions:
            mission_key = mission.get("missionKey", "Unknown")
            # If mission is not claimed and not available, try to report the mission event.
            if not mission.get("claimed", False) and not mission.get(
                "availible", False
            ):
                report_url = f"{self.BASE_URL}reportMissionEvent?{self.token}"
                payload = {"missionKey": mission_key}
                try:
                    self.log(
                        f"🚀 Reporting mission event for '{mission_key}'...", Fore.CYAN
                    )
                    report_response = requests.post(
                        report_url, headers=self.HEADERS, json=payload
                    )
                    report_response.raise_for_status()
                    report_data = report_response.json()
                    self.log(
                        f"🎉 Mission event reported for '{mission_key}'.", Fore.GREEN
                    )
                    # Optionally, display updated mission status:
                    updated = next(
                        (
                            m
                            for m in report_data.get("missions", [])
                            if m.get("missionKey") == mission_key
                        ),
                        None,
                    )
                    if updated:
                        self.log(
                            f"   → Updated: Progress: {updated.get('progress')}, Available: {updated.get('availible')}",
                            Fore.LIGHTGREEN_EX,
                        )
                except requests.exceptions.RequestException as e:
                    self.log(
                        f"❌ Error reporting mission event for '{mission_key}': {e}",
                        Fore.RED,
                    )
                except ValueError as e:
                    self.log(
                        f"❌ JSON decode error during mission event for '{mission_key}': {e}",
                        Fore.RED,
                    )

            # If mission is available (and not claimed), try to claim it.
            if not mission.get("claimed", False) and mission.get("availible", False):
                claim_url = f"{self.BASE_URL}claimMission?{self.token}"
                payload = {"missionKey": mission_key}
                try:
                    self.log(f"🚀 Claiming mission '{mission_key}'...", Fore.CYAN)
                    claim_response = requests.post(
                        claim_url, headers=self.HEADERS, json=payload
                    )
                    claim_response.raise_for_status()
                    claim_data = claim_response.json()
                    self.log(
                        f"🎉 Mission '{mission_key}' claimed successfully.", Fore.GREEN
                    )
                    updated = next(
                        (
                            m
                            for m in claim_data.get("missions", [])
                            if m.get("missionKey") == mission_key
                        ),
                        None,
                    )
                    if updated:
                        self.log(
                            f"   → Updated: Claimed: {updated.get('claimed')}",
                            Fore.LIGHTGREEN_EX,
                        )
                except requests.exceptions.RequestException as e:
                    self.log(
                        f"❌ Error claiming mission '{mission_key}': {e}", Fore.RED
                    )
                except ValueError as e:
                    self.log(
                        f"❌ JSON decode error during mission claim for '{mission_key}': {e}",
                        Fore.RED,
                    )

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


if __name__ == "__main__":
    chi = sleepagotchi()
    index = 0
    max_index = len(chi.query_list)
    config = chi.load_config()
    if config.get("proxy", False):
        proxies = chi.load_proxies()

    chi.log(
        "🎉 [LIVEXORDS] === Welcome to Sleepagotchi LITE Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    chi.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = chi.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        chi.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        if config.get("proxy", False):
            chi.override_requests()
        else:
            chi.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)
        chi.login(index)

        chi.log("🛠️ Starting task execution...")
        tasks = {
            "daily": "📅 Daily: Claim your daily bonus automatically.",
            "task": "📋 Missions: Check and claim your mission rewards.",
            "spin_gacha": "🎰 Gacha: Try your luck for heroes and resources.",
            "shop": "🛒 Shop: Get free materials from the shop.",
            "send_heroes_to_challenges": "🚀 Challenges: Deploy heroes to earn extra rewards.",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            chi.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                chi.log(f"🔄 Executing {task_name}...")
                getattr(chi, task_key)()

        if index == max_index - 1:
            chi.log("🔁 All accounts processed. Restarting loop.")
            chi.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            chi.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
