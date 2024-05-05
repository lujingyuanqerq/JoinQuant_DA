import schedule
import time
from datetime import datetime


class DailyRunner:
    def __init__(self):
        self.jobs = []

    def run_daily(self, func, time_str):
        """计划每天特定时间执行某个函数。

        :param func: 要执行的函数。
        :param time_str: 字符串格式的时间HH:MM，比如 "10:30"。
        """
        job = schedule.every().day.at(time_str).do(func)
        self.jobs.append(job)

    def start(self):
        """开始执行计划任务。"""
        print("启动日常任务调度...")
        while True:
            schedule.run_pending()
            time.sleep(1)


def my_daily_task():
    print(f"执行任务... {datetime.now()}")


if __name__ == "__main__":
    runner = DailyRunner()
    # 计划每天的特定时间执行任务，例如每天的10:30
    runner.run_daily(my_daily_task, "10:30")
    runner.start()
