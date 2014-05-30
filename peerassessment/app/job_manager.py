from apscheduler.scheduler import Scheduler

class JobManager(object):
    """
        This class manages the execution of scheduled jobs or tasks.
    """
    is_running = False
    sched = Scheduler()
    
    @classmethod
    def start(cls):
        if cls.is_running:
            return
        JobManager.is_running = True
        cls.sched.start()

        @cls.sched.interval_schedule(hours=1)
        def scheduled_job():
            pass

    @classmethod
    def shutdown(cls): # Not being called
        if not cls.is_running:
            return
        JobManager.is_running = False
        cls.sched.shutdown()
