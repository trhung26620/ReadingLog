from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.config import TomcatLog, ApacheLog, analyzeModeConfig, DosDetectionConfig


class Render:
    def __init__(self, fromDate, toDate, detectedAttackType, nmapScan, metasploitAttack, dirbBruteforce, dosData, pathLog):
        self.env = Environment(loader=FileSystemLoader(
            "src\ReportTemplate"), autoescape=select_autoescape())
        self.template = self.env.get_template("report.html")
        self.data = {
            'filterDate': {
                'fromDate': fromDate,
                'toDate': toDate,
            },
            'pathLog': pathLog,
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
            'dirbBruteforce': {
                'signature': analyzeModeConfig.dirbDetectionSignature,
                'logDataTomcat': dirbBruteforce['logDataTomcat'],
                'logDataApache': dirbBruteforce['logDataApache']
            },
            'dosAttack': dosData,
            'dosSignature': {
                    'minimumRequest': str(DosDetectionConfig.minimumRequest),
                    'duration': str(DosDetectionConfig.duration)
            },
        }

        self.rendered = self.template.render(data=self.data)

    def outputReport(self):
        with open(analyzeModeConfig.reportFolder, 'w', encoding='utf-8') as f:
            f.write(self.rendered)
