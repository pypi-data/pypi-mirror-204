from hallon import exception
from hallon import switch


def run(l, args):
    from hallon import cli
    cli.show_welcome(l)
    main(args)


def get_lldp_dict(target):
    print("123")


def login_to_core_and_enable(core_ip, core_user, core_pass, timeout, core_port, core_en_pass):
    # login to core switch
    tn_ini = switch.core_login(core_ip, core_user, core_pass, 1, core_port)
    if not tn_ini:
        return 0
    else:
        host_name = tn_ini[1]
        tn = tn_ini[0]

        # enter enable mode
        tn = switch.enable(tn, host_name, core_en_pass)
        if not tn:
            return 0
        else:
            return [tn, host_name]


def main(args):
    from hallon import switch

    lldp_all = {}
    lldp_search_tree = []
    lldp_search_tree_history = []

    # parse arguments
    core_ip = args.core_address
    core_pass = args.core_password.strip()
    core_port = args.core_port
    core_en_pass = args.core_enable_password.strip()
    core_user = args.core_username.strip()
    uni_user = args.unified_username.strip()
    uni_pass = args.unified_password.strip()
    uni_port = args.unified_port
    uni_en_pass = args.unified_enable_password.strip()

    lldp_search_tree.append(core_ip)
    lldp_search_tree_history.append(core_ip)
    tn_obj = login_to_core_and_enable(core_ip, core_user, core_pass, 1, core_port, core_en_pass)
    if not tn_obj:
        exit()
    host_name = tn_obj[1]
    tn = tn_obj[0]

    # get lldp info of core
    tn_lldp_obj = switch.lldp_lookup(tn, host_name)
    if not tn_lldp_obj:
        exit()
    tn = tn_lldp_obj[0]
    switch.disconnect(tn)
    lldp_dict = tn_lldp_obj[1]
    lldp_all[core_ip] = lldp_dict
    if lldp_dict["lldp_num"] > 0:
        for i in lldp_dict['lldp_detail']:
            if "Management address" in lldp_dict["lldp_detail"][i]["info"].keys():
                if lldp_dict["lldp_detail"][i]["info"]["Management address"] not in lldp_search_tree_history:
                    lldp_search_tree.append(lldp_dict["lldp_detail"][i]["info"]["Management address"])
    lldp_search_tree.remove(core_ip)

    # start depth-first-search
    while len(lldp_search_tree) > 0:
        for ip in lldp_search_tree:
            print("Pending:", len(lldp_search_tree))
            print("Archived:", len(lldp_all))
            print("Failed:", len(lldp_search_tree_history) - len(lldp_all))
            print("Total processed:", len(lldp_search_tree_history))
            print(lldp_search_tree)
            print()
            lldp_search_tree_history.append(ip)
            tn_obj = login_to_core_and_enable(core_ip, core_user, core_pass, 1, core_port, core_en_pass)
            if not tn_obj:
                pass
            else:
                tn = tn_obj[0]
                host_name = tn_obj[1]

                # making telnet connection
                tn_ini = switch.tel_login(tn, ip, uni_user, uni_pass, 1, uni_port)
                if not tn_ini:
                    pass
                else:
                    tn = tn_ini[0]
                    host_name = tn_ini[1]
                    tn = switch.enable(tn, host_name, uni_en_pass)
                    if not tn:
                        pass
                    else:
                        # get lldp info of core
                        tn_lldp_obj = switch.lldp_lookup(tn, host_name)
                        if not tn_lldp_obj:
                            pass
                        else:
                            tn = tn_lldp_obj[0]
                            switch.disconnect(tn)
                            lldp_dict = tn_lldp_obj[1]
                            lldp_all[ip] = lldp_dict
                            if lldp_dict["lldp_num"] > 0:
                                for i in lldp_dict['lldp_detail']:
                                    if "Management address" in lldp_dict["lldp_detail"][i]["info"].keys():
                                        if lldp_dict["lldp_detail"][i]["info"]["Management address"] not in lldp_search_tree_history and lldp_dict["lldp_detail"][i]["info"]["Management address"] not in lldp_search_tree:
                                            lldp_search_tree.append(lldp_dict["lldp_detail"][i]["info"]["Management address"])
            lldp_search_tree.remove(ip)

    # get interface info
    # tn = switch.show_interface_status(tn, host_name)
