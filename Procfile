web: gunicorn github-leaderboard:app --workers $WEB_CONCURRENCY --preload --max-requests 1000 --log-file -
# ~~~~~~~
# XXX add this commandline option to gunicorn once we're on gunicorn >= 19.2:
# --max_requests_jitter 100
# ~~~~~~~

