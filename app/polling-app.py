from app.worker.service.hosts_polling_service import run_hosts_polling
from config import HOSTS_POLLING_CONFIG

if __name__ == '__main__':
    run_hosts_polling(HOSTS_POLLING_CONFIG)
