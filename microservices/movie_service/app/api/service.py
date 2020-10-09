import os
import httpx


url = os.environ.get('CAST_SERVICE_HOST_URL')

def is_cast_present(cast_id: int):
    r = httpx.get(f'{url}{cast_id}')
    return r.status_code == 200