from prox.clis.base import Base
from prox.libs import node_lib
from tabulate import tabulate
from prox.libs import utils
import os


class Node(Base): 
    """
        usage:
            node task [-N NODE] [-i VMID]
            node dns [-N NODE]
            node status [-N NODE] [-a ACTION]
            node log
            node rrd [-a ACTION]
            node beans          

        Commands :
            task                              Task Command
            dns                               list DNS
            status                            Node Status
            log                               Node Log Data
            rrd
            beans

        Options:
        -h --help                             Print usage
        -N node --node=NODE                   Get Node
        -i vmid --vmid=VMID                   Get VM
        -a action --action=ACTION             Get Status
        -p path --path=PATH                   Get PATH
    """
    def execute(self):
        node = self.args["--node"]
        if not node:
            utils.log_info("Using Default Node : pve")
            node = "pve"

        if self.args['task']:
            task_data = node_lib.get_finish_task(node)
            if not task_data:
                utils.log_err("Data not found")
                exit()
            
            total_task = task_data['total']
            utils.log_info("Total: "+str(total_task))
            task_list = list()
            vmid = self.args['--vmid']
            if vmid:
                for i in task_data['data']:
                    if i['id'] == vmid:
                        id = None
                        if i['id'] == "":
                            id = "master"
                        else:
                            id = i['id']

                        data = {
                            'id': id,
                            'type': i['type'],
                            'pstart': i['pstart'],
                            'pid': i['pid'], 
                            'status': i['status']
                        }
                        task_list.append(data)
                headers = {
                    'pstart': 'PStart',
                    'id': 'ID', 
                    'type': 'Type',
                    'pid': "PID", 
                    'status': 'Status'
                }
                print(tabulate(task_list, headers=headers, tablefmt='grid'))
                exit()

            for i in task_data['data']:
                id = None
                if i['id'] == "":
                    id = "master"
                else:
                    id = i['id']

                data = {
                    'id': id,
                    'type': i['type'],
                    'pstart': i['pstart'],
                    'pid': i['pid'], 
                    'status': i['status']
                }
                task_list.append(data)
            headers = {
                'pstart': 'PStart',
                'id': 'ID', 
                'type': 'Type',
                'pid': "PID", 
                'status': 'Status'
            }
            print(tabulate(task_list, headers=headers, tablefmt='grid'))
            exit()
        
        if self.args['dns']:
            data_dns = node_lib.get_node_dns(node)
            if not data_dns:
                utils.log_err("Data Not Found")
                exit()
            list_dns = list()
            list_dns.append(data_dns)
            print(tabulate(list_dns, headers="keys" ,tablefmt='grid'))
            exit()

        if self.args['status']:
            data_status = node_lib.get_node_status(node)
            if not data_status:
                utils.log_err("Data Not Found")
                exit()
            action = self.args['--action']
            if action:
                list_action = list()
                for i in data_status:
                    if i == action:
                        if type(data_status[i]) == dict:
                            list_action.append(data_status[i])
                        elif type(data_status[i]) == list:
                            for key in data_status[i]:
                                utils.log_info(key)
                        else:
                            utils.log_info(data_status[i])
                            exit()
                print(tabulate(list_action, headers="keys" ,tablefmt='grid'))
                exit()
            list_status = list()
            for i in data_status:
                list_status.append({
                    "Status": i
                })
            print(tabulate(list_status, headers="keys" ,tablefmt='grid'))
            exit()

        if self.args['log']:
            data = node_lib.get_node_syslog(node)
            list_log = list()
            for i in data:
                data_log = {
                    "row": i['n'],
                    "desc": i['t']
                }
                list_log.append(data_log)
            headers = {
                    "row": "No",
                    "desc": "Description"
                }
            print(tabulate(list_log, headers=headers ,tablefmt='grid'))
            exit()

        if self.args['rrd']:
            data = self.args['--action']
            if data:
                rrd_data = node_lib.get_node_rrd_data(node)
                print(rrd_data)
                exit()
            data = node_lib.get_node_rrd(node)
            print("Testing")
            exit()

        if self.args['beans']:
            data = node_lib.get_node_beans(node)
            print("Testing")
            exit()


        
