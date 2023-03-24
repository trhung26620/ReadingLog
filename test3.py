import datetime
from collections import deque

# Define constants
REQUESTS_THRESHOLD = 1000
INTERVAL_MINUTES = 1
filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-01-11.txt'

# Define variables to keep track of requests
ip_requests = {}
result = {}

# Define a helper function to parse the timestamp string


def parse_timestamp(timestamp_str):
    return datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')


with open(filePath, 'r') as file:
    # Iterate through each line in the log file
    for line in file:
        # Split the line into its components
        components = line.split(' ')

        # Extract the IP address and timestamp from the line
        ip_address = components[0]
        timestamp = parse_timestamp(
            (components[3] + ' ' + components[4]).replace('[', '').replace(']', ''))

        # Check if the IP address has already been seen
        if ip_address not in ip_requests:
            ip_requests[ip_address] = deque(maxlen=REQUESTS_THRESHOLD)
            result[ip_address] = {"count": 0, "timestamp": None}

        # Add the request to the IP address's deque of requests
        ip_requests[ip_address].append(timestamp)

        # Check if the deque is full and the requests are within the time interval
        oldest_allowed = timestamp - \
            datetime.timedelta(minutes=INTERVAL_MINUTES)
        # if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and ip_requests[ip_address][-1] >= oldest_allowed:
        if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and result[ip_address]["count"] == 0:
            result[ip_address]["count"] = REQUESTS_THRESHOLD
            result[ip_address]["timestamp"] = ip_requests[ip_address][0].timestamp()

        # Check if the deque has exceeded the threshold and the requests are within the time interval
        # elif len(ip_requests[ip_address]) > REQUESTS_THRESHOLD and ip_requests[ip_address][-1] >= oldest_allowed:
        if len(ip_requests[ip_address]) > result[ip_address]["count"] and result[ip_address]["count"] != 0:
            result[ip_address]["count"] = REQUESTS_THRESHOLD + \
                len(ip_requests[ip_address]) - REQUESTS_THRESHOLD
            result[ip_address]["timestamp"] = ip_requests[ip_address][0].timestamp()

# Print the results
for ip, res in result.items():
    if res["count"] > 0:
        print(f"{ip}: {res['count']}, {res['timestamp']}")
