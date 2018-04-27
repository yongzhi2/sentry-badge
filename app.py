from chalice import Chalice, Response
import requests
import os

app = Chalice(app_name='sentry-badge')
app.debug = True

#https://api.codacy.com/project/badge/Grade/72a7aaa0e3fd4a8db27607da159d3daa?branch=test
@app.route('/{org}/{project}')
def index(org, project):
    print("ORG", org)
    print("PROJECT", project)
    AUTH0_TOKEN = "Bearer " + os.getenv('SENTRY_TOKEN')
    url = "https://app.getsentry.com/api/0/projects/" + org + "/" + project + "/issues/?statsPeriod=24h"
    print(url)
    r = requests.get(url, headers={'Authorization': AUTH0_TOKEN})
    if r.status_code != 200:
        raise ValueError("API ERROR: " + url)
    j = r.json()
    total = 0
    color = "#62d46d"
    for group in j:
        total += int(group["count"])
    if total > 0:
        color = "#953b39"

    dict = { 'error_count': total, 'color' : color}
    body = '''
<svg xmlns="http://www.w3.org/2000/svg" width="88" height="20">
    <linearGradient id="a" x2="0" y2="100%">
      <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
      <stop offset="1" stop-opacity=".1"/>
    </linearGradient><rect rx="3" width="68" height="20" fill="#555"/>
      <rect rx="3" x="50" width="38" height="20" fill="{color}"/>
      <path fill="{color}" d="M50 0h4v20h-4z"/>
      <rect rx="3" width="88" height="20" fill="url(#a)"/>
      <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
      <text x="26" y="15" fill="#010101" fill-opacity=".3">sentry</text>
      <text x="26" y="14">sentry</text>
      <text x="68" y="15" fill="#010101" fill-opacity=".3">
        {error_count}
      </text>
      <text x="68" y="14">
        {error_count}
      </text>
    </g>
</svg>
'''.format(**dict)
    return Response(body=body,
                    status_code=200,
                    headers={'Content-Type': 'image/svg+xml'})

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
