import argparse
from hallon import lang, topo


def show_welcome(l):
    print(lang.get_msg("welcome_msg", l))


def show_version(l):
    print(lang.get_msg("version_msg", l))


def generate_topology(l, args):
    from hallon import topo
    topo.run(l, args)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--cli_lang", type=str, help="client language", default=lang.get_default_lang())
    parser.add_argument("-v", "--version", help="client version", action='store_true')
    parser.add_argument("-t", "--thread_num", type=int, help="number of threads", default=1)
    parser.add_argument("-nt", "--network_topology", help="generate topology", action='store_true')
    parser.add_argument("-cadr", "--core_address", type=str, help="telnet address of the core switch")
    parser.add_argument("-cprt", "--core_port", type=int, help="telnet port of the core switch", default=23)
    parser.add_argument("-cusr", "--core_username", type=str, help="username for logging in to the core switch", default="admin")
    parser.add_argument("-cpas", "--core_password", type=str, help="password for logging in to the core switch")
    parser.add_argument("-cenpas", "--core_enable_password", type=str, help="enable password for the core switch")
    parser.add_argument("-uprt", "--unified_port", type=int, help="general telnet port", default=23)
    parser.add_argument("-uusr", "--unified_username", type=str, help="general username for telnet login")
    parser.add_argument("-upas", "--unified_password", type=str, help="general password for telnet login")
    parser.add_argument("-uenpas", "--unified_enable_password", type=str, help="general enable password for telnet")
    parser.add_argument("-tt", "--telnet_timeout", type=float, help="telnet global timeout", default=1)

    args = parser.parse_args()

    cli_lang = args.cli_lang.strip().lower()
    multi_proc_num = args.thread_num
    version_display = args.version
    network_topology = args.network_topology

    if version_display:
        show_version(cli_lang)
        exit()

    if args.telnet_timeout <= 0:
        parser.error("--telnet_timeout must be greater than 0")

    if network_topology:
        if args.network_topology and (args.core_address is None or args.core_password is None or args.core_enable_password is None):
            parser.error("--network_topology requires --core_address, --core_password and --core_enable_password")
        else:
            if args.unified_username is None:
                args.unified_username = args.core_username
            if args.unified_password is None:
                args.unified_password = args.core_password
            if args.unified_enable_password is None:
                args.unified_enable_password = args.core_enable_password
            from hallon import func
            if func.is_ipv4(args.core_address.strip()) and 0 <= args.core_port <= 65536:
                topo.main(args)
            else:
                parser.error("--core_address/--core_port invalid.")
        exit()

    if cli_lang not in lang.get_lang():
        # raise ValueError("Bad argument: -l, supported language:", lang.get_lang())
        print("Bad argument: -l, supported languages:", lang.get_lang(), ", default language:", lang.get_default_lang())
        exit()
