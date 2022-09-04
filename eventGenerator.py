import uuid
import random
import time
from datetime import datetime, timedelta


action=[ "Break", "Rent", "Steel", "Return", "Customize", "Adjust"]
bikeVendor=["Merida","Gant","Silverback","Author"]
customer=["Jim","Tom","Alex","Lada","Jiri","Sasha"]

bikeId=dict()
for i in range(100):
    bikeId[i]=random.choice(bikeVendor)
#print (bikeId)     
#print (bikeId.keys())

def gen_random_event():
    evtBikeId=random.choice(range(10))
    evtBikeVendor=bikeId[evtBikeId]
    evtTimestamp=datetime.now()
    evtId=uuid.uuid4()
    evtAction=random.choice(action)
    evtCustomer=random.choice(customer)
    event=f"{evtTimestamp}  {evtId}  {evtAction}  {evtCustomer}  {evtBikeId}  {evtBikeVendor}"
    with open("/home/olga/learning/elastic/rent.txt", 'a') as file:
        # Write given line to the dummy file
        file.write(event + '\n')

while True:
    gen_random_event()
    time.sleep(1)
