from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from src.config import TomcatLog, ApacheLog, MenuConfig, ExtendConfig, analyzeModeConfig, DosDetectionConfig
# ['Nmap scanning', 'Metasploit attack', 'DoS']


class Render:
    def __init__(self, fromDate, toDate, detectedAttackType, nmapScan, metasploitAttack, dosData):
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
            'dosAttack': dosData,
            'dosSignature': {
                    'minimumRequest': str(DosDetectionConfig.minimumRequest),
                    'duration': str(DosDetectionConfig.duration)  # minutes
            },
        }

        self.rendered = self.template.render(data=self.data)

    def outputReport(self):
        with open(analyzeModeConfig.reportFolder, 'w', encoding='utf-8') as f:
            f.write(self.rendered)
