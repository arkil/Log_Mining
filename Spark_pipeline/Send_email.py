#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:02:15 2019

@author: ankitachikodi
"""
import smtplib
import config

MY_ADDRESS = "noreply.logmining@gmail.com"
PASSWORD = "noreply@123"

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(MY_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(MY_ADDRESS, config.EMAIL_ADDR, message)
        server.quit()
        print('EMAIL SENT')
    except:
        print('FAILED')
        
subject = "!!! Anamoly DETECTED !!!"
msg = "Your logs have anamolies"

send_email(subject, msg)
        
        