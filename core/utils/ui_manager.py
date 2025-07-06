from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime
import time

class UIManager:
    def __init__(self):
        self.console = Console()

    def show_banner(self):
        banner = r"""
 ________  _______   ________ ________      ___    ___ 
|\_____  \|\  ___ \ |\  _____\\   __  \    |\  \  /  /|
 \|___/  /\ \   __/|\ \  \__/\ \  \|\  \   \ \  \/  / /
     /  / /\ \  \_|/_\ \   __\\ \  \\\  \   \ \    / / 
    /  /_/__\ \  \_|\ \ \  \_| \ \  \\\  \   \/  /  /  
   |\________\ \_______\ \__\   \ \_______\__/  / /    
    \|_______|\|_______|\|__|    \|_______|\___/ /     
                                          \|___|/      
        """
        self.console.print(Panel(banner, style="bold cyan"), justify="center")
    
    def show_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[bold green][{timestamp}][/] {message}")

    def show_error(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[bold red][{timestamp}][/] {message}")

    def progress_bar(self, seconds):
        with Progress() as progress:
            task = progress.add_task("[cyan]Waiting...", total=seconds)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(1)
