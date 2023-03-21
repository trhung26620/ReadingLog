from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from src.config import TomcatLog, ApacheLog, MenuConfig, ExtendConfig, analyzeModeConfig
# ['Nmap scanning', 'Metasploit attack', 'DoS']


class Render:
    def __init__(self, fromDate, toDate, detectedAttackType, nmapScan, metasploitAttack):
        self.env = Environment(loader=FileSystemLoader(
            "src\ReportTemplate"), autoescape=select_autoescape())
        self.template = self.env.get_template("report.html")
        self.data = {
            'filterDate': {
                'fromDate': fromDate,
                'toDate': toDate,
            },
            'pathLog': {
                'tomcatPath': TomcatLog.folderPath,
                'apachePath': ApacheLog.folderPath,
            },
            'detectedAttackType': detectedAttackType,
            'nmapScan': {
                'signature': analyzeModeConfig.nmapDetectionSignature,
                'logDataTomcat': nmapScan['logDataTomcat'],
                'logDataApache': nmapScan['logDataApache']
            },
            'metasploitAttack': {
                'signature': analyzeModeConfig.metasploitDetectionSignature,
                'logDataTomcat': metasploitAttack['logDataTomcat'],
                'logDataApache': metasploitAttack['logDataApache']
            },
            'dosAttack':
                [
                    {
                        'time': '18/Feb/2023:22:41:22',
                        'ip': '192.168.10.1:1',
                        'numOfReq': '1000'
                    },
                    {
                        'time': '18/Feb/2023:22:41:22',
                        'ip': '192.168.10.1:1',
                        'numOfReq': '1000'
                    },
                    {
                        'time': '18/Feb/2023:22:41:22',
                        'ip': '192.168.10.1:1',
                        'numOfReq': '1000'
                    },            {
                        'time': '18/Feb/2023:22:41:22',
                        'ip': '192.168.10.1:1',
                        'numOfReq': '1000'
                    },            {
                        'time': '18/Feb/2023:22:41:22',
                        'ip': '192.168.10.1:1',
                        'numOfReq': '1000'
                    }
            ]
        }
        self.rendered = self.template.render(data=self.data)

    def outputReport(self):
        with open(analyzeModeConfig.reportFolder, 'w', encoding='utf-8') as f:
            f.write(self.rendered)


# 192.168.160.141 - - 08/Mar/2023:10:25:10 GET /nmaplowercheck1678245910 HTTP/1.1 404 775
# 192.168.160.141 - - 07/Mar/2023:12:50:48 GET /nmaplowercheck1678168248 HTTP/1.1 404 775
# 192.168.160.141 - - 07/Mar/2023:10:41:48 GET /nmaplowercheck1678160508 HTTP/1.1 404 775
# 192.168.160.141 - - 23/Feb/2023:16:14:53 GET /nmaplowercheck1677143693 HTTP/1.1 404 775
# 192.168.160.141 - - 23/Feb/2023:16:13:40 GET /nmaplowercheck1677143621 HTTP/1.1 404 775
# 192.168.160.141 - - 23/Feb/2023:16:04:09 GET /nmaplowercheck1677143049 HTTP/1.1 404 775
# 192.168.160.141 - - 23/Feb/2023:15:53:04 GET /nmaplowercheck1677142384 HTTP/1.1 404 775
# 192.168.160.141 - - 16/Feb/2023:23:40:51 GET /nmaplowercheck1676565651 HTTP/1.1 404 775
# 192.168.1.61 - - 16/Feb/2023:12:12:30 GET /nmaplowercheck1676524350 HTTP/1.1 404 775
# 192.168.101.93 - - 03/Feb/2023:12:51:41 GET /nmaplowercheck1675403501 HTTP/1.1 404 775
# 192.168.101.93 - - 11/Jan/2023:02:41:39 GET /nmaplowercheck1673379699 HTTP/1.1 404 775
# 192.168.101.11 - - 11/Jan/2023:01:27:12 GET /nmaplowercheck1673375232 HTTP/1.1 404 775
# 192.168.101.93 - - 27/Dec/2022:01:21:08 GET /nmaplowercheck1672129268 HTTP/1.1 404 775
# 192.168.160.134 - - 23/Dec/2022:05:50:52 GET /nmaplowercheck1671799853 HTTP/1.1 404 775
# 192.168.160.134 - - 22/Dec/2022:02:49:26 GET /nmaplowercheck1671702568 HTTP/1.1 404 775
# 10.0.0.69 - - 17/Sep/2021:01:33:54 GET /nmaplowercheck1631864034 HTTP/1.1 404 775
