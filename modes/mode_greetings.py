import random
from modes.base_mode import Mode
from utils.lcd_manager import display_message


class GreetingsMode(Mode):
    """Greetings display mode - shows hardcoded greeting messages."""

    command_name = "greetings"
    needs_clear = False

    def display(self, lcd, log_func, mode_params=None):
        """
        Display a greeting message on the LCD.

        Args:
            lcd: LCD display object
            log_func: Logging function
        """
        # Default Christmas messages in Portuguese
        default_messages = [
            "Feliz Natal!\n\nQue esta época traga muita alegria!",
            "Boas Festas!\n\nDesejo um Natal cheio de amor e paz",
            "Feliz Natal e um Próspero Ano Novo!\nCom os melhores votos de felicidade!",
            "Neste Natal, que a magia ilumine o teu coração!",
            "Que o espírito natalício traga muita felicidade a toda a família!",
            "Feliz Natal!\n\nQue 2026 seja um ano incrível!",
            "Boas Festas!\n\nQue o Ano Novo traga realizações!",
            "Feliz Natal!\n\nQue esta época traga alegria!",
            "Boas Festas!\n\nDesejo um Natal cheio de paz!",
            "Feliz Natal e um Próspero Ano Novo!",
            "Que a magia do Natal ilumine o teu dia!",
            "Que o espírito natalício traga felicidade!",
            "Feliz Natal!\n\nQue 2026 seja incrível!",
            "Boas Festas!\n\nQue o Ano Novo traga sucesso!",
            "Feliz Natal!\n\nMuita saúde e alegria!",
            "Que o Natal traga bons momentos!",
            "Boas Festas!\n\nMuito amor nesta época!",
            "Um Natal iluminado e feliz!",
            "Feliz Natal!\n\nQue os sonhos se realizem!",
            "Que este Natal seja simples e feliz!",
            "Feliz Natal e um Ano Novo feliz!",
            "Boas Festas!\n\nDias cheios de alegria!",
        ]

        message = random.choice(default_messages)  # type: ignore

        display_message(lcd, message, log_func, word_wrap=True)
