import time
import os
from dotenv import load_dotenv

load_dotenv()

class Logger:

    def writeFile(self, msg):
        with open(os.getenv("LOGPATH"), "a") as f:
            f.write(msg + "\n")

    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def log(self, msg):
        print(f"\033[30m{self.getTime()} \033[94m{'INFO'}     \033[95m{'custom.bot'} \033[0m{msg}")
        self.writeFile(f"{self.getTime()} INFO  custom.bot {msg}")