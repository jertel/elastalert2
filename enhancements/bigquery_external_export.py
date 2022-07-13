import re
from elastalert.enhancements import BaseEnhancement, DropMatchException
from elastalert import util

class BigQueryExternalExport(BaseEnhancement):

    def process(self, match):
        # fetching the bigquery SQL query 
        query = match["gcp"]["audit"]["bigquery"]["query"]
        if query == "":
            raise DropMatchException()

        # running a regex to get the word after `INSERT INTO` in the query which 
        # should hopefully indicate us where the data is being inserted into...
        m = re.search("INSERT INTO ([a-zA-Z0-9_\.]+)", query)
        if (m is None):
            raise DropMatchException()

        # doing some sanity checking on the returned data to avoid errors
        if (len(m.groups())) == 0:
            raise DropMatchException()
        destination = m.groups()[0]

        # ignore if project starts with ravelin-xxx
        if destination.startswith("ravelin-"):
            raise DropMatchException()

        # ignore if no dots are found, this means it's inserting data into a temp bigquery table
        if "." not in destination:
            raise DropMatchException()

