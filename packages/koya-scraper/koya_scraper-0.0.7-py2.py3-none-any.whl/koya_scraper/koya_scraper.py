import os
import datetime
import sys
import boto3
import pandas as pd

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# from koya_aws import config_aws_env, create_bucket
from koya_utilities import send_email_to

import socket
import platform
import psutil
import subprocess
import sqlalchemy
import json
import awswrangler as wr

def get_engine(host='koya-internal.cr4gqvnvc2y8.us-east-1.rds.amazonaws.com', port='3306', db_user=None, db_password=None):
    
    if db_user is None or db_password is None:
        db_user = os.getenv('KOYA_DB_SCRAPER_LOGS_USER')
        db_password = os.getenv('KOYA_DB_SCRAPER_LOGS_PASSWORD')
    return sqlalchemy.create_engine(f'mysql+pymysql://{db_user}:{db_password}@{host}')

def get_executor_info():
    hostname = socket.gethostname()
    system = platform.platform()
    processor = platform.processor()
    cpu_count = psutil.cpu_count()
    memory_total = round(psutil.virtual_memory().total/(1024*1024*1024))
    if os.name == 'nt':
        cpu_info = subprocess.check_output('wmic cpu list /format:list', shell=True).decode()
        cpu_dict = {i.split('=')[0]:i.split('=')[1] for i in cpu_info.split('\r\r\n') if i!=''}
    elif os.name=='posix':
        cpu_dict = {'Name':'skip'}
    else:
        cpu_info = subprocess.check_output('lscpu', shell=True).decode()
        cpu_dict = [i.replace('  ','').strip() for i in cpu_info.split('\n')]
        cpu_dict = {i.split(':')[0]:i.split(':')[1] for i in cpu_dict if ':' in i}
        cpu_dict['Name'] = cpu_dict['Model Name'] # "Changing" key name
    
    exec_dict = cpu_dict.copy()
    exec_dict.update({
        'hostname': hostname
        ,'system': system
        ,'processor': processor
        ,'cpu_count': cpu_count
        ,'memory_total': memory_total
    })

    return exec_dict

def save_crawler_info_to_db(crawler,spider,s3_uri,engine,context):
    crawler_stats = crawler.stats.get_stats()
    exec_info = get_executor_info()

    start_time = crawler_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    finish_time = crawler_stats['finish_time'].strftime('%Y-%m-%d %H:%M:%S')
    time_lapsed = crawler_stats['elapsed_time_seconds']
    author = os.getenv('KOYA_DB_SCRAPER_LOGS_USER')
    system_details = {k:v for k,v in exec_info.items() if k=='hostname' or k=='system' or k=='processor' or k=='cpu_count' or k=='memory_total' or k=='Name'}

    try:
        website = spider.start_urls[0]
    except:
        website = spider.allowed_domains[0] if spider.allowed_domains else None
    
    try:
        crawler_name = spider.name 
    except:
        print("Crawler Name parameter doesn't exist")
        crawler_name = None

    execution_details = {k:v for k,v in crawler_stats.items() if k!='start_time' and k!='finish_time' and k!='elapsed_time_seconds' and k!='item_scraped_count'}
    num_items = [crawler_stats['item_scraped_count'] if 'item_scraped_count' in crawler_stats else None][0]
    #crawler_version = None #TODO: how to implement? git tag versioning?
    storage_path = s3_uri
    status = 'OK'

    query = f"""
        INSERT INTO koya_internal.scraper_executions (start_time, finish_time, time_lapsed, author, system_details, website, crawler_name, execution_details, num_items, storage_path, context, status)
        VALUES ('{start_time}', '{finish_time}', {time_lapsed}, '{author}', '{json.dumps(system_details)}', '{website}', '{crawler_name}', '{json.dumps(execution_details, indent=4, sort_keys=True, default=str)}', {num_items}, '{storage_path}', '{context}', '{status}')
    """
    with engine.connect() as conn:
        conn.execute(query)

    print('Execution logs written to DB')

def save_crawler_info_to_db_on_error(crawler,spider,s3_uri,engine,context,error_message):
    crawler_stats = crawler.stats.get_stats()
    exec_info = get_executor_info()
    error_message =error_message.replace("'",'"')

    start_time = crawler_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    finish_time = crawler_stats['finish_time'].strftime('%Y-%m-%d %H:%M:%S')
    time_lapsed = crawler_stats['elapsed_time_seconds']
    author = os.getenv('KOYA_DB_SCRAPER_LOGS_USER')
    system_details = {k:v for k,v in exec_info.items() if k=='hostname' or k=='system' or k=='processor' or k=='cpu_count' or k=='memory_total' or k=='Name'}

    try:
        website = spider.start_urls[0]
    except:
        print("Website parameter doesn't exist")
        website = None
    try:
        crawler_name = spider.name
    except:
        print("Crawler Name parameter doesn't exist")
        crawler_name = None

    execution_details = {k:v for k,v in crawler_stats.items() if k!='start_time' and k!='finish_time' and k!='elapsed_time_seconds' and k!='item_scraped_count'}
    num_items = [crawler_stats['item_scraped_count'] if 'item_scraped_count' in crawler_stats else None][0]
    #crawler_version = None #TODO: how to implement? git tag versioning?
    storage_path = s3_uri
    status = 'NOK'            
    query = f"""
        INSERT INTO koya_internal.scraper_executions (start_time, finish_time, time_lapsed, author, system_details, website, crawler_name, execution_details, num_items, storage_path, context, status, error_message)
        VALUES ('{start_time}', '{finish_time}', {time_lapsed}, '{author}', '{json.dumps(system_details)}', '{website}', '{crawler_name}', '{json.dumps(execution_details, indent=4, sort_keys=True, default=str)}', {num_items}, '{storage_path}', '{context}', '{status}', '{error_message}')
    """
    with engine.connect() as conn:
            conn.execute(query)

    print('Error - Execution logs written to DB')

