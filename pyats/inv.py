from genie.testbed import load

testbed = load('testbed.yaml')

devices = testbed.devices

for k, v in devices.items(): print(f'{k}, {v}')