import time
from modes.base_mode import Mode
from utils.lcd_manager import display_message


ASCII_ART = {
    "cat": [
        r"       /\_/\        ",
        r"      ( o.o )       ",
        r"       > ^ <        ",
        r"      /|   |\       "
    ],
    "heart": [
        r"     **     **     ",
        r"    *  *   *  *    ",
        r"    *    *    *    ",
        r"     *       *     "
    ],
    "robot": [
        r"     .-------.     ",
        r"    | o     o |    ",
        r"    |    ^    |    ",
        r"    | '-----' |    "
    ],
    "coffee": [
        r"         )(         ",
        r"        (  )        ",
        r"       .----.       ",
        r"       |____|       "
    ],
    "house": [
        r"         /\         ",
        r"        /  \        ",
        r"       /____\       ",
        r"       | [] |       "
    ],
    "tree": [
        r"         *         ",
        r"        ***        ",
        r"       *****       ",
        r"         |         "
    ],
    "rocket": [
        r"         /\        ",
        r"        /  \       ",
        r"       | () |      ",
        r"       |    |      "
    ],
    "flower": [
        r"       @-@-@        ",
        r"        \|/         ",
        r"         |          ",
        r"         |          "
    ],
    "bird": [
        r"        ___         ",
        r"       ( v )        ",
        r"      ((___))       ",
        r"        ^ ^         ",
    ],
    "snowman": [
        r"       _===_       ",
        r"      ( o.o )      ",
        r"      ( > < )      ",
        r"     _( === )_     "
    ],
    "santahat": [
        r"         *        ",
        r"        / \       ",
        r"       /   \      ",
        r"      {_____}     "
    ],
    "snowflake": [
        r"       \ | /       ",
        r"      --***--      ",
        r"      --***--      ",
        r"       / | \       "
    ],
    "lights": [
        r"     o-o-o-o-o      ",
        r"    *~*~*~*~*~*     ",
        r"   o-o-o-o-o-o-o    ",
        r"    *~*~*~*~*~*     "
    ],
    "gingerbread": [
        r"         o         ",
        r"        \|/        ",
        r"         |         ",
        r"        / \        "
    ],
    "bethlehem": [
        r"         *         ",
        r"        /|\        ",
        r"       / | \       ",
        r"      /  |  \      "
    ],
}


class AsciiArtMode(Mode):
    """ASCII art display mode."""

    command_name = "ascii"
    needs_clear = False

    def _get_random_ascii_art(self):
        """Get a random ASCII art from the collection."""
        # Use current time as seed for pseudo-random selection
        art_names = list(ASCII_ART.keys())
        index = int(time.time()) % len(art_names)
        return ASCII_ART[art_names[index]]

    def display(self, lcd, log_func, mode_params=None):
        """
        Display ASCII art on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
            mode_params: Optional name (str) of specific ASCII art to display.
                        If None, a random art is selected.
        """
        try:
            # If a specific name is provided, use it; otherwise get random art
            if mode_params is not None:
                art_name = str(mode_params).lower()
                if art_name in ASCII_ART:
                    art = ASCII_ART[art_name]
                    print(f"Displaying ASCII art: {art_name}")
                else:
                    log_func(f"Invalid ASCII art name: {art_name}. Using random art.")
                    art = self._get_random_ascii_art()
            else:
                print("Displaying random ASCII art")
                art = self._get_random_ascii_art()

            # https://forums.raspberrypi.com/viewtopic.php?t=33387
            message = "\n".join(art).replace("\\", chr(96))
            display_message(lcd, message, log_func)

            print("ASCII art displayed on LCD")

        except Exception as e:
            log_func(f"Error displaying ASCII art: {e}")
