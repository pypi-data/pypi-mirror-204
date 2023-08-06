from TheSilent.clear import clear
from TheSilent.command_scanner import command_scanner
from TheSilent.html_lint import html_lint
from TheSilent.sql_injection_scanner import sql_injection_scanner
from TheSilent.xss_scanner import xss_scanner

CYAN = "\033[1;36m"

# scans for security flaws and bad practices
def web_scanner(url, secure=True, tor=False, my_file=" ", crawl="0", parse=" ", delay=1, report=True, problem="all"):
    clear()

    my_sql_injection_scanner = sql_injection_scanner(url=url, secure=secure, tor=tor, my_file=my_file, crawl=crawl, parse=parse, delay=delay)
    my_xss_scanner = xss_scanner(url=url, secure=secure, tor=tor, my_file=my_file, crawl=crawl, parse=parse, delay=delay)
    command_injection_scanner = command_scanner(url, secure=secure, tor=tor, crawl=crawl, my_file=my_file, parse=parse, delay=delay)

    clear()

    print(CYAN + "command injection:")

    for i in command_injection_scanner:
        if report:
            with open(url +  ".txt", "a") as f:
                f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "sql injection:")

    for i in my_sql_injection_scanner:
        if report:
            with open(url +  ".txt", "a") as f:
                f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "xss:")

    for i in my_xss_scanner:
        if report:
            with open(url +  ".txt", "a") as f:
                f.write(i + "\n")
                
        print(CYAN + i)

    html_lint(url, secure=secure, crawl=crawl, delay=delay, tor=tor, parse=parse, problem=problem, report=report)
