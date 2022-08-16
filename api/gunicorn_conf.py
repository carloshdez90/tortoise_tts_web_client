from multiprocessing import cpu_count

''' 
	Update paths to match with your file system
'''

# Socket Path
bind = 'unix:/home/charlie/ws/tortoise_tts_web_client/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/charlie/ws/tortoise_tts_web_client/logs/access_log.log'
errorlog = '/home/charlie/ws/tortoise_tts_web_client/logs/error_log.log'
