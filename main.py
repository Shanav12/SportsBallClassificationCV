# import requirements needed
import requests
from flask import Flask, render_template, request

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
app = Flask(__name__)


# set up the routes and logic for the webserver
@app.route('/')
def home():
  return render_template('index.html')


API_URL = "https://api-inference.huggingface.co/models/Shanav12/sports_ball_classification"
headers = {"Authorization": "Bearer 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"}


def query():
  response = requests.post(API_URL,
                           headers=headers,
                           data=request.files['file'])
  return response.json()


@app.route('/classify', methods=["POST"])
def classification():
  try:
    res = query()
    for i in range(len(res)):
      res[i]['score'] = round(res[i]['score'], 3)
    context = {"results": res, "prediction": res[0]['label']}
  except KeyError:
    context = {"results": [], "prediction": ""}
  return render_template('index.html', **context)


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
  # IMPORTANT: change url to the site where you are editing this file.
  website_url = 'url'

  print(f'Try to open\n\n    https://{website_url}' + '/' + '\n\n')
  app.run(host='0.0.0.0', port=port, debug=True)
