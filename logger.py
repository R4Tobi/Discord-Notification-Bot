import time

class Logger:

    def getTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def log(self, msg):
        print(f"\033[30m{self.getTime()} \033[94m{'INFO'}     \033[95m{'custom.bot'} \033[0m{msg}")