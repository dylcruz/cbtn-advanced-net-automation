from nornir import InitNornir

nr = InitNornir(config_file='config.yaml')

def test_template(task):
    print(f'{task.host.platform}-templates')

nr.run(task=test_template)
