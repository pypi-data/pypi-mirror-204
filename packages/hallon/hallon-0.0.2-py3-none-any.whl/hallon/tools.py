import ifcfg


def run():
    from PyInquirer import prompt
    import os
    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': 'Network tools (Use arrow keys)',
            'choices': ["View network information", "difference", "product", "divide"]
        },
    ]
    answers = prompt(questions)
    os.system('clear')
    if answers.get("user_option") == "View network information":
        questions = [
            {
                'type': 'list',
                'name': 'user_option',
                'message': 'Which info would you like to view (Use arrow keys)',
                'choices': ["IP", "Router", "Subnet-mask"]
            },
        ]
        answers = answers = prompt(questions)
        os.system('clear')
        if answers.get("user_option") == "IP":
            device_list = []
            for name, interface in ifcfg.interfaces().items():
                device_list.append(interface['device'])
            if len(device_list) > 0:
                questions = [
                    {
                        'type': 'list',
                        'name': 'user_option',
                        'message': 'Choose an interface (Use arrow keys)',
                        'choices': ["default interface"] + device_list,
                        'default': 'default'
                    },
                ]
                answers = answers = prompt(questions)
                default = ifcfg.default_interface()
                if answers.get("user_option") == "default":
                    print("-", default['device'])  # Device name
                    print("  - IPv4")  # First IPv4 found
                    if len(default['inet4']) > 0:
                        for i in default['inet4']:
                            print("     -", i)
                    else:
                        print("     - None.")
                    print("  - IPv6")  # First IPv4 found
                    if len(default['inet6']) > 0:
                        for i in default['inet6']:
                            print("     -", i)
                    else:
                        print("     - None.")
                else:
                    for name, interface in ifcfg.interfaces().items():
                        if interface['device'] == answers.get("user_option"):
                            print("-", interface['device'])  # Device name
                            print("  - IPv4")  # First IPv4 found
                            if len(interface['inet4']) > 0:
                                for i in interface['inet4']:
                                    print("     -", i)
                            else:
                                print("     - None.")
                            print("  - IPv6")  # First IPv4 found
                            if len(interface['inet6']) > 0:
                                for i in interface['inet6']:
                                    print("     -", i)
                            else:
                                print("     - None.")
                        # print(interface['netmask'])  # Backwards compat: First netmask
                        # print(interface['netmasks'])  # List of netmasks
                        # print(interface['broadcast'])  # Backwards compat: First broadcast
                        # print(interface['broadcasts'])  # List of broadcast
                        # default = ifcfg.default_interface()
            else:
                print("No device detected!")

def get_network_info():
    import ifcfg
    for i in (ifcfg.interfaces()):
        print(i)
