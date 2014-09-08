'''
Created on Aug 25, 2014

@author: Bart Romgens
'''

from django_cron import CronJobBase, Schedule

from userprofile.models import UserProfile, NotificationInterval

import logging
logger = logging.getLogger(__name__)


class DailyEmails(CronJobBase):
  RUN_EVERY_MINS = 1*24*60

  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'care.daily_emails'    # a unique code

  def do(self):
    interval = NotificationInterval.objects.get(name="Daily")
    userprofiles = UserProfile.objects.all().filter(historyEmailInterval=interval)
    for userprofile in userprofiles:
      logger.info(userprofile.displayname)
      userprofile.sendTransactionHistory()


class WeeklyEmails(CronJobBase):
  RUN_EVERY_MINS = 7*24*60

  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'care.weekly_emails'    # a unique code

  def do(self):
    interval = NotificationInterval.objects.get(name="Weekly")
    userprofiles = UserProfile.objects.all().filter(historyEmailInterval=interval)
    for userprofile in userprofiles:
      logger.info(userprofile.displayname)
      userprofile.sendTransactionHistory()


class MonthlyEmails(CronJobBase):
  RUN_EVERY_MINS = 30*24*60

  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'care.monthly_emails'    # a unique code

  def do(self):
    interval = NotificationInterval.objects.get(name="Monthly")
    userprofiles = UserProfile.objects.all().filter(historyEmailInterval=interval)
    for userprofile in userprofiles:
      logger.info(userprofile.displayname)
      userprofile.sendTransactionHistory()


class TestEmails(CronJobBase):
  RUN_EVERY_MINS = 5
  
  schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
  code = 'care.test2_emails'

  def do(self):
    interval = NotificationInterval.objects.get(name="Weekly")
    userprofiles = UserProfile.objects.all().filter(historyEmailInterval=interval)
  
    for userprofile in userprofiles:
      logger.info('testtesttest')
      logger.info(userprofile.displayname)
      userprofile.sendTransactionHistory()
      logger.info('testtesttest - END')