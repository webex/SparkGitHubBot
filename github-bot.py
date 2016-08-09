from flask import Flask, request
import json 
import urllib, urllib2
import hmac
import hashlib

app = Flask(__name__)

SECRET_TOKEN = "EventsToSparkRoom" #Secret provided in the Github webhook config. Change this to your own secret phrase

@app.route('/', methods =['POST'])

def githubCommits():
    '''This function validates if the request is properly signed by Github.
       (If not, this is a spoofed webhook.).
       Then collects the webhook payload sent from Github and parses the parameters you want to send to Spark Room
    '''
    incoming_signature = request.headers.get('X-Hub-Signature')
    signature = 'sha1=' + hmac.new(SECRET_TOKEN, request.data, hashlib.sha1).hexdigest()
    
    if signature == incoming_signature:
        
        json_file = request.json
        
        if 'commits' in json_file:
            commit_id = json_file["commits"][0]['id']
            commit_message = json_file["commits"][0]['message']
            commit_time = json_file["commits"][0]['timestamp']
            commit_url = json_file["commits"][0]['url']
            commit_author_name = json_file["commits"][0]['author']['name']
            committer_name = json_file["commits"][0]['committer']['name']
            pusher_name = json_file["pusher"]['name']
            repo_name = json_file["repository"]['name']
            results = """**Author**: %s\n\n**Committer**: %s\n\n**Pusher**: %s\n\n**Commit Message**: %s\n\n**Commit id**: %s\n\n**Time**: %s\n\n**Repository**: %s\n\n**Commit Link**: %s<br><br>""" % (commit_author_name,committer_name,pusher_name,commit_message,commit_id,commit_time,repo_name,commit_url)
            toSpark(results)
            return 'Ok'
            
        elif 'comment' in json_file:
            comment_url = json_file["comment"]["html_url"]
            comment_user = json_file["comment"]["user"]["login"]
            commit_id = json_file["comment"]["commit_id"]
            comment = json_file["comment"]["body"]
            comment_repo = json_file["repository"]["name"]
            results = """**User**: %s\n\n**Comment on Commit**: %s\n\n**Comment url**: %s\n\n**Commit id**: %s\n\n**Repository**: %s<br><br>""" % (comment_user,comment,comment_url,commit_id,comment_repo)
            toSpark(results)
            return "Ok"
            
        
    else:
        print "Spoofed Hook"
        
        
# POST Function  that sends the commits & comments in markdown to a Spark room    
def toSpark(commits):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer BOT_TOKEN'}
    values =   {'roomId':'YOUR_ROOM_ID', 'markdown': commits }
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080, debug=True)
