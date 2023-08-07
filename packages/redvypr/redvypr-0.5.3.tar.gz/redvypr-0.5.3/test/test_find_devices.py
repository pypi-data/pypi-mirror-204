import redvypr.device


devsearch = redvypr.device.redvypr_device_scan()

devsearch.scan_modules()
#devsearch.print_modules()
print('Modules')
for k in devsearch.redvypr_devices['modules'].keys():
    print(devsearch.redvypr_devices['modules'][k])
    print('---')
print('Modules done')

print('Modules flat')
for k in devsearch.redvypr_devices_flat:
    print(k)
    print('---')


