import telnetlib


def core_login(ip, user, pas, timeout=5, port=23):
    # print("Telnet", ip, "...", end="")
    try:
        tn = telnetlib.Telnet(ip, port=port, timeout=timeout)
        # tn.set_debuglevel(1)
    except:
        # print("Connection timeout.")
        return 0
    try:
        tn.read_until(b'Username:')
        tn.write(user.encode('utf-8') + b'\n')
        tn.read_until(b'Password:')
        tn.write(pas.encode('utf-8') + b'\n')
        info = tn.read_until(b'>', timeout=5)
        try:
            info = info.decode('gb2312')
        except:
            try:
                info = info.decode('utf-8')
            except:
                tn.close()
                return -2
        if ">" not in info:
            # print("Invalid credentials.")
            tn.close()
            return -1
        host_name = info[info.index("\n"):].strip()[:-1]
        # print("Login successful, device name:", host_name)
        return [tn, host_name]
    except:
        # print("Failed.")
        tn.close()
        return -1


def tel_login(tn, ip, user, pas, timeout=1, port=23):
    print("Telnet", ip, "...", end="")
    command = "telnet " + ip + " " + str(port)
    try:
        tn.write(command.encode('utf-8') + b'\n')
        info = tn.read_until(b'Username:', timeout=5)
        try:
            info = info.decode('gb2312')
        except:
            try:
                info = info.decode('utf-8')
            except:
                print("Decoding error.")
                tn.close()
                return -2
        if "Username" not in info:
            print("Connection timeout.")
            tn.close()
            return 0
        tn.write(user.encode('utf-8') + b'\n')
        tn.read_until(b'Password:')
        tn.write(pas.encode('utf-8') + b'\n')
        info = tn.read_until(b'>', timeout=5)
        try:
            info = info.decode('gb2312')
        except:
            try:
                info = info.decode('utf-8')
            except:
                print("Decoding error.")
                tn.close()
                return -2
        if ">" not in info:
            print("Invalid credentials.")
            tn.close()
            return -1
        host_name = info[info.index("\n"):].strip()[:-1]
        print("Login successful, device name:", host_name)
        return [tn, host_name]
    except:
        print("Failed.")
        tn.close()
        return -1


def enable(tn, host_name, enpas):
    # print("Enabling", host_name, "...", end="")
    try:
        tn.write("enable".encode('utf-8') + b'\n')
        tn.read_until(b'Password:')
        tn.write(enpas.encode('utf-8') + b'\n')
        tn.read_until(bytes(host_name + '#', 'utf8'))
        # print("Enabled.")
        return tn
    except:
        # print("Enter enable mode failed.")
        tn.close()
        return 0


def lldp_lookup(tn, host_name):
    try:
        # print("Looking for neighbors of", host_name + "...", end="")
        tn.write("terminal length 0".encode('utf-8') + b'\n')
        tn.read_until(bytes(host_name + '#', 'utf8'))
        tn.write("show lldp neighbors detail".encode('utf-8') + b'\n')
        info = tn.read_until(bytes(host_name + '#', 'utf8'))
        try:
            info = info.decode('gb2312')
        except:
            try:
                info = info.decode('utf-8')
            except:
                # print("Decoding error.")
                tn.close()
                return -1
        # print(info.strip().strip("show lldp neighbors detail").strip(host_name+"#").strip().split("----------------------------------------------------------------------------"))
        lldp_list_raw = info.strip().strip("show lldp neighbors detail").strip(host_name + "#").strip().split(
            "----------------------------------------------------------------------------")
        lldp_list = []
        for i in lldp_list_raw:
            if i.strip() != "":
                lldp_list.append(i.strip())
        if len(lldp_list) > 1:
            lldp_num = int(len(lldp_list) / 2)
            for index, i in enumerate(lldp_list):
                if ((index + 1) % 2) != 0:
                    lldp_list[index] = i[i.index("[") + 1:i.index("]")].strip()
                else:
                    lldp_list_detail = []
                    for n in i.split("\n"):
                        if n.strip() != "":
                            if ":" in n.strip():
                                lldp_list_detail_raw = []
                                for m in n.strip().split(":"):
                                    lldp_list_detail_raw.append(m.strip())
                                lldp_list_detail.append(lldp_list_detail_raw)
                    lldp_list[index] = lldp_list_detail
        else:
            lldp_num = 0
        lldp_dict = {"lldp_num": lldp_num,
                     "lldp_detail": {}
                     }
        for index, i in enumerate(lldp_list):
            lldp_dict_single = {}
            if (index + 1) % 2 != 0:
                lldp_dict_single["port"] = i
                lldp_dict_pro = {}
                for n in lldp_list[index + 1]:
                    lldp_dict_pro[n[0]] = n[1]
                lldp_dict_single["info"] = lldp_dict_pro
                lldp_dict["lldp_detail"][str(int((index + 2) / 2))] = lldp_dict_single
        # print(lldp_dict["lldp_num"], "neighbors found.")
        return [tn, lldp_dict]
    except:
        # print("Failed.")
        tn.close()
        return 0


def show_interface_status(tn, host_name):
    try:
        tn.write("terminal length 0".encode('utf-8') + b'\n')
        tn.read_until(bytes(host_name + '#', 'utf8'))
        tn.write("show interface".encode('utf-8') + b'\n')
        info = tn.read_until(bytes(host_name + '#', 'utf8'))
        try:
            info = info.decode('gb2312')
        except:
            try:
                info = info.decode('utf-8')
            except:
                tn.close()
                return -1
        int_list_raw = info.strip().strip().strip("show interface").strip(host_name + "#").split("\n=")
        int_list_raw_pro = []
        # print(len(int_list_raw))
        for i in int_list_raw:
            if i.strip() != "":
                int_list_raw_pro.append(i.strip())
        for index, i in enumerate(int_list_raw_pro):
            int_list_raw_pro[index] = i.split("\n", 1)
        if len(int_list_raw_pro) > 1:
            for index, i in enumerate(int_list_raw_pro):
                int_list_raw_pro[index][0] = i[0].replace("=", "").strip()
                int_list_raw_pro[index][1] = i[1][:i[1].index("Rxload")]
        for i in int_list_raw_pro:
            print(i[0])
            print(i[1])
    except:
        tn.close()
        return 0


def disconnect(tn):
    tn.close()
