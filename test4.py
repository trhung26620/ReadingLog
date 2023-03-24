import datetime

REQUESTS_THRESHOLD = 5
INTERVAL_MINUTES = 1
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-03-23.txt'
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\localhost_access_log.2023-01-11.txt'
# filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\tomcatLog\testlog.txt'
filePath = r'F:\Work\Development\Freelance\ReadingLog\temp\opt\tomcat\logs\localhost_access_log.2023-03-24.txt'

# Define variables to keep track of requests
ip_requests = {}
# first_requests = {}
result = {}
# Define a helper function to parse the timestamp string


def parse_timestamp(timestamp_str):
    # return datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
    return datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')


count = 0
# Open the log file
with open(filePath, 'r') as file:
    # Iterate through each line in the log file
    for line in file:
        # Split the line into its components
        components = line.split(' ')

        # Extract the IP address and timestamp from the line
        ip_address = components[0]
        timestamp = parse_timestamp(
            # (components[3] + ' ' + components[4]).replace('[', '').replace(']', ''))
            (components[3]).replace('[', '').replace(']', ''))
        print(timestamp)
        # Check if the IP address has already been seen
        if ip_address not in ip_requests:
            ip_requests[ip_address] = []
            # first_requests[ip_address] = timestamp
            result[ip_address] = {"count": 0, "timestamp": None}

        # Add the request to the IP address's list of requests
        ip_requests[ip_address].append(timestamp)

        # Remove requests that are older than the 2-minute interval
        if result[ip_address]["count"] < REQUESTS_THRESHOLD:
            oldest_allowed = timestamp - \
                datetime.timedelta(minutes=INTERVAL_MINUTES)
            # print(oldest_allowed)
            ip_requests[ip_address] = [
                req for req in ip_requests[ip_address] if req >= oldest_allowed]
        else:
            result[ip_address]["count"] += 1

        if len(ip_requests[ip_address]) == REQUESTS_THRESHOLD and result[ip_address]["count"] == 0:
            result[ip_address]["count"] = REQUESTS_THRESHOLD
            result[ip_address]["timestamp"] = ip_requests[ip_address][0]

for key, val in result.items():
    if val["timestamp"]:
        print(f"{key}: " + str(val["count"]) + ", " +
              str(val["timestamp"]))
