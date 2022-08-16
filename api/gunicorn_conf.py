from multiprocessing import cpu_count

''' 
	Update paths to match with your file system
'''

# Socket Path
bind = 'unix:/home/deploy/tts/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Timeout
keepalive = 120
timeout = 7200

# Logging Options
loglevel = 'debug'
accesslog = '/home/deploy/tts/logs/access_log.log'
errorlog = '/home/deploy/tts/logs/error_log.log'
capture_output = True
