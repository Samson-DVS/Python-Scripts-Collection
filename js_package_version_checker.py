#Author: Visahl Samson David Selvam

import requests

def latest_version(package_name):
    response = requests.get(f'https://registry.npmjs.org/{package_name}/latest')
    data = response.json()
    if 'version' in data:
        return data['version']
    else:
        return "Version information not available"

def check_latest_version(package_name):
    latest = latest_version(package_name)
    print(f"Latest version of {package_name}: {latest}")

new_packages = [
    "ant-design/icons",
    "reduxjs/toolkit",
    "antd",
    "axios",
    "dayjs",
    "echarts",
    "prop-types"
]

for package_name in new_packages:
    check_latest_version(package_name)
