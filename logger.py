import time
import os
from dotenv import load_dotenv

load_dotenv()

class Logger:
    def __init__(self):
        self.guildLength = 0

    def writeFile(self, msg):
        with open(os.getenv("LOGPATH"), "a") as f:
            f.write(msg + "\n")

    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def log(self, guild, msg):
        guild = guild.ljust(self.guildLength)
        str = f"\033[37m{self.getTime()} \033[94m{'INFO'}     \033[35m{'custom.bot'} \033[90m{guild} \033[0m{msg}";
        print(str)
        self.writeFile(str)
    
    def error(self, guild, msg):
        guild = guild.ljust(self.guildLength)
        str = f"\033[37m{self.getTime()} \033[94m{'ERROR'}    \033[35m{'custom.bot'} \033[90m{guild} \033[0m{msg}"
        print(str)
        self.writeFile(str)

    def setGuildLength(self, length):
        self.guildLength = length + 1