def get_system_path(profile_name,scrape_project_name,client_project_name,stage,verbose):
    if profile_name is None:
        profile_name = os.getenv('AWS_PROFILE_NAME')
    
    package = scrape_project_name.lower()
    today = datetime.datetime.now().strftime('%m-%d-%Y')
    filename = f'{package}_{today}.csv'
    
    cwd = os.getcwd()
    root = cwd[:cwd.find('/Koya/')]

    if verbose:
        print('root:',root)

    root_path = root+'/Koya/'+client_project_name+'/scrape/'


    if verbose:
        print('root_path:',root_path)

    module_path = os.path.join(root_path, scrape_project_name, scrape_project_name, 'spiders')
    
    if verbose:
        print('module_path:',module_path)  

    sys.path.append(module_path)

    name = f"{scrape_project_name}spider"

    if verbose:
        print('name:',name) 

    spider = getattr(__import__(package, fromlist=[name]), name)
    
    #get local path
    data_save_path = os.path.join(root, client_project_name, 'pipeline','1-ingestion','data')

    
    scrapy_profile = os.getenv('AWS_PROFILE_NAME')
    session = boto3.Session(profile_name=scrapy_profile)
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    scrapy_access_key = current_credentials.access_key
    scrapy_secret_key = current_credentials.secret_key
    bucket = client_project_name
    key = f'{stage}/ingestion/data/{filename}'
    
        
    # Local storage file
    f = os.path.join(data_save_path, filename)
    s = get_project_settings()
    s['LOG_LEVEL'] = 'INFO'
        
    if key is None or bucket is None:
        e='key or bucket are missing'
        raise ValueError(e)

    s3_uri = f'S3://{bucket}/{key}'

    s['AWS_ACCESS_KEY_ID'] = scrapy_access_key
    s['AWS_SECRET_ACCESS_KEY'] = scrapy_secret_key
    s['FEEDS'] =  {
        f'{s3_uri}': {
            'format': 'csv'
        }
    }

    scrapy_storage_settings = s

    return scrapy_storage_settings,spider,filename,s3_uri


def run_spider(stage = 'development'
               ,client_project_name = 'koya-boom-and-bucket'
               ,scrape_project_name = 'Cat'
               ,context='aws'
               ,return_data=True
               ,profile_name=None
               ,save_execution_logs=True
               ,send_email=True
               ,email_to='andre@getkoya.ai'
               ,verbose=False):

    ##Get the spider definitions
    try:
    
        scrapy_storage_settings,spider,filename,s3_uri = get_system_path(profile_name,scrape_project_name,client_project_name,stage,verbose)
        
        process = CrawlerProcess(scrapy_storage_settings)
        crawler = process.create_crawler(spider)
        d=process.crawl(crawler)

        # TODO: Even when the spider fails, the function returns "finished" status. We would have to capture/parser the exception from the crawler_stats in order to define errors. 
        # Is there are better way?
        # What are the possible/most common spider exceptions? So we can parse (search for the key in the key:value)

    except Exception as e:
        print(str(e))
        if send_email:
            send_email_to(body=f'error on scraper for \n client_project_name: {client_project_name} \n scrape_project_name: {scrape_project_name} \n error: {str(e)}'
                          , project_name=scrape_project_name
                          , subject=f'error on scraper for client_project_name {client_project_name} and scrape_project_name {scrape_project_name}'
                          , email_to=email_to)

        return 1

    #start the spider process
    try:
        process.start()

        #if it runs well

        print('scraper completed')

        if save_execution_logs:
            engine = get_engine()
            save_crawler_info_to_db(crawler,spider,s3_uri,engine,context)

        if send_email:
            send_email_to(body=f'scraper completed for \n client_project_name: {client_project_name} \n scrape_project_name: {scrape_project_name}'
                          , project_name=scrape_project_name
                          , subject=f'scraper completed for \n client_project_name: {client_project_name} \n scrape_project_name: {scrape_project_name}'
                          , email_to=email_to)
    #if it did not run well
    except Exception as e:
        error_message=str(e)
        print(error_message)
        
        if save_execution_logs:
            engine = get_engine()
            save_crawler_info_to_db_on_error(crawler,spider,s3_uri,engine,context,error_message)

        if send_email:
            send_email_to(body=f'error on scraper for \n client_project_name: {client_project_name} \n scrape_project_name: {scrape_project_name} \n error: {str(e)}'
                          , project_name=scrape_project_name
                          , subject=f'error on scraper for client_project_name {client_project_name} and scrape_project_name {scrape_project_name}'
                          , email_to=email_to)

        return 1


    if return_data:
        try:

            file_path = f"s3://{client_project_name}/{stage}/ingestion/data/"+filename
            print(f"reading: {file_path}")
            data = wr.s3.read_csv(path=file_path)
            return data
        except Exception as e:
            print(str(e))
            if send_email:
                send_email_to(body=f'error on scraper for \n client_project_name: {client_project_name} \n scrape_project_name: {scrape_project_name} \n error: {str(e)}'
                              , project_name=scrape_project_name
                              , subject=f'error on scraper for client_project_name {client_project_name} and scrape_project_name {scrape_project_name}'
                              , email_to=email_to)


    return 0
