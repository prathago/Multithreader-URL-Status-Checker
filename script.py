import threading
import requests
import re
import csv
import logging
from queue import Queue

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

lock = threading.Lock()
results = []
threadWorkload = {}

def checkValidURL(url):
    pattern = re.compile(
        r'^(https?://)?' 
        r'([a-zA-Z0-9.-]+)'
        r'(:\d+)?'
        r'(/.*)?$' 
    )
    return pattern.match(url) is not None

checkValidURL("https://www.apple.com/in/")
    
def checkURLStatus(q, thread):
    count = 0
    while not q.empty():
        url = q.get()
        if not checkValidURL(url):
            status = "Invalid URL"
        else:
            try:
                response = requests.get(url, timeout=5)
                status = response.status_code
            except requests.RequestException:
                status = "Error"
                logging.error(f"{thread} - {url} - Error fetching URL")
        
        with lock:
            results.append({'url': url, 'status': status})
            logging.info(f"{thread} - {url} - {status}")
            count+=1
        q.task_done()
    
    with lock:
        threadWorkload[thread] = count
    
def saveToCSV():
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'status'])
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    num_threads = 5
    queue = Queue()
    threads = []

    with open('urls.txt', 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
        for url in urls:
            queue.put(url)   
    
    for i in range(num_threads):
        threadName = f'Thread-{i+1}'
        thread = threading.Thread(target=checkURLStatus, args=(queue, threadName))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    saveToCSV()

    print("\nThread Workload Distribution:")
    for name, count in threadWorkload.items():
        print(f"{name}: {count} URLs processed")

    print(f"\nTotal URLs Checked: {len(results)}")
    