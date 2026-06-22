"""
Vitalis RPG System
Character stats, boss fights, pets, gear — all driven by habit completion.
"""
import random
from datetime import date

CHARACTERS = [
    {"id": "warrior",  "name": "Warrior",   "emoji": "⚔️",  "color": "#F44336",
     "stat_bonus": "strength",  "description": "Power through every challenge"},
    {"id": "mage",     "name": "Mage",      "emoji": "🔮",  "color": "#9C27B0",
     "stat_bonus": "wisdom",    "description": "Knowledge is the greatest power"},
    {"id": "ranger",   "name": "Ranger",    "emoji": "🏹",  "color": "#4CAF50",
     "stat_bonus": "agility",   "description": "Discipline and precision"},
    {"id": "paladin",  "name": "Paladin",   "emoji": "🛡️",  "color": "#FFD700",
     "stat_bonus": "vitality",  "description": "Protect body, mind and soul"},
]

BOSSES = [
    {"id": "sloth",      "name": "The Sloth Demon",   "emoji": "😴",
     "hp": 100, "description": "Drains your energy and motivation",
     "weakness": "exercise", "reward": "⚡ Energy Crystal"},
    {"id": "gluttony",   "name": "Lord Gluttony",     "emoji": "🍔",
     "hp": 120, "description": "Tempts you away from healthy habits",
     "weakness": "nutrition", "reward": "🌿 Health Amulet"},
    {"id": "insomnia",   "name": "The Insomnia Wraith","emoji": "👻",
     "hp": 90,  "description": "Steals your sleep and clarity",
     "weakness": "sleep", "reward": "🌙 Dream Crystal"},
    {"id": "chaos",      "name": "Chaos Titan",        "emoji": "🌪️",
     "hp": 150, "description": "Destroys streaks and consistency",
     "weakness": "any", "reward": "👑 Titan's Crown"},
    {"id": "anxiety",    "name": "The Anxiety Specter","emoji": "😰",
     "hp": 110, "description": "Feeds on stress and inconsistency",
     "weakness": "meditation", "reward": "🧘 Serenity Stone"},
]

GEAR = [
    {"id": "iron_will",    "name": "Iron Will Gauntlets", "emoji": "🥊",
     "requirement": "7_streak",    "bonus": "+10% XP",  "rarity": "Common"},
    {"id": "gold_crown",   "name": "Gold Consistency Crown","emoji": "👑",
     "requirement": "30_streak",   "bonus": "+25% XP",  "rarity": "Rare"},
    {"id": "dragon_armor", "name": "Dragon Habit Armor",  "emoji": "🐉",
     "requirement": "100_checkins","bonus": "+50% XP",  "rarity": "Epic"},
    {"id": "phoenix_ring", "name": "Phoenix Ring",        "emoji": "🔥",
     "requirement": "3_habits",    "bonus": "Streak Freeze x3", "rarity": "Rare"},
    {"id": "wisdom_staff", "name": "Staff of Wisdom",     "emoji": "🔮",
     "requirement": "50_checkins", "bonus": "+15% XP",  "rarity": "Uncommon"},
]

PETS = [
    {"id": "dragon",    "name": "Ember",    "emoji": "🐲", "type": "Dragon",
     "description": "Grows stronger with your exercise streak",
     "stat": "exercise", "evolved_emoji": "🔥🐉"},
    {"id": "owl",       "name": "Sage",     "emoji": "🦉", "type": "Owl",
     "description": "Gets wiser as you read and learn",
     "stat": "reading",  "evolved_emoji": "✨🦉"},
    {"id": "wolf",      "name": "Storm",    "emoji": "🐺", "type": "Wolf",
     "description": "Loyal and fierce — thrives on consistency",
     "stat": "any",      "evolved_emoji": "⚡🐺"},
    {"id": "phoenix",   "name": "Blaze",   "emoji": "🦅", "type": "Phoenix",
     "description": "Reborn from every broken streak",
     "stat": "any",      "evolved_emoji": "🔥🦅"},
]

RARITY_COLORS = {
    "Common": "#9E9E9E",
    "Uncommon": "#4CAF50",
    "Rare": "#2196F3",
    "Epic": "#9C27B0",
    "Legendary": "#FFD700",
}


