from jenkins import Jenkins, LAUNCHER_JNLP
import os
import signal
import sys
import urllib
import subprocess
import shutil
import requests
import time

agent_jar = '/var/lib/jenkins/agent.jar'
agent_name = os.environ['AGENT_NAME'] if os.environ['AGENT_NAME'] != '' else 'docker-agent-' + os.environ['HOSTNAME']
jnlp_url = os.environ['JENKINS_URL'] + '/computer/' + agent_name + '/jenkins-agent.jnlp'
agent_jar_url = os.environ['JENKINS_URL'] + '/jnlpJars/agent.jar'
print(agent_jar_url)
process = None

def clean_dir(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def agent_create(node_name, working_dir, executors, labels):
    j = Jenkins(os.environ['JENKINS_URL'], os.environ['JENKINS_USER'], os.environ['JENKINS_PASS'])
    j.create_node(node_name, remoteFS = working_dir, numExecutors = int(executors), labels = labels, launcher = LAUNCHER_JNLP)

def agent_delete(node_name):
    j = Jenkins(os.environ['JENKINS_URL'], os.environ['JENKINS_USER'], os.environ['JENKINS_PASS'])
    j.delete_node(node_name)

def agent_download(target):
    if os.path.isfile(agent_jar):
        os.remove(agent_jar)

    urllib.request.urlretrieve(os.environ['JENKINS_URL'] + '/jnlpJars/agent.jar', '/var/lib/jenkins/agent.jar')

def agent_run(agent_jar, jnlp_url):
    params = [ 'java', '-jar', agent_jar, '-jnlpUrl', jnlp_url ]
    if os.environ['JENKINS_AGENT_ADDRESS'] != '':
        params.extend([ '-connectTo', os.environ['JENKINS_AGENT_ADDRESS' ] ])

    if os.environ['AGENT_SECRET'] == '':
        params.extend([ '-jnlpCredentials', os.environ['JENKINS_USER'] + ':' + os.environ['JENKINS_PASS'] ])
    else:
        params.extend([ '-secret', os.environ['AGENT_SECRET'] ])
    return subprocess.Popen(params, stdout=subprocess.PIPE)

def signal_handler(sig, frame):
    if process != None:
        process.send_signal(signal.SIGINT)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def controller_ready(url):
    try:
        r = requests.head(url, verify=False, timeout=None)
        return r.status_code == requests.codes.ok
    except:
        return False

while not controller_ready(agent_jar_url):
    print("Controller not ready yet, sleeping for 10sec!")
    time.sleep(10)

agent_download(agent_jar)
print('Downloaded Jenkins agent jar.')

if os.environ['AGENT_WORING_DIR']:
    os.setcwd(os.environ['AGENT_WORING_DIR'])

if os.environ['CLEAN_WORKING_DIR'] == 'true':
    clean_dir(os.getcwd())
    print("Cleaned up working directory.")

if os.environ['AGENT_NAME'] == '':
    agent_create(agent_name, os.getcwd(), os.environ['AGENT_EXECUTORS'], os.environ['AGENT_LABELS'])
    print('Created temporary Jenkins agent.')

process = agent_run(agent_jar, jnlp_url)
print('Started Jenkins agent with name "' + agent_name + '" and labels [' + os.environ['AGENT_LABELS'] + '].')
process.wait()

print('Jenkins agent stopped.')
if os.environ['AGENT_NAME'] == '':
    agent_delete(agent_name)
    print('Removed temporary Jenkins agent.')
