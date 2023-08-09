import flask
import yaml
import subprocess

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

app = flask.Flask(__name__)

@app.route('/',methods=['GET'])
@app.route('/help',methods=['GET'])
def help():
    return f"""
Usage: curl -H 'Content-Type: application/json' <host>/<api>

POST: 
    addrecord       Add dns record.
                    inputtype: json
                    outputtype: string
                    input:
                        name: domain name
                        type: record type
                        data: record data
                        username: username
                        password: password
                    Ex: curl -H 'Content-Type: application/json' <host>/addrecord -X POST -d '{{"name":"www.example.com", "type": "A", "data": "192.168.0.1", "username": "test", "password": "testpass"}}'
    delrecord       Delete dns record.
                    inputtype: json
                    outputtype: string
                    input:
                        name: domain name
                        type: record type
                        data: record data
                        username: username
                        password: password
                    Ex: curl -H 'Content-Type: application/json' <host>/delrecord -X POST -d '{{"name":"www.example.com", "type": "A", "data": "192.168.0.1", "username": "test", "password": "testpass"}}'
"""

def checkdomain(ch, ans):
    ch = ch.strip().rstrip('.').split('.')
    ans = ans.strip().rstrip('.').split('.')
    if len(ch) != len(ans): return False
    for a in range(len(ch)):
        if(ch[a] != ans[a] and ans[a] != '*'):
            return False
    return True

@app.route('/addrecord',methods=['POST'])
def addrecord():
    data = flask.request.get_json()
    for a in config['auth']:
        if checkdomain(f"{a['hostname'].strip()}.{a['zone'].strip()}", data['name'].strip()) and a['username'].strip() == data['username'].strip() and a['password'].strip() == data['password'].strip() and data['type'].strip() in a['allowtype']:
            process = subprocess.run(['bash', 'addrecord.sh', '-n', a['hostname'].strip(), '-z', a['zone'].strip(), '-t', data['type'].strip(), '-d', data['data'].strip()])
            if process.returncode != 0:
                return "Error", 500
            break
    return "Bad auth", 403

@app.route('/delrecord',methods=['POST'])
def delrecord():
    data = flask.request.get_json()
    if 'data' not in data: data['data'] = ''
    for a in config['auth']:
        if checkdomain(f"{a['hostname'].strip()}.{a['zone'].strip()}", data['name'].strip()) and a['username'].strip() == data['username'].strip() and a['password'].strip() == data['password'].strip() and data['type'].strip() in a['allowtype']:
            process = subprocess.run(['bash', 'delrecord.sh', '-n', a['hostname'].strip(), '-z', a['zone'].strip(), '-t', data['type'].strip(), '-d', data['data'].strip()])
            if process.returncode != 0:
                return "Error", 500
            break
    return "Bad auth", 403

if __name__ == "__main__":
    app.run(host=config['ListenHost'].strip().lstrip('[').rstrip(']'),port=int(config['ListenPort']))
