""" We have this runner till we use docker """

import uvicorn
import subprocess

from src.config import setting
from src.app import app


def run():
    if setting.SSL:
        uvicorn.run(
            app, 
            host=setting.APP_HOST ,
            port=setting.APP_PORT,
            ssl_certfile=setting.SSL_CERT,
            ssl_keyfile=setting.SSL_KEY,
        )
    else:
        uvicorn.run(
            app, 
            host=setting.APP_HOST ,
            port=setting.APP_PORT,
        )

def run_workers():
    workers = [
        "celery -A src.core.celery_app purge -f",
        "pkill -f celery -e",
        "screen -mdS send-email-otp-bt celery -A src.core.celery_app worker -Q send_email_otp_bt -n send_email_otp_bt@%h -f log/python/celery/send_email_otp_bt.log --concurrency=1 -l debug",
        "screen -mdS scrape-snap-cafe celery -A src.core.celery_app worker -Q scrape_snap_cafe -n scrape_snap_cafe@%h -f log/python/celery/scrape_snap_cafe.log --concurrency=1 --pool=solo -l debug",
    
    ]

    for cmd in workers:
        print(f"\nRUNNING WORKER COMMAND:\n{cmd}")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print("stdout:", res.stdout)
        print("stderr:", res.stderr)

        
if __name__ == "__main__":
    run_workers()
    run()
    