from hallon import switch
import ipaddress


def login_to_core_and_enable(core_ip, core_user, core_pass, timeout, core_port, core_en_pass):
    tn_ini = switch.core_login(core_ip, core_user, core_pass, timeout, core_port)
    if type(tn_ini) == int:
        return 0
    else:
        host_name = tn_ini[1]
        tn = tn_ini[0]

        # enter enable mode
        tn = switch.enable(tn, host_name, core_en_pass, timeout)
        if type(tn) == int:
            return 0
        else:
            return [tn, host_name]


def main(args):
    # variables
    lldp_all = {}  # dictionary for lldp info dict of all network nodes
    lldp_search_tree = []  # pending nodes list
    lldp_search_tree_history = []  # processed nodes list
    lldp_search_failed = []  # failed nodes list

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
    timeout = args.telnet_timeout

    # initialization
    lldp_search_tree.append(core_ip)

    # start dfs algo
    while len(lldp_search_tree) > 0:
        for ip in lldp_search_tree:
            print("Pending:", len(lldp_search_tree))
            print("Archived:", len(lldp_all))
            print("Failed:", len(lldp_search_failed))
            print("Total processed:", len(lldp_search_tree_history))
            # telnet core switch and enter enable mode
            tn_obj = login_to_core_and_enable(core_ip, core_user, core_pass, timeout, core_port, core_en_pass)
            if type(tn_obj) == int:  # failed
                print("Failed connecting to core switch.")
                lldp_search_failed.append(ip)
            else:  # success
                tn = tn_obj[0]  # telnet obj
                host_name = tn_obj[1]  # telnet device name

                # start telnet pending nodes
                if ip == core_ip:
                    tn_ini = switch.tel_login(tn, ip, core_user, core_pass, timeout, core_port)
                else:
                    tn_ini = switch.tel_login(tn, ip, uni_user, uni_pass, timeout, uni_port)
                if type(tn_ini) == int:
                    print("Failed connecting to target.")
                    lldp_search_failed.append(ip)
                else:
                    tn = tn_ini[0]
                    host_name = tn_ini[1]

                    # enter enable mode
                    tn = switch.enable(tn, host_name, uni_en_pass, timeout)
                    if type(tn) == int:
                        print("Failed enabling target.")
                        lldp_search_failed.append(ip)
                    else:
                        # lldp lookup in target
                        tn_lldp_obj = switch.lldp_lookup(tn, host_name)
                        if type(tn_lldp_obj) == int:
                            exit()
                        else:
                            tn = tn_lldp_obj[0]
                            lldp_dict = tn_lldp_obj[1]

                            # close current telnet session
                            switch.disconnect(tn)

                            # detect public domain ip:
                            if ipaddress.ip_address(ip).is_private:
                                lldp_all[ip] = lldp_dict

                            # process lldp_dict and update main variables
                            if lldp_dict["lldp_num"] > 0:  # has neighbors
                                for i in lldp_dict['lldp_detail']:
                                    if "Management address" in lldp_dict["lldp_detail"][i]["info"].keys():  # has management ip
                                        if lldp_dict["lldp_detail"][i]["info"]["Management address"] not in lldp_search_tree_history and lldp_dict["lldp_detail"][i]["info"]["Management address"] not in lldp_search_tree:
                                            lldp_search_tree.append(lldp_dict["lldp_detail"][i]["info"]["Management address"])
            lldp_search_tree.remove(ip)
            lldp_search_tree_history.append(ip)

        print("Pending:", len(lldp_search_tree))
        print("Archived:", len(lldp_all))
        print("Failed:", len(lldp_search_failed))
        print("Total processed:", len(lldp_search_tree_history))
