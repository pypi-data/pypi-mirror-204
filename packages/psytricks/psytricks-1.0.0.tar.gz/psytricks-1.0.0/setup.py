# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psytricks']

package_data = \
{'': ['*'], 'psytricks': ['ps1scripts/*', 'ps1scripts/dummydata/*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['psytricks = psytricks.cli:run_cli']}

setup_kwargs = {
    'name': 'psytricks',
    'version': '1.0.0',
    'description': 'PowerShell Python Citrix Tricks.',
    'long_description': '# PSytricks\n\n`P`ower`S`hell P`y`thon Ci`tri`x Tri`cks`.\n\nPun intended.\n\n![logo](https://raw.githubusercontent.com/imcf/psytricks/main/resources/images/logo.png)\n\nThis package provides an abstraction layer allowing Python code to interact with\na [Citrix Virtual Apps and Desktops (CVAD)][www_cvad] stack, i.e. to fetch\nstatus information and trigger actions on machines and sessions. It does this by\ncalling a wrapper script written in `Windows PowerShell` (note: **not**\n`PowerShell Core`, see below) that is using the *Citrix Broker PowerShell\nSnap-In* which is provided along with the `Delivery Controller` installation\nmedia.\n\n## 🤯 Are you serious?\n\nCalling PowerShell as a subprocess from within Python? 😳\n\nTo convert results to JSON and pass them back, just to parse it again in Python.\nReally? 🧐\n\n### ✅ Yes. We. Are\n\n*And the package name was chosen to reflect this.*\n\nTo be very clear: performance is abysmal, but this is *not at all* an issue for\nus. Abysmal, as in: for every wrapped call a full (new) PowerShell process needs\nto be instantiated, usually taking something like 1-2 seconds. ⏱\n\nHowever, the frequency of calls is also *very* low in our use case - not more\nthan a handful per minute, and that\'s already the peak. Therefore, having a\nrobust way of interacting with the Citrix platform outnumbers all other\narguments. 🍹\n\n## Installation\n\n### Prerequisites\n\nAs mentioned above, the *Citrix Broker PowerShell Snap-In* is required to be\ninstalled on the machine that will run the wrapper script, since its commands\nare being used to communicate with the CVAD stack. This is also the reason why\nthis package will work on ***Windows PowerShell only*** as snap-ins are not\nsupported on other PowerShell editions. Please note this also implies that the\nlatest usable PowerShell version is 5.1 as newer ones have dropped support for\nsnap-ins (but that\'s a different problem that Citrix will have to solve at some\npoint).\n\nTo install the snap-in, look for an MSI package like this in the `Delivery\nController` or `XenDesktop` installation media and install it as usual:\n\n* `Broker_PowerShellSnapIn_x64.msi`\n\n### Installing the package\n\nFor installing `psytricks` please create a `venv`, then run:\n\n```bash\npip install psytricks\n```\n\nThis will also register the CLI tool `psytricks.exe` although that one is mostly\nmeant for testing and demonstration purposes, otherwise the `*-Broker*` commands\nprovided by the PowerShell snap-in could be used directly.\n\n## What does it provide?\n\nTo interact with CVAD, a `psytricks.wrapper.PSyTricksWrapper` object needs to be\ninstantiated and passed the address of the *Delivery Controller* to connect to,\nfor example:\n\n```Python\nfrom psytricks.wrapper import PSyTricksWrapper\n\nwrapper = PSyTricksWrapper(deliverycontroller="cdc01.vdi.example.xy")\n```\n\n### Fetching status information\n\nThe wrapper object can then be used to e.g. retrieve information on the machines\ncontrolled ("brokered") by Citrix:\n\n```Python\nmachines = wrapper.get_machine_status()\n\nfor machine in machines:\n    print(f"[{machine["DNSName"]}] is in power state \'{machine["PowerState"]}\'")\nprint(f"Got status details on {len(machines)} machines.")\n```\n\n### Performing actions\n\nTo restart a machine, use something like this:\n\n```Python\nwrapper.perform_poweraction(machine="vm23.vdi.example.xy", action="restart")\n```\n\nFor placing a machine in *Maintenance Mode* use:\n\n```Python\nwrapper.set_maintenance(machine="vm42.vdi.example.xy", disable=False)\n```\n\n[www_cvad]: https://docs.citrix.com/en-us/citrix-virtual-apps-desktops\n',
    'author': 'Niko Ehrenfeuchter',
    'author_email': 'nikolaus.ehrenfeuchter@unibas.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
