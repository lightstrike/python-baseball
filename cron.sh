#!/usr/bin/env bash
source ~/.virtualenvs/baseball/bin/activate
source ~/.virtualenvs/baseball/bin/postactivate
cd ~/applications/python-baseball
# make sure to set $TWILIO_TEXT_NUMBER in postactivate script
python baseball.py NYY $TWILIO_TEXT_NUMBER
