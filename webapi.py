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
    ch = ch.strip()
    while len(ch) > 0 and ch[-1] == '.': ch = ch.rstrip('.')
    ch = ch.split('.')
    ans = ans.strip()
    while len(ans) > 0 and ans[-1] == '.': ans = ans.rstrip('.')
    ans = ans.split('.')
    if len(ch) != len(ans): return False
    for a in range(len(ch)):
        if(ch[a] != ans[a] and ans[a] != '*'):
            return False
    return True

def gethostname(domain, zone):
    domain = domain.strip()
    while len(domain) > 0 and domain[-1] == '.': domain = domain.rstrip('.')
    zone = zone.strip()
    while len(zone) > 0 and zone[-1] == '.': zone = zone.rstrip('.')
    result = domain[::-1].replace(zone[::-1], "", 1)[::-1].strip()
    while len(result) > 0 and result[-1] == '.': result = result.rstrip('.')
    return result

@app.route('/<string:mode>',methods=['POST'])
def setrecord(mode):
    if mode != 'addrecord' or mode != 'delrecord':
        return 'Not Found', 404
    data = flask.request.get_json()
    for a in config['auth']:
        if checkdomain(data['name'].strip(), f"{a['hostname'].strip()}.{a['zone'].strip()}") and a['username'].strip() == data['username'].strip() and a['password'].strip() == data['password'].strip() and data['type'].strip() in a['allowtype']:
            process = subprocess.run(['bash', f'{mode}.sh', '-n', gethostname(data['name'], a['zone']), '-z', a['zone'].strip(), '-t', data['type'].strip(), '-d', data['data'].strip()])
            if process.returncode != 0:
                return "Error", 500
            return "Success"
    return "Bad auth", 403

if __name__ == "__main__":
    app.run(host=config['ListenHost'].strip().lstrip('[').rstrip(']'),port=int(config['ListenPort']))
