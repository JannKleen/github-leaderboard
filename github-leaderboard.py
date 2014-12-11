# Python imports
from itertools import groupby
from collections import defaultdict
import json

# Contrib imports
from flask import Flask, g
from github3 import login, user

# Local imports
import settings

app = Flask(__name__)


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
def hello_world():
    return 'Hello World!'


@app.route('/update')
def update_from_gh():
    def calculate_score(labels):
        scores = []
        for label in labels:
            scores.append(settings.label_scores.get(label, 0))
        return sum(scores)

    gh = login(getattr(settings, 'GITHUB_USERNAME'), getattr(settings, 'GITHUB_TOKEN'))
    repo = gh.repository(getattr(settings, 'GITHUB_REPO_OWNER'), getattr(settings, 'GITHUB_REPO_NAME'))
    closed_issues = list(repo.iter_issues(state='closed'))
    closed_issues = filter(lambda issue: issue.milestone is not None, closed_issues)
    response = {
        'issues': defaultdict(lambda: defaultdict(list)),
        'scores': defaultdict(lambda: defaultdict(lambda: 0)), }

    for issue in closed_issues:
        score = calculate_score([label.name for label in issue.labels])
        response['issues'][issue.milestone.title][issue.assignee.login].append(
            {'title': issue.title,
             'score': score,
             'closed': issue.closed_at.isoformat(),
             'url': issue.html_url, })
        response['scores'][issue.milestone.title][issue.assignee.login] += score
    response['rate_limit'] = gh.ratelimit_remaining
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
