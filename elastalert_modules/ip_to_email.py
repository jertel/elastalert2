from elastalert.enhancements import BaseEnhancement
from elastalert import util

class IP2EmailSearchLink(BaseEnhancement):
    # The enhancement is run against every match
    # The match is passed to the process function where it can be modified in any way
    # ElastAlert 2 will do this for each enhancement linked to a rule
    def process(self, match):
        if 'ip' in match["source"]:
            ip = match["source"]["ip"]
            util.elastalert_logger.info(f"Retrieving email relating to {ip}")
            match['ip_to_email_link'] = f"https://watchtower.ravelin.net/app/discover#/?_g=(filters:!(),query:(language:kuery,query:''),refreshInterval:(pause:!t,value:0),time:(from:now-1h%2Fh,to:now))&_a=(columns:!(),filters:!(),index:aec5cdb0-94d0-11ec-bd6a-3d68c61c44d9,interval:auto,query:(language:kuery,query:'source.ip:%22{ip}%22'),sort:!(!('@timestamp',desc)))"
        else:
            util.elastalert_logger.info("source.ip not present in results! Skipping.")
