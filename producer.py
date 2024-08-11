import pika
import faker
from model_contacts import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')


fake = faker.Faker()
num_contacts = 10

for i in range(num_contacts):
    fullname = fake.name()
    email = fake.email()

    contact = Contact(fullname=fullname, email=email)
    contact.save()

    # Отправка идентификатора контакта в очередь RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=str(contact.id)
    )
    print(f"Contact {fullname} with email {email} added and ID sent to queue.")

connection.close()
