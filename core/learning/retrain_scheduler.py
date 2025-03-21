import schedule
import time
from datetime import datetime
from .adaptive_learner import AdaptiveLearner

class RetrainScheduler:
    def __init__(self, learner: AdaptiveLearner):
        self.learner = learner
        schedule.every().day.at("04:00").do(self.daily_retrain)
        schedule.every(1).hours.do(self.check_retrain_needed)

    def daily_retrain(self):
        if len(self.learner.approved_terms) > 0:
            self.learner.retrain()
            print(f"[{datetime.now()}] Performed daily retraining")

    def check_retrain_needed(self):
        if len(self.learner.approved_terms) >= 50:
            self.learner.retrain()
            print(f"[{datetime.now()}] Emergency retrain for 50+ new terms")

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
