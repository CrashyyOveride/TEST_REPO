"""
ALL SAINTS CATHOLIC COLLEGE
SOFTWARE ENGINEERING 2026 - STAGE 6 YEAR 11
Assessment Task No. 2: Object-Oriented RPG Application
Student Name: [Your Name]
Teacher: Mr McFarlane
"""

import tkinter as tk
from tkinter import scrolledtext
import random

# ==============================================================================
# 1. OBJECT-ORIENTED MODEL LAYER (Add your custom classes and attributes here)
# ==============================================================================

class GameObject:
    """Base class for all named entities in the game world."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Item(GameObject):
    """Base class for all equipment, loot, and relics."""
    def __init__(self, name: str, description: str, item_class: str, rarity: str):
        super().__init__(name, description)
        self.item_class = item_class  # e.g., "Sword class", "Dagger class"
        self.rarity = rarity          # e.g., "Common", "Rare", "Legacy", "Relic"


class Weapon(Item):
    """Specialised item class that carries damage attributes."""
    def __init__(self, name: str, description: str, item_class: str, rarity: str, damage: int, effect="None"):
        super().__init__(name, description, item_class, rarity)
        self.damage = damage
        self.effect = effect


class Character(GameObject):
    """Base structural class for players, monsters, and friendly NPCs."""
    def __init__(self, name: str, description: str, hp: int, base_damage: int):
        super().__init__(name, description)
        self.hp = hp
        self.max_hp = hp
        self.base_damage = base_damage

    def is_alive(self) -> bool:
        return self.hp > 0


class Enemy(Character):
    """Dungeon denizens that fight the player."""
    def __init__(self, name: str, description: str, hp: int, damage: int, has_wild_magic: bool):
        super().__init__(name, description, hp, damage)
        self.has_wild_magic = has_wild_magic


class Player(Character):
    """The user's entity tracking active inventory and progression states."""
    def __init__(self, name: str):
        super().__init__(name, "An individual exiled from the sky.", 100, 10)
        self.current_zone = "Oakhaven"
        self.inventory = [
            Weapon("Stick", "A normal branch.", "Sword class", "Common", 2, "Embarrassment")
        ]
        self.runes_held = 0
        self.has_light = False
        self.mary_spawned_once = False

    def check_light_source(self):
        """Dynamic check to see if the player is carrying a lit item."""
        self.has_light = any(item.name == "Holy Kris" for item in self.inventory)

# ==============================================================================
# 2. APPLICATION INTERFACE LAYER (The Tkinter Window & Event Loop Engine)
# ==============================================================================

