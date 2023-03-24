import datetime
from collections import Counter

# Define constants
startTime = datetime.datetime.now()
REQUESTS_THRESHOLD = 1000
INTERVAL_MINUTES = 1
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-03-23.txt'
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-01-11.txt'
filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\testlog.txt'
# Define variables to keep track of requests
ip_requests = {}
first_requests = {}
result = {}

# Define a helper function to parse the timestamp string


def parse_timestamp(timestamp_str):
    return datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')


# Parse the timestamps outside the loop
with open(filePath, 'r') as file:
    for line in file:
        components = line.split(' ')
        ip_address = components[0]
        timestamp_str = (components[3] + ' ' + components[4]
                         ).replace('[', '').replace(']', '')
        timestamp = parse_timestamp(timestamp_str)

        if ip_address not in ip_requests:
            ip_requests[ip_address] = set()
            first_requests[ip_address] = timestamp
            result[ip_address] = {"count": 0, "timestamp": None}

        ip_requests[ip_address].add(timestamp)

        oldest_allowed = timestamp - \
            datetime.timedelta(minutes=INTERVAL_MINUTES)
        ip_requests[ip_address] = ip_requests[ip_address].intersection(
            {req for req in ip_requests[ip_address] if req >= oldest_allowed})
        print(line)
        print(ip_requests[ip_address])
        print(len(ip_requests[ip_address]))
        print("="*60)
        if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and result[ip_address]["count"] == 0:
            result[ip_address]["count"] = REQUESTS_THRESHOLD
        if len(ip_requests[ip_address]) > result[ip_address]["count"] and result[ip_address]["count"] != 0:
            result[ip_address]["count"] += 1
            result[ip_address]["timestamp"] = first_requests[ip_address]

# Use a counter to count the requests
for key, val in ip_requests.items():
    request_count = Counter(val)
    if request_count:
        max_count = max(request_count.values())
        if max_count >= REQUESTS_THRESHOLD:
            result[key]["count"] = max_count
            result[key]["timestamp"] = first_requests[key]

for key, val in result.items():
    if val["timestamp"]:
        print(f"{key}: " + str(val["count"]) + ", " +
              str(val["timestamp"].timestamp()))
# print(datetime.datetime.now().timestamp())
endTime = datetime.datetime.now()
diff = endTime - startTime
print(diff.total_seconds())
