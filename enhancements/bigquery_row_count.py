import yaml
from elastalert.enhancements import BaseEnhancement, DropMatchException
from elastalert import util

class BigQueryRowCount(BaseEnhancement):
    
    def process(self, match):
        if self.check_match(match):
            with open("/opt/elastalert/config.yaml") as config:
                conf = yaml.safe_load(config)
                parsed_conf = util.build_es_conn_config(conf)
                es_client = util.elasticsearch_client(parsed_conf)

            tmp_table_id = match["gcp"]["audit"]["bigquery"]["tmp_table_id"]
            row_count = self.search_row_count(tmp_table_id, es_client)
            es_client.close()
            match["row_count"] = row_count

            # Filter out all exports that are smaller than 1000 rows 
            if int(row_count) < 1000:
                raise DropMatchException()

            
    def check_match(self, match):
        """Check that the document has all expected fields before proceeding"""
        try:
            tmp_table_id = match["gcp"]["audit"]["bigquery"]["tmp_table_id"]
            if tmp_table_id != "":
                return True
        except Exception as e:
            util.elastalert_logger.error(e)
            return False

    def search_row_count(self, table_id, es):
        index = "_all"
        # TODO: Return only one document
        query = {
            "query": {
                "bool": {
                    "must": [
                        { "match": { "gcp.audit.bigquery.tmp_table_id": table_id }},
                        { "exists": { "field": "gcp.audit.bigquery.output_row_count" }}
                    ]
                }
            }
        }
        results = es.search(index=index, body=query)

        return results["hits"]["hits"][0]["gcp"]["audit"]["bigquery"]["output_row_count"]
