from nornir import InitNornir
from nornir.core.filter import F
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def send_cmd(task):
    task.run(task=send_command, command='show cdp neighbors')

my_filter = nr.filter(F(region='north') & F(coast='east'))
or_filter = nr.filter(F(region='north')| F(coast='east'))
not_filter = nr.filter(~F(region='south') & ~F(coast='west'))

avd_filter = nr.filter(F(data_point__contains='MyData') & F(some_var__ge=10))

results = my_filter.run(task=send_cmd)
print_result(results)

results = or_filter.run(task=send_cmd)
print_result(results)

results = not_filter.run(task=send_cmd)
print_result(results)