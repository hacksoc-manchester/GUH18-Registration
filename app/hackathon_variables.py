# HACKATHON PERSONALIZATION
import os

from django.utils import timezone

HACKATHON_NAME = 'GreatUniHack 2018'
# What's the name for the application
HACKATHON_APPLICATION_NAME = 'GreatUniHack 2018 registration'
# Hackathon timezone
TIME_ZONE = 'UTC'
# This description will be used on the html and sharing meta tags
HACKATHON_DESCRIPTION = '24 hours hacking, 250 attendees and more than 50 hacks.' \
                        'GreatUniHack 2018 aims at being a full experience and ' \
                        'bringing together a wide range of students from different ' \
                        'fields to showcase their ideas in front of leading companies.'
# Domain where application is deployed, can be set by env variable
HACKATHON_DOMAIN = os.environ.get('DOMAIN', 'localhost:8000')
# Hackathon contact email: where should all hackers contact you. It will also be used as a sender for all emails
HACKATHON_CONTACT_EMAIL = 'greatunihack@hacksoc.com'
# Hackathon logo url, will be used on all emails
HACKATHON_LOGO_URL = 'https://image.ibb.co/hYpwMp/Webp_net_resizeimage_7.png'

HACKATHON_OG_IMAGE = 'https://hackcu.org/img/hackcu_ogimage870x442.png'
# (OPTIONAL) Track visits on your website
# HACKATHON_GOOGLE_ANALYTICS = 'UA-7777777-2'
# (OPTIONAL) Hackathon twitter user
HACKATHON_TWITTER_ACCOUNT = 'GreatUniHack'
# (OPTIONAL) Hackathon Facebook page
HACKATHON_FACEBOOK_PAGE = 'GreatUniHack'
# (OPTIONAL) Github Repo for this project (so meta)
HACKATHON_GITHUB_REPO = 'https://github.com/hacksoc-manchester/GUH18-Registration/'

# (OPTIONAL) Applications deadline
HACKATHON_APP_DEADLINE = timezone.datetime(2018, 10, 9, 19, 00, tzinfo=timezone.pytz.timezone(TIME_ZONE))
# (OPTIONAL) When to arrive at the hackathon
# HACKATHON_ARRIVE = 'Registration opens at 3:00 PM and closes at 6:00 PM on Friday October 13th, ' \
#                    'the opening ceremony will be at 7:00 pm.'

# (OPTIONAL) When to arrive at the hackathon
# HACKATHON_LEAVE = 'Closing ceremony will be held on Sunday October 15th from 3:00 PM to 5:00 PM. ' \
#                   'However the projects demo fair will be held in the morning from 10:30 AM to 1 PM.'
# (OPTIONAL) Hackathon live page
HACKATHON_LIVE_PAGE = 'https://greatunihack.com'

# (OPTIONAL) Regex to automatically match organizers emails and set them as organizers when signing up
REGEX_HACKATHON_ORGANIZER_EMAIL = '^.*@hacksoc\.com$'

# (OPTIONAL) Sends 500 errors to email whilst in production mode.
HACKATHON_DEV_EMAILS = [ "kzalys@gmail.com" ]

# Reimbursement configuration
REIMBURSEMENT_ENABLED = False
CURRENCY = '£'
REIMBURSEMENT_EXPIRY_DAYS = 5
REIMBURSEMENT_REQUIREMENTS = 'You have to submit a project and demo it during the event in order to get reimbursed'
REIMBURSEMENT_DEADLINE = timezone.datetime(2018, 10, 24, 3, 14, tzinfo=timezone.pytz.timezone(TIME_ZONE))

# (OPTIONAL) Max team members. Defaults to 4
TEAMS_ENABLED = True
HACKATHON_MAX_TEAMMATES = 4

# (OPTIONAL) Code of conduct link
CODE_CONDUCT_LINK = "https://drive.google.com/open?id=1w97ARjs2b7pc4sEHzfP6VNXafUIsQhj3"
DATA_SHARING_LINK = "https://drive.google.com/open?id=1wMcJbfEhIp9FjdNbyom4RVUoTH4xc0OB"

# (OPTIONAL) Slack credentials
# Highly recommended to create a separate user account to extract the token from
SLACK = {
    'team': os.environ.get('SL_TEAM', 'test'),
    # Get it here: https://api.slack.com/custom-integrations/legacy-tokens
    'token': os.environ.get('SL_TOKEN', None)
}

# (OPTIONAL) Logged in cookie
# This allows to store an extra cookie in the browser to be shared with other application on the same domain
LOGGED_IN_COOKIE_DOMAIN = '.hacksoc.com'
LOGGED_IN_COOKIE_KEY = 'hackassistant_logged_in'

# Hardware configuration
HARDWARE_ENABLED = False
#Hardware request time length (in minutes)
HARDWARE_REQUEST_TIME = 15
