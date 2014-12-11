# Python imports
import os
from collections import defaultdict
import json

# Contrib imports
from flask import Flask, g
from github3 import login

# Local imports
import settings

app = Flask(__name__, static_folder='frontend/build/web/')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = settings.db.connect()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def frontend_html():
    return app.send_static_file('frontend.html')


@app.route('/frontend.html_bootstrap.dart.js')
def frontend_js():
    return app.send_static_file('frontend.html_bootstrap.dart.js')


@app.route('/packages/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('packages', path))


@app.route('/update')
def update_from_gh():
    def calculate_score(labels):
        """ Rate the labels assigned to an issue according to the scoreboard in settings
        :param labels: labels to rate
        :return: sum of all labels
        """
        scores = []
        for label in labels:
            scores.append(settings.label_scores.get(label, 0))
        return sum(scores)

    # Connect to GH and get the repo
    gh = login(settings.GITHUB_USERNAME, settings.GITHUB_TOKEN)
    repo = gh.repository(settings.GITHUB_REPO_OWNER, settings.GITHUB_REPO_NAME)

    # Get all closed issues which have a milestone (our way to separate sprints)
    closed_issues = list(repo.iter_issues(state='closed'))
    closed_issues = filter(lambda _issue: _issue.milestone is not None, closed_issues)

    response = {
        'issues': defaultdict(lambda: defaultdict(list)),
        'scores': defaultdict(lambda: defaultdict(lambda: 0)), }

    for issue in closed_issues:
        score = calculate_score([label.name for label in issue.labels])

        # Add issue to issue list
        response['issues'][issue.milestone.title][issue.assignee.login].append(
            {'title': issue.title,
             'score': score,
             'closed': issue.closed_at.isoformat(),
             'url': issue.html_url, })

        # Add score to user aggregate score
        response['scores'][issue.milestone.title][issue.assignee.login] += score

    # Add rate limit returned from GH for debug reasons
    response['rate_limit'] = gh.ratelimit_remaining
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