def get_character_stats(habits_data: list, character_id: str = "warrior",
                        user: dict = None) -> dict:
    char = next((c for c in CHARACTERS if c["id"] == character_id), CHARACTERS[0])
    total_checkins = sum(h.get("completed_count", 0) for h in habits_data)
    avg_streak = sum(h.get("current_streak", 0) for h in habits_data) / max(len(habits_data), 1)
    max_streak = max((h.get("longest_streak", 0) for h in habits_data), default=0)

    # Level and XP come from the single source of truth: the users table
    # (db.add_xp uses level = 1 + xp // 100). Fall back to check-in-derived
    # values only when no user record is supplied.
    if user is not None:
        total_xp = user.get("xp", 0)
        level = user.get("level", 1 + total_xp // 100)
        xp_in_level = total_xp % 100
        xp_to_next = 100
    else:
        total_xp = total_checkins * 10
        level = 1 + total_checkins // 20
        xp_in_level = total_checkins % 20
        xp_to_next = 20

    # Stats based on habits
    strength  = min(100, sum(h.get("completed_count", 0) for h in habits_data
                             if "exercise" in h.get("name","").lower() or
                                "workout" in h.get("name","").lower()) * 5)
    vitality  = min(100, sum(h.get("completed_count", 0) for h in habits_data
                             if "water" in h.get("name","").lower() or
                                "sleep" in h.get("name","").lower()) * 5)
    wisdom    = min(100, sum(h.get("completed_count", 0) for h in habits_data
                             if "read" in h.get("name","").lower() or
                                "study" in h.get("name","").lower() or
                                "meditat" in h.get("name","").lower()) * 5)
    agility   = min(100, int(avg_streak * 10))
    endurance = min(100, int(max_streak * 3))

    hp = 100 + level * 10
    mp = 50 + wisdom // 2

    return {
        "character": char,
        "level": level,
        "xp": total_xp,
        "xp_in_level": xp_in_level,
        "xp_to_next": xp_to_next,
        "hp": hp, "max_hp": hp,
        "mp": mp, "max_mp": mp,
        "stats": {
            "Strength":  max(1, strength),
            "Vitality":  max(1, vitality),
            "Wisdom":    max(1, wisdom),
            "Agility":   max(1, agility),
            "Endurance": max(1, endurance),
        }
    }

def get_current_boss(habits_data: list) -> dict:
    if not habits_data:
        boss = dict(BOSSES[0])
        boss["current_hp"] = boss["hp"]
        boss["progress_pct"] = 0
        return boss
    avg_checkins = sum(h.get("completed_count", 0) for h in habits_data) / max(len(habits_data), 1)
    boss_idx = min(int(avg_checkins // 10), len(BOSSES) - 1)
    boss = dict(BOSSES[boss_idx])
    completed = sum(h.get("completed_count", 0) for h in habits_data)
    boss_progress = min(completed % 20, 20)
    boss["current_hp"] = max(0, boss["hp"] - boss_progress * (boss["hp"] // 20))
    boss["progress_pct"] = int((boss_progress / 20) * 100)
    return boss

def get_unlocked_gear(habits_data: list) -> list:
    if not habits_data:
        return []
    total_checkins = sum(h.get("completed_count", 0) for h in habits_data)
    max_streak = max((h.get("longest_streak", 0) for h in habits_data), default=0)
    num_habits = len(habits_data)
    unlocked = []
    for g in GEAR:
        req = g["requirement"]
        if req == "7_streak" and max_streak >= 7:
            unlocked.append(g)
        elif req == "30_streak" and max_streak >= 30:
            unlocked.append(g)
        elif req == "100_checkins" and total_checkins >= 100:
            unlocked.append(g)
        elif req == "50_checkins" and total_checkins >= 50:
            unlocked.append(g)
        elif req == "3_habits" and num_habits >= 3:
            unlocked.append(g)
    return unlocked


def get_pet_status(habits_data: list, pet_id: str = "dragon") -> dict:
    pet = next((p for p in PETS if p["id"] == pet_id), PETS[0])
    total = sum(h.get("completed_count", 0) for h in habits_data)
    happiness = min(100, total * 2)
    level = 1 + total // 15
    evolved = level >= 5
    return {
        "pet": pet,
        "level": level,
        "happiness": happiness,
        "evolved": evolved,
        "emoji": pet["evolved_emoji"] if evolved else pet["emoji"],
        "mood": "Overjoyed! 🎉" if happiness > 80 else
                "Happy 😊" if happiness > 50 else
                "Okay 😐" if happiness > 25 else
                "Sad 😢 — complete more habits!",
    }