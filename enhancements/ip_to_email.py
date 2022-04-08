import yaml
from elastalert.enhancements import BaseEnhancement
from elastalert import util


class IP2EmailSearchLink(BaseEnhancement):
    # The enhancement is run against every match
    # The match is passed to the process function where it can be modified in any way
    # ElastAlert 2 will do this for each enhancement linked to a rule
    def process(self, match):
        with open("/opt/elastalert/config.yaml") as config:
            conf = yaml.safe_load(config)
            parsed_conf = util.build_es_conn_config(conf)
            es_client = util.elasticsearch_client(parsed_conf)

            if "ip" in match["source"]:
                ip = match["source"]["ip"]
                users = self.search_ip(ip, es_client)
                match["users"] = ",".join(users)
            else:
                util.elastalert_logger.info(
                    "source.ip not present in results! Skipping."
                )
            es_client.close()

    def search_ip(self, ip, es):
        index = "_all"
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"exists": {"field": "user.email"}},
                        {
                            "match": {
                                "source.ip": ip
                            },
                        },
                    ]
                }
            }
        }

        results = es.search(index=index, body=query)
        users = []

        for hit in results["hits"]["hits"]:
            user = hit["_source"]["user"]["email"]
            if user not in users:
                users.append(user)
        return users