class RPGApplication:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("EXILED: Chronicles of the World Below")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1a1a1a")

        # Initialize core data models
        self.player = Player("The Exiled")
        
        # State Machine Flags: Controls how the input field interprets typing
        # Values: "EXPLORING", "COMBAT", "MARY_PROMPT"
        self.game_state = "EXPLORING" 
        self.active_enemy = None

        # Draw the GUI elements
        self.build_ui()
        
        # Initial boot text screen display
        self.print_terminal("⚡ APPLICATION ENGINE INITIALISED LINK SUCCESSFULLY.")
        self.print_terminal("Welcome, Exiled Warrior. Your hunt for worth starts now.\n")
        self.display_location_details()

    def build_ui(self):
        """Sets up the layout split between output log and a live diagnostics panel."""
        # --- LEFT FRAME: Text Output & Input Box ---
        self.left_panel = tk.Frame(self.root, bg="#1a1a1a")
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Output Log Window
        self.terminal = scrolledtext.ScrolledText(
            self.left_panel, wrap=tk.WORD, bg="#0c0c0c", fg="#39ff14",
            insertbackground="white", font=("Consolas", 11), state=tk.DISABLED
        )
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Command Input Field Container
        self.input_container = tk.Frame(self.left_panel, bg="#1a1a1a")
        self.input_container.pack(fill=tk.X)

        self.prompt_pointer = tk.Label(self.input_container, text="CMD> ", font=("Consolas", 12, "bold"), bg="#1a1a1a", fg="#00ffff")
        self.prompt_pointer.pack(side=tk.LEFT)

        self.input_field = tk.Entry(self.input_container, bg="#262626", fg="#ffffff", font=("Consolas", 12), insertbackground="white")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", self.handle_enter_key)
        self.input_field.focus()

        # --- RIGHT FRAME: Object State Diagnostics Panel ---
        self.sidebar = tk.Frame(self.root, bg="#222222", width=250)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 12), pady=12)
        self.sidebar.pack_propagate(False)

        # Section Labels
        self.sidebar_title = tk.Label(self.sidebar, text="⚙️ GAME VARIABLES", font=("Consolas", 12, "bold"), bg="#222222", fg="#ff007f")
        self.sidebar_title.pack(pady=12)

        self.hp_text = tk.StringVar()
        self.hp_lbl = tk.Label(self.sidebar, textvariable=self.hp_text, font=("Consolas", 11), bg="#222222", fg="#ffff00")
        self.hp_lbl.pack(anchor="w", padx=12, pady=4)

        self.zone_text = tk.StringVar()
        self.zone_lbl = tk.Label(self.sidebar, textvariable=self.zone_text, font=("Consolas", 11), bg="#222222", fg="#00ffff")
        self.zone_lbl.pack(anchor="w", padx=12, pady=4)

        self.inv_title = tk.Label(self.sidebar, text="🎒 Live Inventory Array:", font=("Consolas", 11, "bold"), bg="#222222", fg="#ffffff")
        self.inv_title.pack(anchor="w", padx=12, pady=(16, 4))

        self.inventory_box = tk.Listbox(self.sidebar, bg="#111111", fg="#ffffff", font=("Consolas", 10), bd=0, highlightthickness=0)
        self.inventory_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.update_live_sidebar()

    # ==============================================================================
    # 3. CONTROLLER LAYER (Interface interaction handling mechanics)
    # ==============================================================================

    def print_terminal(self, text: str):
        """Appends formatted message blocks safely to the output display window."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, text + "\n")
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)

    def update_live_sidebar(self):
        """Queries model states dynamically to update GUI visualization metrics."""
        self.hp_text.set(f"Health: {self.player.hp}/{self.player.max_hp}")
        self.zone_text.set(f"Region: {self.player.current_zone}")
        self.inventory_box.delete(0, tk.END)
        for item in self.player.inventory:
            self.inventory_box.insert(tk.END, f"• {item.name} ({item.item_class})")

    def display_location_details(self):
        """Prints background context blocks matching the active sector string indicator."""
        zone = self.player.current_zone
        if zone == "Oakhaven":
            self.print_terminal("📍 AREA: Oakhaven [Civilian Safe Zone]")
            self.print_terminal("Surrounded by stone walls. Home to 'The Blind Boar' tavern. Touch the 'Pathfinder' stone for luck.")
        elif zone == "Ashenhollow":
            self.print_terminal("📍 AREA: Ashenhollow [1st Dungeon Domain]")
            self.print_terminal("A low-level cave network holding volatile Orbs and a hiding Lesser Dragon boss.")
        elif zone == "Anatoli":
            self.print_terminal("📍 AREA: Anatoli [Subzero Peak - Combat Active]")
            self.print_terminal("A freezing mountain settlement buried under snow. Watch out for Soldat's Expedition unit!")
        self.print_terminal("Available Commands: 'explore', 'travel [zone]', 'clear', 'help'\n")

    def handle_enter_key(self, event):
        """Intercepts keyboard inputs and routes data tokens to appropriate state machines."""
        raw_cmd = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)

        if not raw_cmd:
            return

        # Render what the user typed to the terminal screen
        self.print_terminal(f">>> {raw_cmd}")
        cleaned_cmd = raw_cmd.lower()

        # --- MANDATORY GLOBAL LORE RULE: CRITICAL OVERRIDE ---
        if "orsted" in cleaned_cmd and self.game_state != "COMBAT":
            self.print_terminal("\n❌ [CURSE ACTIVATED] You spoke the name 'Orsted' in a safe location!")
            self.print_terminal("NPCs panic and immediately throw you past the walls of the settlement!")
            self.player.current_zone = "Ashenhollow"
            self.game_state = "EXPLORING"
            self.update_live_sidebar()
            self.display_location_details()
            return

        # Route inputs to correct handling method based on current game state
        if self.game_state == "EXPLORING":
            self.parse_exploration_state(cleaned_cmd)
        elif self.game_state == "COMBAT":
            self.parse_combat_state(cleaned_cmd)
        elif self.game_state == "MARY_PROMPT":
            self.parse_mary_state(cleaned_cmd)

    # ==============================================================================
    # 4. GAME STATE ROUTERS (Add your custom functionality mechanics inside these)
    # ==============================================================================

    def parse_exploration_state(self, cmd: str):
    """Processes logic arguments when traversing world map sectors."""
    if cmd == "help":
        self.print_terminal("Controls: 'explore' | 'travel oakhaven' | 'travel ashenhollow' | 'travel anatoli' | 'clear'")
    elif cmd == "clear":
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete('1.0', tk.END)
        self.terminal.config(state=tk.DISABLED)
    elif cmd == "explore":
        self.process_exploration_logic()
    elif "travel" in cmd:
        if "oakhaven" in cmd:
            self.player.current_zone = "Oakhaven"
        elif "ashenhollow" in cmd:
            self.player.current_zone = "Ashenhollow"
        elif "anatoli" in cmd:
            self.player.current_zone = "Anatoli"
        else:
            self.print_terminal("⚠️ Coordinates broken. Destination unreachable.")
            return
        self.update_live_sidebar()
        self.display_location_details()
    else:
        self.print_terminal("❓ Input Processing Exception: Instruction string unrecognized.")

def process_exploration_logic(self):
    """Implements environmental rules and random encounters based on location [4]."""
    zone = self.player.current_zone
    roll = random.random()

    # 1. Check for Mary Althea Random Spawn Opportunity (Everywhere except Oakhaven)
    if zone != "Oakhaven" and roll < 0.30:
        self.print_terminal("\n✨ [NPC ENCOUNTER] Mary Althea steps out from a beam of light.")
        self.print_terminal("Do you want her to heal your wounds? (Type 'accept' or 'dismiss')")
        self.game_state = "MARY_PROMPT"
        return

    # 2. Sector Specific Exploration Interactions
    if zone == "Oakhaven":
        self.print_terminal("🏙️ You roam the cobblestone streets. You step up and press your hand against the Pathfinder stone. Luck is with you.")
    elif zone == "Ashenhollow":
        # Dungeon 1 Spawn Table Example
        if roll < 0.60:
            self.active_enemy = Enemy("Pure Black Orb", "An unruly ball of compressed wild magic.", 25, 6, True)
        else:
            self.active_enemy = Enemy("Drakonid Guard", "A scaled warrior wielding a sword. A 'G.G' logo is branded on its arm.", 40, 10, False)
        
        self.print_terminal(f"\n⚔️ [COMBAT SPARKED] A hostile {self.active_enemy.name} blocks your route!")
        self.print_terminal(f"Enemy Info: {self.active_enemy.description}")
        self.print_terminal("Select Action: '1' to Strike Weapon | '2' to Flee Zone")
        self.game_state = "COMBAT"
    elif zone == "Anatoli":
        # Northern Soldat Unit Interception Mechanics Check
        if roll < 0.50:
            self.print_terminal("\n🛡️ [ROUTE LOCKED] Commander Soldat Vanderbilt and his squad halt your party!")
            self.print_terminal("'This mountain route is completely restricted by the North Expedition unit. Back off, dense diver!'")
        else:
            self.print_terminal("❄️ You map freezing abandoned log cabins. The Polar Vortex winds howl nearby.")

def parse_combat_state(self, cmd: str):
    """Tracks turn interactions inside separated isolated battle parameters."""
    if not self.active_enemy:
        self.game_state = "EXPLORING"
        return

    if cmd == "1":
        # Resolve Player Damage (Weapons increase base values)
        damage_out = self.player.base_damage
        self.active_enemy.hp -= damage_out
        self.print_terminal(f"💥 You deal {damage_out} damage to the {self.active_enemy.name}!")
        
        # Check if Enemy has survived
        if self.active_enemy.is_alive():
            damage_in = self.active_enemy.base_damage
            
            # Wild Magic Surge Calculation Rule
            if self.active_enemy.has_wild_magic and random.random() > 0.70:
                damage_in *= 2
                self.print_terminal("⚠️ The enemy's wild magic surges uncontrollably!")
            
            # Check for Noid vs Light mechanic here if you add Noids later
            if self.active_enemy.name == "Noid" and self.player.has_light:
                self.print_terminal("🔦 The Noid recoils in pain from your light source, missing its attack!")
                damage_in = 0
                
            self.player.hp = max(0, self.player.hp - damage_in)
            self.print_terminal(f"🩸 {self.active_enemy.name} strikes back, dealing {damage_in} damage to you.")
            self.update_live_sidebar()
            
            # Evaluate if Player died
            if not self.player.is_alive():
                self.print_terminal("\n💀 Your soul has faded. The Exiled falls into darkness below...")
                self.input_field.config(state=tk.DISABLED) # Lock input box on Game Over
        else:
            self.print_terminal(f"🎉 Victory! The {self.active_enemy.name} dissolves into particles.")
            self.active_enemy = None
            self.game_state = "EXPLORING"
            self.print_terminal("\nYou are back to exploring. Where to next?")
            self.update_live_sidebar()
            
    elif cmd == "2":
        self.print_terminal("🏃 You turned and scrambled back away to safe corridors!")
        self.active_enemy = None
        self.game_state = "EXPLORING"
        self.display_location_details()
    else:
        self.print_terminal("Choose an option: '1' to strike or '2' to flee.")

def parse_mary_state(self, cmd: str):
    """Processes choices during Mary Althea interactions."""
    if cmd == "accept":
        self.print_terminal("✨ Mary cleans your wounds. Your health metrics are fully restored!")
        self.player.hp = self.player.max_hp
        # Lore Check: Accepting means she won't help again
        self.player.mary_spawned_once = True
        self.game_state = "EXPLORING"
        self.update_live_sidebar()
    elif cmd == "dismiss":
        self.print_terminal("👋 You nod and dismiss Mary. She blends back into shadows, ready to potentially return.")
        self.game_state = "EXPLORING"
    else:
        self.print_terminal("Please respond with either 'accept' or 'dismiss'.")

# ==============================================================================
# 5. ENTRYPOINT RUNTIME ENGINE INITIALIZER
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RPGApplication(root)
    root.mainloop()
