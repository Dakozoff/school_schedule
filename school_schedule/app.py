from utils.console import Console
from database import Database

if __name__ == "__main__":
    db = Database("schedule.db")
    console = Console(db)
    console.run()