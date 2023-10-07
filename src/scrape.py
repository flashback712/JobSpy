from dao.mongoDAO import MongoDBHelper
from tools.tools import get_location_list, get_title_list
import os
from jobspy import scrape_jobs
import pandas as pd
from jobspy.jobs import JobPost

# for write date to mongo
mongo_helper = MongoDBHelper()

# locations, titles for search
locations = get_location_list()
titles = get_title_list()


# write jobs to mongo
def write_jobs_to_mongo(job_list, mongo: MongoDBHelper):
    # print(job_list)
    mongo.insert_all(data_list=job_list)


for location in locations:
    for title in titles:
        try:
            jobs: pd.DataFrame = scrape_jobs(
                site_name=["indeed"],
                search_term=title,
                location=location,
                results_wanted=15,
                country_indeed='USA',
                # offset=25  # start jobs from an offset (use if search failed and want to continue)
                proxy="http://crawler-gost-proxy.jobright-internal.com:8083"  # gcp
                # proxy="http://crawler-gost-proxy.jobright-internal.com:8080" # aws
            )
            jobs_list = jobs.to_dict(orient='records')
            for job in jobs_list:
                if 'date_posted' in job:
                    job['date_posted'] = job['date_posted'].strftime('%Y-%m-%d %H:%M:%S')
            write_jobs_to_mongo(jobs_list, mongo_helper)
        except Exception as e:
            print(f'Error when process: [{location}][{title}]')
            print(e)
            continue
        print(f'[{location}][{title}]: {jobs.shape[0]} rows append.')
