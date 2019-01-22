from prox.libs import login_lib
from prox.libs import utils

def get_auth():
    try:
        prox = login_lib.load_dumped_session()
    except Exception as e:
        print(e)
        exit()
    else:
        return prox

def get_vm_detail(node, vm_id):
    prox = get_auth()
    vm_detail = prox.getVirtualIndex(node, vm_id)
    return vm_detail['data']

def get_vm_status(node, vm_id):
    prox = get_auth()
    vm_status = prox.getVirtualStatus(node, vm_id)
    return vm_status['data']
