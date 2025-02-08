from datetime import datetime
import json
import time
from colorama import Fore
import requests
from math import pow  

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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
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
            print(Fore.LIGHTBLACK_EX + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |") + " " + color + message + Fore.RESET)

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
            self.log("❌ Failed to parse config.json. Please check the file format.", Fore.RED)
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
            self.log("❌ Invalid login index. Please check your input and try again.", Fore.RED)
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
                self.log("⚠️ Login failed: Verification unsuccessful. Please check your token.", Fore.YELLOW)

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
        # Continue spinning until there are no paid gacha spins left.
        while self.gachaPoint > 0 or self.gem >= 500:
            self.log("🎰 Initiating gacha spin...", Fore.GREEN)

            # Construct the URL using self.token for authentication.
            url = f"{self.BASE_URL}spendGacha?{self.token}"
            headers = {**self.HEADERS}
            # Define the JSON payload for the POST request with strategy "gacha".
            payload = {"amount": 1, "strategy": "gacha"}

            try:
                self.log("📡 Sending gacha request...", Fore.CYAN)
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                # Retrieve the heroes from the response.
                heroes = data.get("heroes", [])
                if heroes:
                    self.log("🎉 Gacha spin successful! You've received the following heroes:", Fore.GREEN)
                    for hero in heroes:
                        name = hero.get("name", "Unknown")
                        hero_type = hero.get("heroType", "Unknown")
                        hero_class = hero.get("class", "Unknown")
                        rarity = hero.get("rarity", "Unknown")
                        power = hero.get("power", "Unknown")
                        # Display key information about each hero.
                        self.log(
                            f"🦸 Name: {name} | 🏷️ Type: {hero_type} | 🛡️ Class: {hero_class} | ⭐ Rarity: {rarity} | ⚡ Power: {power}",
                            Fore.LIGHTGREEN_EX,
                        )
                else:
                    self.log("⚠️ Gacha spin failed: No heroes received.", Fore.YELLOW)

                # Deduct one gacha spin after each request, regardless of the outcome.
                self.gachaPoint -= 1
                self.log(f"🔄 Remaining gacha spins: {self.gachaPoint}", Fore.CYAN)

            except requests.exceptions.RequestException as e:
                self.log(f"❌ Request error during gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except ValueError as e:
                self.log(f"❌ JSON decode error during gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except KeyError as e:
                self.log(f"❌ Missing expected data during gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break
            except Exception as e:
                self.log(f"❌ Unexpected error during gacha spin: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                break

        self.log("😢 No more gacha spins left. Please try again later!", Fore.YELLOW)

        # --- API Gacha Free Spin ---
        self.log("🎰 Initiating free gacha spin...", Fore.GREEN)

        # Gunakan payload dengan strategy "free"
        free_payload = {"amount": 1, "strategy": "free"}
        free_url = f"{self.BASE_URL}spendGacha?{self.token}"
        try:
            self.log("📡 Sending free gacha request...", Fore.CYAN)
            free_response = requests.post(free_url, headers=self.HEADERS, json=free_payload)
            free_response.raise_for_status()
            free_data = free_response.json()

            # Retrieve the heroes from the free spin response.
            free_heroes = free_data.get("heroes", [])
            if free_heroes:
                self.log("🎉 Free gacha spin successful! You've received the following heroes:", Fore.GREEN)
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
    
    def heroes(self) -> None:

        def evaluate_formula(formula: str, level: float, star: float) -> float:
            """
            Evaluasi formula upgrade dengan mengganti operator '^' menjadi '**'.
            Catatan: Penggunaan eval di sini diasumsikan aman karena formula berasal dari API tepercaya.
            """
            safe_formula = formula.replace('^', '**')
            try:
                # Batasi builtins untuk keamanan (meskipun tidak 100% aman)
                result = eval(safe_formula, {"__builtins__": {}}, {"level": level, "star": star})
                return int(result)
            except Exception as e:
                self.log(f"❌ Error evaluating formula '{formula}': {e}", Fore.RED)
                return 0

        self.log("🔍 Fetching your heroes collection from user data...", Fore.GREEN)
        url = f"{self.BASE_URL}getUserData?{self.token}"
        headers = {**self.HEADERS}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Extract the heroes from the player data.
            player = data.get("player", {})
            heroes_list = player.get("heroes", [])
            
            if not heroes_list:
                self.log("⚠️ No heroes found in your collection!", Fore.YELLOW)
                return

            # Create a modifiable copy of the heroes list.
            available_heroes = heroes_list.copy()

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error while fetching user data: {e}", Fore.RED)
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

        # --- Tambahan: Ambil definisi hero dari getAllHeroes untuk mendapatkan formula upgrade ---
        self.log("🔍 Fetching hero definitions...", Fore.GREEN)
        url_all = f"{self.BASE_URL}getAllHeroes?{self.token}"
        try:
            response_all = requests.get(url_all, headers=headers)
            response_all.raise_for_status()
            hero_definitions = response_all.json()
            if not hero_definitions:
                self.log("⚠️ No hero definitions found!", Fore.YELLOW)
                return
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error while fetching hero definitions: {e}", Fore.RED)
            self.log(f"📄 Response content: {response_all.text}", Fore.RED)
            return
        except ValueError as e:
            self.log(f"❌ JSON decode error for hero definitions: {e}", Fore.RED)
            self.log(f"📄 Response content: {response_all.text}", Fore.RED)
            return
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching hero definitions: {e}", Fore.RED)
            self.log(f"📄 Response content: {response_all.text}", Fore.RED)
            return

        # --- Proses upgrade untuk setiap hero ---
        while available_heroes:
            # Pilih hero terbaik berdasarkan rarity tertinggi.
            best_hero = max(available_heroes, key=lambda hero: hero.get("rarity", 0))
            self.log("🏆 Best hero selected from your collection:", Fore.GREEN)
            self.log(f"   👉 Name: {best_hero.get('name', 'Unknown')}", Fore.LIGHTGREEN_EX)
            self.log(f"   👉 Type: {best_hero.get('heroType', 'Unknown')}", Fore.LIGHTGREEN_EX)
            self.log(f"   👉 Class: {best_hero.get('class', 'Unknown')}", Fore.LIGHTGREEN_EX)
            self.log(f"   👉 Rarity: {best_hero.get('rarity', 'Unknown')}", Fore.LIGHTGREEN_EX)

            # Pastikan hero memiliki atribut level dan star (default 1 bila tidak ada)
            if "level" not in best_hero:
                best_hero["level"] = 1
            if "star" not in best_hero:
                best_hero["star"] = 1

            current_hero = best_hero
            upgrade_count = 0

            # Loop upgrade untuk hero terpilih
            while True:
                # Cari definisi hero yang sesuai (berdasarkan heroType)
                matching_def = next((d for d in hero_definitions if d.get("heroType") == current_hero.get("heroType")), None)
                if not matching_def:
                    self.log(f"⚠️ No hero definition found for heroType: {current_hero.get('heroType')}", Fore.YELLOW)
                    break

                # Hitung biaya upgrade berdasarkan formula dari definisi
                cost_gold = evaluate_formula(matching_def.get("costLevelGoldFormula", "0"), current_hero.get("level", 1), current_hero.get("star", 1))
                cost_green = evaluate_formula(matching_def.get("costLevelGreenFormula", "0"), current_hero.get("level", 1), current_hero.get("star", 1))
                cost_purple = 0  # Tidak ada formula untuk purple, diasumsikan 0

                self.log(
                    f"💸 Calculated upgrade cost for {current_hero.get('heroType')}: Gold: {cost_gold}, Green Stones: {cost_green}, Purple Stones: {cost_purple}",
                    Fore.CYAN,
                )

                # Cek apakah resource cukup untuk upgrade
                if self.coin < cost_gold or self.green_stones < cost_green or self.purple_stones < cost_purple:
                    self.log("⚠️ Not enough resources for further upgrades. Stopping upgrades for this hero.", Fore.YELLOW)
                    break

                upgrade_url = f"{self.BASE_URL}levelUpHero?{self.token}"
                payload = {"heroType": current_hero.get("heroType"), "strategy": "one"}

                try:
                    self.log("⬆️ Attempting to upgrade your hero...", Fore.CYAN)
                    upgrade_response = requests.post(upgrade_url, headers=headers, json=payload)
                    upgrade_response.raise_for_status()
                    upgrade_data = upgrade_response.json()

                    # Extract biaya resource dari upgrade response.
                    spent_gold = upgrade_data.get("spentGold", 0)
                    spent_green = upgrade_data.get("spentGreenStones", 0)
                    spent_purple = upgrade_data.get("spentPurpleStones", 0)

                    # Kurangi resource yang digunakan.
                    self.coin -= spent_gold
                    self.green_stones -= spent_green
                    self.purple_stones -= spent_purple

                    upgraded_hero = upgrade_data.get("hero", {})
                    upgrade_count += 1

                    self.log(f"✅ Upgrade #{upgrade_count} successful!", Fore.GREEN)
                    self.log(f"   👉 New Level: {upgraded_hero.get('level', 'Unknown')}", Fore.LIGHTGREEN_EX)
                    self.log(f"   👉 New Power: {upgraded_hero.get('power', 'Unknown')}", Fore.LIGHTGREEN_EX)
                    self.log(
                        f"   👉 Next Upgrade Cost - Gold: {upgraded_hero.get('costLevelGold', 'Unknown')}, "
                        f"Green Stones: {upgraded_hero.get('costLevelGreen', 'Unknown')}",
                        Fore.LIGHTGREEN_EX,
                    )
                    if "costLevelPurple" in upgraded_hero:
                        self.log(
                            f"   👉 Next Upgrade Cost - Purple Stones: {upgraded_hero.get('costLevelPurple', 'Unknown')}",
                            Fore.LIGHTGREEN_EX,
                        )

                    self.log(f"💰 Remaining Coins: {self.coin}", Fore.CYAN)
                    self.log(f"💚 Remaining Green Stones: {self.green_stones}", Fore.CYAN)
                    self.log(f"💜 Remaining Purple Stones: {self.purple_stones}", Fore.CYAN)

                    # Perbarui data hero untuk iterasi upgrade berikutnya.
                    current_hero = upgraded_hero

                    # Opsional: Jika resource tidak cukup untuk upgrade selanjutnya berdasarkan data numeric di response,
                    # bisa juga dilakukan pengecekan lagi di sini.
                    next_cost_gold = current_hero.get("costLevelGold", 0)
                    next_cost_green = current_hero.get("costLevelGreen", 0)
                    next_cost_purple = current_hero.get("costLevelPurple", 0)
                    if self.coin < next_cost_gold or self.green_stones < next_cost_green or self.purple_stones < next_cost_purple:
                        self.log("⚠️ Not enough resources for further upgrades. Stopping upgrades for this hero.", Fore.YELLOW)
                        break

                except requests.exceptions.RequestException as e:
                    if upgrade_response is not None and "error_hero_not_found" in upgrade_response.text:
                        self.log("❌ Hero not found during upgrade. Searching for another hero...", Fore.YELLOW)
                        break
                    else:
                        self.log(f"❌ Request error during hero upgrade: {e}", Fore.RED)
                        self.log(f"📄 Upgrade response content: {upgrade_response.text}", Fore.RED)
                        break
                except Exception as e:
                    self.log(f"❌ Unexpected error during hero upgrade: {e}", Fore.RED)
                    break

            # Hapus hero yang baru saja diproses dari daftar available.
            hero_type = best_hero.get("heroType")
            available_heroes = [hero for hero in available_heroes if hero.get("heroType") != hero_type]
            self.log("🔄 Searching for another hero to upgrade...", Fore.CYAN)

        self.log("🏁 Completed hero upgrades.", Fore.GREEN)

    def send_heroes_to_challenges(self) -> None:
        self.log("🚀 Initiating mission deployment...", Fore.GREEN)

        # STEP 1: Ambil data hero dari getUserData.
        try:
            heroes_url = f"{self.BASE_URL}getUserData?{self.token}"
            hero_response = requests.get(heroes_url, headers=self.HEADERS)
            hero_response.raise_for_status()
            user_data = hero_response.json()
            player = user_data.get("player", {})
            available_heroes = player.get("heroes", [])
            if not available_heroes:
                self.log("⚠️ No heroes available in your collection!", Fore.YELLOW)
                return
            self.log(f"🤩 Retrieved {len(available_heroes)} heroes from your user data.", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching heroes: {e}", Fore.RED)
            self.log(f"📄 Response content: {hero_response.text}", Fore.RED)
            return

        # STEP 2: Ambil daftar misi (constellations)
        try:
            constellations_payload = {"startIndex": 0, "amount": 6}
            constellations_url = f"{self.BASE_URL}getConstellations?{self.token}"
            constellation_response = requests.post(constellations_url, headers=self.HEADERS, json=constellations_payload)
            constellation_response.raise_for_status()
            constellation_data = constellation_response.json()
            constellations = constellation_data.get("constellations", [])
            if not constellations:
                self.log("⚠️ No missions found!", Fore.YELLOW)
                return
            self.log(f"✨ Retrieved {len(constellations)} missions.", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching missions: {e}", Fore.RED)
            self.log(f"📄 Response content: {constellation_response.text}", Fore.RED)
            return

        # Untuk mencegah penggunaan hero yang sama di misi berbeda, simpan hero yang sudah dipakai.
        used_heroes = set()

        # STEP 3: Proses setiap misi (constellation)
        for constellation in constellations:
            constellation_name = constellation.get("name", "Unknown Mission")
            progress = constellation.get("progress", 0)
            if progress == 100:
                self.log(f"⚠️ Skipping mission '{constellation_name}' as its progress is 100.", Fore.YELLOW)
                continue

            self.log(f"🔸 Processing mission: {constellation_name} (Progress: {progress}%)", Fore.CYAN)
            challenges = constellation.get("challenges", [])
            mission_started = False

            # Proses tiap challenge dalam misi
            for challenge in challenges:
                challenge_name = challenge.get("name", "Unnamed Challenge")
                challenge_type = challenge.get("challengeType", "UnknownType")
                required_skill = challenge.get("heroSkill", "").lower()  # misalnya "element1"
                challenge_time = challenge.get("time", 120)  # Menggunakan nilai waktu dari response, default 120 jika tidak ada
                self.log(f"🔎 Evaluating challenge: {challenge_name} [{challenge_type}] (Required skill: {required_skill}, Time: {challenge_time})", Fore.CYAN)

                ordered_slots = challenge.get("orderedSlots", [])
                assignments = []    # Kumpulan penugasan hero untuk challenge ini
                local_used = set()  # Hero yang akan dipakai untuk challenge ini

                # Coba assign hero untuk setiap slot kosong
                for idx, slot in enumerate(ordered_slots):
                    if slot.get("occupiedBy", "").lower() != "empty":
                        continue  # Lewati slot yang sudah terisi

                    required_class = slot.get("heroClass", "").lower()  # misalnya "ranger", "mage", atau "defender"
                    for hero in available_heroes:
                        hero_identifier = hero.get("heroType")
                        # Pastikan hero belum digunakan secara global atau di challenge ini
                        if hero_identifier in used_heroes or hero_identifier in local_used:
                            continue

                        hero_class = hero.get("class", "").lower()
                        hero_skill = hero.get("skill", "").lower()
                        if hero_class == required_class and hero_skill == required_skill:
                            assignments.append({"slotId": idx, "heroType": hero_identifier})
                            local_used.add(hero_identifier)
                            self.log(
                                f"✅ Assigned hero '{hero.get('name')}' (Type: {hero_identifier}) to slot {idx} for challenge '{challenge_name}'",
                                Fore.LIGHTGREEN_EX
                            )
                            break  # Setelah menemukan hero untuk slot ini, lanjut ke slot berikutnya

                # Jika ada minimal 1 hero yang diassign, kirim payload ke API
                if assignments:
                    used_heroes.update(local_used)
                    send_payload = {
                        "challengeType": challenge_type,
                        "heroes": assignments,
                        "time": challenge_time  # Sertakan waktu sesuai dengan nilai di challenge response
                    }
                    try:
                        self.log(f"🚀 Sending assigned heroes for challenge '{challenge_name}'...", Fore.CYAN)
                        send_url = f"{self.BASE_URL}sendToChallenge?{self.token}"
                        send_response = requests.post(send_url, headers=self.HEADERS, json=send_payload)
                        send_response.raise_for_status()
                        send_data = send_response.json()
                        if send_data.get("success", False):
                            self.log(f"🎉 Challenge '{challenge_name}' started successfully with {len(assignments)} hero(s)!", Fore.GREEN)
                            mission_started = True
                            break  # Selesai dengan challenge ini, lanjut ke misi berikutnya
                        else:
                            self.log(f"⚠️ Challenge '{challenge_name}' failed to start.", Fore.YELLOW)
                    except requests.exceptions.RequestException as e:
                        self.log(f"❌ Error sending heroes for challenge '{challenge_name}': {e}", Fore.RED)
                        self.log(f"📄 Response content: {send_response.text}", Fore.RED)
                else:
                    self.log(f"⚠️ No suitable hero found for challenge '{challenge_name}'.", Fore.YELLOW)

            if mission_started:
                self.log(f"✅ Mission '{constellation_name}' initiated. Moving to next mission.", Fore.GREEN)
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
                self.log("✅ Purchase successful! Enjoy your free materials!", Fore.GREEN)
            else:
                self.log("⚠️ Purchase failed: Unexpected response status.", Fore.YELLOW)
                self.log(f"📄 Response content: {response.text}", Fore.YELLOW)
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error during shop purchase: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ JSON decode error during shop purchase: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error during shop purchase: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)

if __name__ == "__main__":
    chi = sleepagotchi()
    index = 0
    max_index = len(chi.query_list)
    config = chi.load_config()

    chi.log("🎉 [LIVEXORDS] === Welcome to Sleepagotchi LITE Automation === [LIVEXORDS]", Fore.YELLOW)
    chi.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = chi.query_list[index]
        display_account = current_account[:10] + "..." if len(current_account) > 10 else current_account

        chi.log(f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}", Fore.YELLOW)

        chi.login(index)

        chi.log("🛠️ Starting task execution...")
        tasks = {
            "spin_gacha": "🎰 Spin the gacha to obtain new heroes and resources.",
            "heroes": "⬆️ Upgrade your best hero repeatedly until your resources run out.",
            "shop": "🛒 Purchase free materials from the shop automatically.",
            "send_heroes_to_challenges": "🚀 Deploy available heroes to missions (challenges) to earn extra rewards.",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            chi.log(f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}", Fore.YELLOW if task_status else Fore.RED)

            if task_status:
                chi.log(f"🔄 Executing {task_name}...")
                getattr(chi, task_key)()

        if index == max_index - 1:
            chi.log("🔁 All accounts processed. Restarting loop.")
            chi.log(f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting.")
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            chi.log(f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds.")
            time.sleep(config.get("delay_account_switch", 10))
            index += 1