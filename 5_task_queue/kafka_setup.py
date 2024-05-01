from kafka import KafkaAdminClient
from kafka.admin.new_partitions import NewPartitions

NUM_PARTITIONS = 2

client = KafkaAdminClient(bootstrap_servers='localhost:29092')

rsp = client.create_partitions({
    'tasks': NewPartitions(NUM_PARTITIONS)
})

print(rsp)
