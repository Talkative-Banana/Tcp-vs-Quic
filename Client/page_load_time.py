import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def PLT(type, pz):
    # Configure WebDriver
    chrome_options = Options()

    proxy_host = "192.168.192.235"  # Local proxy address
    proxy_port = 6121         # Local proxy port quic
    proxy_port_t = 443         # Local proxy port tcp

    url = ''
    chrome_options.add_argument("--disable-cache")  # Explicitly disable cache
    chrome_options.add_argument("--max-old-space-size=1024")
    if(type == 'quic'):
        print("Making Quic Request")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
        chrome_options.add_argument("--no-proxy-server")
        chrome_options.add_argument("--enable-quic")
        chrome_options.add_argument("--origin-to-force-quic-on=www.example.org:443")
        chrome_options.add_argument(f"--host-rules=MAP www.example.org:443 {proxy_host}:{proxy_port}") 
        chrome_options.add_argument("--disable_certificate_verification")
        # URL to measure
        url = "https://www.example.org"
    else:
        print("Making Tcp Request")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")
        chrome_options.add_argument("--disable-quic")
        chrome_options.add_argument("--disable-http3")
        chrome_options.add_argument(f"--host-rules=MAP www.example.org:443 {proxy_host}:{proxy_port_t}")
        chrome_options.add_argument("--disable_certificate_verification")
        chrome_options.add_argument("--ignore-certificate-errors")
        # URL to measure
        url = "https://www.example.org"


    if(pz == 5):      url += "/index_5KB.html"
    elif(pz == 500):  url += "/index_500KB.html"
    elif(pz == 10):   url += "/index_10MB.html"
    elif(pz == 50):   url += "/index_50MB.html"
    elif(pz == 700):  url += "/index_700MB.html"
    #chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())

    # Initialize WebDriver with options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.set_page_load_timeout(60000000)  # Increase timeout to 180 seconds
    load_time = 0
    try:
        # Record start time
        start_time = time.time()

        # Load the page
        driver.get(url)

        # Wait for the page to load completely (optional, depends on specific elements)
        driver.find_element(By.TAG_NAME, "body")  # Ensures the page has loaded

        # Record end time
        end_time = time.time()

        # Calculate load time
        load_time = end_time - start_time
        
    finally: # Quit the driver
        #input()
        driver.quit()

    return load_time

def Quic_PLT(times, pz):
    plt_quic = []
    for i in range(times):
        load_time = PLT("quic", pz)
        print(f"Page Load Time on {i+1}th attempt: {load_time:.3f} seconds")
        plt_quic.append(load_time)

    res = sum(plt_quic) / times
    print("Average PageLoadTime using quic is: ", res)
    return res

def Tcp_PLT(times, pz):
    plt_tcp = []
    for i in range(times):
        load_time = PLT("tcp", pz)
        print(f"Page Load Time on {i+1}th attempt: {load_time:.3f} seconds")
        plt_tcp.append(load_time)

    res = sum(plt_tcp) / times
    print("Average PageLoadTime using tcp is: ", res)
    return res

itrs = int(sys.argv[1])    
type = sys.argv[2]
pz = int(sys.argv[3])

if(len(sys.argv) != 4):
    print("Invalid Usage")
    print("Correct Usage: python3 page_load_time.py [iterations] [--quic/--tcp] [-5/-500/-100/-5000]")
    exit(1)


if(type == '--quic'):
    Quic_PLT(itrs, pz)
elif(type == '--tcp'):
    Tcp_PLT(itrs, pz)
else:
    print("Invalid type")
    print("Correct Usage: python3 page_load_time.py [iterations] [--quic/--tcp] [-5/-500/-100/-5000]")
    exit(1)
