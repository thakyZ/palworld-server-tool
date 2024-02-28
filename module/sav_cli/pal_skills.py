# pylint: disable=C0114,C0103
from enum import Enum


# https://github.com/EternalWraith/PalEdit/blob/main/PalInfo.py
class PalSkills(Enum):
    """PalSkills

    See:
        https://github.com/EternalWraith/PalEdit/blob/main/PalInfo.py
        https://github.com/EternalWraith/PalEdit/blob/main/palworld_pal_edit/resources/data/passives.json

    Args:
        Enum (str): Pal skill name per internal ID.
    """
    UNKNOWN = "Unknown"
    NONE = "None"

    ElementResist_Normal_1_PAL = "Abnormal"
    ElementResist_Dark_1_PAL = "Cheery"
    ElementResist_Dragon_1_PAL = "Dragonkiller"
    ElementResist_Ice_1_PAL = "Heated Body"
    ElementResist_Fire_1_PAL = "Suntan Lover"
    ElementResist_Leaf_1_PAL = "Botanical Barrier"
    ElementResist_Earth_1_PAL = "Earthquake Resistant"
    ElementResist_Thunder_1_PAL = "Insulated Body"
    ElementResist_Aqua_1_PAL = "Waterproof"

    ElementBoost_Normal_1_PAL = "Zen Mind"
    ElementBoost_Dark_1_PAL = "Veil of Darkness"
    ElementBoost_Dragon_1_PAL = "Blood of the Dragon"
    ElementBoost_Ice_1_PAL = "Coldblooded"
    ElementBoost_Fire_1_PAL = "Pyromaniac"
    ElementBoost_Leaf_1_PAL = "Fragrant Foliage"
    ElementBoost_Earth_1_PAL = "Power of Gaia"
    ElementBoost_Thunder_1_PAL = "Capacitor"
    ElementBoost_Aqua_1_PAL = "Hydromaniac"

    ElementBoost_Normal_2_PAL = "Celestial Emperor"
    ElementBoost_Dark_2_PAL = "Lord of the Underworld"
    ElementBoost_Dragon_2_PAL = "Divine Dragon"
    ElementBoost_Ice_2_PAL = "Ice Emperor"
    ElementBoost_Fire_2_PAL = "Flame Emperor"
    ElementBoost_Leaf_2_PAL = "Spirit Emperor"
    ElementBoost_Earth_2_PAL = "Earth Emperor"
    ElementBoost_Thunder_2_PAL = "Lord of Lightning"
    ElementBoost_Aqua_2_PAL = "Lord of the Sea"

    PAL_ALLAttack_up1 = "Brave"
    PAL_ALLAttack_up2 = "Ferocious"
    PAL_ALLAttack_down1 = "Coward"
    PAL_ALLAttack_down2 = "Pacifist"

    Deffence_up1 = "Hard Skin"
    Deffence_up2 = "Burly Body"
    Deffence_down1 = "Downtrodden"
    Deffence_down2 = "Brittle"

    TrainerMining_up1 = "Mine Foreman"
    TrainerLogging_up1 = "Logging Foreman"
    TrainerATK_UP_1 = "Vanguard"
    TrainerWorkSpeed_UP_1 = "Motivational Leader"
    TrainerDEF_UP_1 = "Stronghold Strategist"

    PAL_Sanity_Down_1 = "Positive Thinker"
    PAL_Sanity_Down_2 = "Workaholic"
    PAL_Sanity_Up_1 = "Unstable"
    PAL_Sanity_Up_2 = "Destructive"

    PAL_FullStomach_Down_1 = "Dainty Eater"
    PAL_FullStomach_Down_2 = "Diet Lover"
    PAL_FullStomach_Up_1 = "Glutton"
    PAL_FullStomach_Up_2 = "Bottomless Stomach"

    CraftSpeed_up1 = "Serious"
    CraftSpeed_up2 = "Artisan"
    CraftSpeed_down1 = "Clumsy"
    CraftSpeed_down2 = "Slacker"

    MoveSpeed_up_1 = "Nimble"
    MoveSpeed_up_2 = "Runner"
    MoveSpeed_up_3 = "Swift"

    PAL_CorporateSlave = "Work Slave"

    PAL_rude = "Hooligan"
    Noukin = "Musclehead"

    PAL_oraora = "Aggressive"

    PAL_conceited = "Conceited"

    PAL_masochist = "Masochist"
    PAL_sadist = "Sadist"

    Rare = "Lucky"
    Legend = "Legend"
