from apscheduler.schedulers.blocking import BlockingScheduler
import daily_summary

sched = BlockingScheduler()

@sched.scheduled_job("cron", hour=8, minute=0)
def send_daily_summary():
    daily_summary.main()

if __name__ == "__main__":
    print("Starting scheduler... it will run daily_summary.main() at 08:00.")
    sched.start()
