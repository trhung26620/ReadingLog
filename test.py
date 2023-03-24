import datetime

# Define constants
# time
startTime = datetime.datetime.now()
REQUESTS_THRESHOLD = 1000
INTERVAL_MINUTES = 1
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-03-23.txt'
filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-01-11.txt'
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\testlog.txt'

# Define variables to keep track of requests
ip_requests = {}
# first_requests = {}
result = {}
# "count" = {}
# Define a helper function to parse the timestamp string


def parse_timestamp(timestamp_str):
    return datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')


count = 0
# Open the log file
with open(filePath, 'r') as file:
    # Iterate through each line in the log file
    for line in file:
        # count += 1
        # print(count)
        # Split the line into its components
        components = line.split(' ')

        # Extract the IP address and timestamp from the line
        ip_address = components[0]
        timestamp = parse_timestamp(
            (components[3] + ' ' + components[4]).replace('[', '').replace(']', ''))

        # Check if the IP address has already been seen
        if ip_address not in ip_requests:
            ip_requests[ip_address] = []
            # first_requests[ip_address] = timestamp
            result[ip_address] = {"count": 0, "timestamp": None}

        # Add the request to the IP address's list of requests
        ip_requests[ip_address].append(timestamp)

        # Remove requests that are older than the 2-minute interval
        oldest_allowed = timestamp - \
            datetime.timedelta(minutes=INTERVAL_MINUTES)
        ip_requests[ip_address] = [
            req for req in ip_requests[ip_address] if req >= oldest_allowed]

        # print(ip_requests)
        # print("*"*50)
        # print(first_requests)
        # print(oldest_allowed)
        # print("=" * 60)
        # count += 1
        # if count == 4:
        #     exit()
        # Check if the IP address has made 100 requests within the 2-minute interval
        # if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD:
        #     minReq[ip_address] = REQUESTS_THRESHOLD
        if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and result[ip_address]["count"] == 0:
            result[ip_address]["count"] = REQUESTS_THRESHOLD
        # print(len(ip_requests[ip_address]))
        # print(result[ip_address]["count"])
        # print(result[ip_address]["count"] != 0)
        # print("="*50)
        if len(ip_requests[ip_address]) > result[ip_address]["count"] and result[ip_address]["count"] != 0:
            result[ip_address]["count"] += 1
            result[ip_address]["timestamp"] = ip_requests[ip_address][0]

            # Print the IP address and the time of the first request
            # print(first_requests)
            # exit()
        # if len(ip_requests[ip_address]) >= REQUESTS_THRESHOLD:
        #     print(f'IP address {ip_address} made {len(ip_requests[ip_address])} requests between '
        #           f'{oldest_allowed} and {timestamp}, starting at {first_requests[ip_address]}')
# print(result)
for key, val in result.items():
    if val["timestamp"]:
        print(f"{key}: " + str(val["count"]) + ", " +
              str(val["timestamp"].timestamp()))
# print(datetime.datetime.now().timestamp())
endTime = datetime.datetime.now()
diff = endTime - startTime
print(diff.total_seconds())
# print(result["127.0.0.1"]["timestamp"])
