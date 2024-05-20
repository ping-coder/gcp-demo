from google.cloud import bigquery
import pprint

client = bigquery.Client()

job = client.get_job(job_id='bquxjob_2468cee6_18f52ce18c5')

pprint.pp(job.__dict__)