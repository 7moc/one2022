
import pymysql
import random
import time,requests
from web3 import Web3


#判断是否使用代理
try:
    requests.get('https://etherscan.io/',timeout=5)
    proxies=None    
except:
    proxies = {"http": "socks5://127.0.0.1:10808", "https": "socks5://127.0.0.1:10808",}



# 创建数据库链接
conn = pymysql.connect(host='', port=3306, user='one2022', passwd='', db='one2022')
cur = conn.cursor()






proxies = {"http": "socks5://127.0.0.1:10808","https": "socks5://127.0.0.1:10808",}

eth_web3=Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/7906bef1634f4e24b1665f47b0e0ad6f",request_kwargs={"proxies":proxies}))

#创建地址
def ceate_address(create_amount):
    # 100个地址，保存地址和私钥excel
    address_list=[]
    for i in range(create_amount):
        address=eth_web3.eth.account.create()
        address_list.append([address.address,address.privateKey.hex()])

    # 将这些地址保存到数据库
    cur = conn.cursor()
    for i,q in enumerate(address_list):
        address=q[0]
        private_key=q[1]
        sql='insert into address (address,private_key) values("{}","{}")'.format(address,private_key)
        cur.execute(sql)
        conn.commit()
    print(i,address,private_key)




# 更新任务
def update_task_status(address,taskname,status):
    sql='update opt_task set "{}"="{}" where address="{}"'.format(taskname,status,address)
    cur.execute(sql)
    conn.commit()
    print("更新任务成功",taskname,status)


# 获取最新1个可用地址,要不要把qx_order_data的状态也占用
def get_address():
    # 获取地址
    sql='select address,private_key from address where id >(select min(id) from address where status=0)+{} and status=0 limit 1'.format(random.randint(0, 0)*5)     
    cur.execute(sql)
    result=cur.fetchall()
    address=result[0][0]
    private_key=result[0][1]
    # 更新地址状态
    sql='update address set status=1 where address="{}"'.format(address)
    cur.execute(sql)
    conn.commit()
    # 插入任务
    sql='insert into opt_task (address) values("{}")'.format(address)
    cur.execute(sql)
    conn.commit()
    # 返回地址和私钥
    return address,private_key

# address,private_key=get_address()
# print(address,private_key)


# 获取各个任务状态
def check_task_status(address):
    task_list=["Pika","Beethoven","Velodrome","Granary","Rubicon","Perp","Synapse","PoolTogether","mint_uniswap","mint_Synapse","mint_Stargate","mint_Perp","mint_Pika","mint_PoolTogether","PoolTogether_withdrawFrom"]
    for taskname in task_list:
        sql='select {} from opt_task where address="{}"'.format(taskname,address)
        cur.execute(sql)
        result=cur.fetchall()
        task_status=result[0][0]
        print(taskname,task_status)
        # if random.randint(0, 1)==1:
        #     update_task_status(address,taskname,1) 


# address="0xc27Fe83784039EcDA924Ee37d2a09f79B9435D47"
# check_task_status(address)

# 获取1个可用的 qx_signature，qx_order_data
def get_qx_signature():
    sql='select address,qx_signature,qx_order_data from opt_task where qx_status=1 limit 1'  
    cur.execute(sql)
    result=cur.fetchall()
    address=result[0][0]
    qx_signature=result[0][1]
    qx_order_data=result[0][2]
    # 更新qx_signature状态
    return address,qx_order_data,qx_signature
#
# print(get_qx_signature())
