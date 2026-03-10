from utils.asset_registry import AssetRegistry

def get_npc_types():
    return {
        "alchemist": {
            "name": "Алхимик Татьяна",
            "profession": "Алхимик",
            "quest_item": "Красная Тинктура",
            "dialogue": "Приветствую! Я ищу Красную Тинктуру для своих экспериментов.",
            "image": AssetRegistry.NPC_ALCHEMIST,
            "hp": 100,
            "mp": 100
        },
        "bard": {
            "name": "Бард Рауль",
            "profession": "Бард",
            "quest_item": "Лютня",
            "dialogue": "Здравствуй, путник! Мне нужна Лютня для моих песен.",
            "image": AssetRegistry.NPC_BARD,
            "hp": 100,
            "mp": 100
        },
        "blacksmith": {
            "name": "Кузнец Милана",
            "profession": "Кузнец",
            "quest_item": "Железо",
            "dialogue": "Приветствую! Принеси мне Железо, и я помогу тебе.",
            "image": AssetRegistry.NPC_BLACKSMITH,
            "hp": 100,
            "mp": 100
        },
        "dealer": {
            "name": "Торговец Брукс",
            "profession": "Торговец",
            "quest_item": "Шелк",
            "dialogue": "Добрый день! Мне нужен Шелк для торговли.",
            "image": AssetRegistry.NPC_DEALER,
            "hp": 100,
            "mp": 100
        },
        "doctor": {
            "name": "Лекарь Кавен",
            "profession": "Лекарь",
            "quest_item": "Лечебная трава",
            "dialogue": "Здравствуй! Принеси мне Лечебную траву.",
            "image": AssetRegistry.NPC_DOCTOR,
            "hp": 100,
            "mp": 100
        },
        "hunter": {
            "name": "Охотник Тир",
            "profession": "Охотник",
            "quest_item": "Капкан",
            "dialogue": "Привет! Мне нужен Капкан для охоты.",
            "image": AssetRegistry.NPC_HUNTER,
            "hp": 100,
            "mp": 100
        },
        "jeweler": {
            "name": "Ювелир Мила",
            "profession": "Ювелир",
            "quest_item": "Алмаз",
            "dialogue": "Приветствую! Принеси мне Алмаз.",
            "image": AssetRegistry.NPC_JEWELER,
            "hp": 100,
            "mp": 100
        },
        "mage": {
            "name": "Волшебница Екатерина",
            "profession": "Волшебница",
            "quest_item": "Зелье Маны",
            "dialogue": "Здравствуй! Мне нужно Зелье Маны.",
            "image": AssetRegistry.NPC_MAGE,
            "hp": 100,
            "mp": 100
        },
        "sage": {
            "name": "Мудрец Соломон",
            "profession": "Мудрец",
            "quest_item": "Древний свиток",
            "dialogue": "Приветствую, путник! Принеси мне Древний свиток.",
            "image": AssetRegistry.NPC_SAGE,
            "hp": 100,
            "mp": 100
        },
        "traveler": {
            "name": "Путешественник Гитьян",
            "profession": "Путешественник",
            "quest_item": "Карта Авистана",
            "dialogue": "Здравствуй! Мне нужна Карта Авистана.",
            "image": AssetRegistry.NPC_TRAVELER,
            "hp": 100,
            "mp": 100
        }
    }
