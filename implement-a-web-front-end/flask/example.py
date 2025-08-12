from flask import Flask, render_template
from nornir import InitNornir
from nornir.core.filter import F
from nornir_scrapli.tasks import send_command

app = Flask(__name__)

@app.route('/')
def homepage_test():
    return render_template('base.html')

@app.route('/newpage')
def newpage_test():
    return render_template('newpage.html')

@app.route('/greeting')
def say_hello():
    return 'Hello there!'

@app.route('/hosts/inventory')
def get_all_inventory():
    nr = InitNornir(config_file='config.yaml')
    return render_template('inventory.html', inv=nr.inventory.hosts.values())

@app.route('/all/running')
def get_all_running():
    print('Pulling running config from all devices.')
    print('Initiating Nornir')
    nr = InitNornir(config_file='config.yaml')
    print('Pulling running configs via scrapli')
    results = nr.run(task=send_command, command='show run')
    print('Pulled all configs. Returning data to template.')
    config_list = [v.scrapli_response.result for v in results.values()]
    return render_template('running.html', config_list=config_list)

@app.route('/all/version')
def get_all_version():
    print('Pulling version information from all devices.')
    print('Initiating Nornir')
    nr = InitNornir(config_file='config.yaml')
    print('Pulling version information via scrapli')
    results = nr.run(task=send_command, command='show version')
    print('Pulled all versions. Returning data to template.')
    version_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template('version.html', version_list=version_list)

@app.route('/hosts/<hostname>/version')
def get_host_version(hostname):
    print(f'Pulling version information from device {hostname}.')
    print('Initiating Nornir')
    nr = InitNornir(config_file='config.yaml')
    filtered = nr.filter(F(hostname=hostname))
    print('Pulling version information via scrapli')
    results = filtered.run(task=send_command, command='show version')
    print('Pulled version. Returning data to template.')
    version_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template('version.html', version_list=version_list)


if __name__ == '__main__':
    app.run(debug=True)