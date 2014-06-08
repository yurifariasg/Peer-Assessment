from apscheduler.scheduler import Scheduler
import assignment_updater as AssignmentUpdater
import peerassessment.settings as settings

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

        @cls.sched.interval_schedule(minutes=settings.JOB_UPDATER_TIMER)
        def scheduled_job():
            print "Checking for Assignments that needs to be updated"
            AssignmentUpdater.update_assignments()

    @classmethod
    def shutdown(cls): # Not being called
        if not cls.is_running:
            return
        JobManager.is_running = False
        cls.sched.shutdown()
