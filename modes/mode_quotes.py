import random
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class QuotesMode(Mode):
    """Quotes display mode - shows movie quotes."""

    command_name = "quotes"
    needs_clear = False

    def display(self, lcd, log_func, mode_params=None):
        """
        Display a movie quote on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
        """
        default_messages = [
            "May the Force be with you.\n\nStar Wars",
            "I'll be back.\n\nThe Terminator",
            "There's no place like home.\nThe Wizard of Oz",
            "Houston, we have a problem.\n\nApollo 13",
            "You can't handle the truth!\n\nA Few Good Men",
            "I'm the king of the world!\n\nTitanic",
            "Just keep swimming.\n\nDory",
            "To infinity and beyond!\n\nToy Story",
            "Life is like a box of chocolates.\n\nForrest Gump",
            "Carpe diem. Seize the day, boys.\n\nDead Poets Society",
            "Sometimes you have to take a leap.\nDead Poets Society",
            "Every man dies, not every man really lives.\nBraveheart",
            "I'm gonna make him an offer he can't refuse.\nThe Godfather",
            "After all, tomorrow is another day!\n\nGone with the Wind",
            "Roads? Where we're going, we don't need roads.\nBack to the Future",
            "The future is what you make it, so make it a good one.\nBack to the Future",
            "I feel the need, the need for speed!\n\nTop Gun",
            "Hasta la vista, baby.\n\nTerminator 2",
            "Hope is a good thing, maybe the best of things.\nShawshank",
            "Fear is the mind-killer; let it pass through you.\nDune",
            "Not all treasure is silver and gold, mate.\nJack Sparrow",
            "Run, Forrest, run!\n\nForrest Gump",
            "You make your own luck.\n\nThe Martian",
            "Happiness is only real when shared.\n\nInto the Wild",
            "Never give up hope.\n\nThe Green Mile",
            "Let the past die.\n\nStar Wars",
            "Be a goldfish, Sam.\n\nTed Lasso",
            "Human beings are never perfect.\n\nTed Lasso",
            "Get busy living, or get busy dying.\nShawshank",
            "There's no place like home.\n\nThe Wizard of Oz",
            "It is our choices, Harry, that show what we truly are.\nDumbledore",
            "Yer a wizard, Harry.\n\nHagrid",
            "We've all got something worth fighting for.\nHermione",
            "Look after your kingdom.\n\nMufasa",
            "Life's not fair, but it's still good.\nMufasa",
            "Simba, you are ready.\n\nNala",
            "Hakuna Matata.\n\nTimon & Pumba",
            "Look beyond what you see.\n\nMufasa",
            "Courage comes from within.\n\nSimba",
            "Ogres are like onions.\n\nShrek",
        ]

        message = random.choice(default_messages)  # type: ignore

        display_message(lcd, message, log_func, word_wrap=True)
