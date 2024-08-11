import pika
from model_contacts import Contact

def simulate_email_send(email):
    print(f"Sending email to {email}...")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.message_sent:
        simulate_email_send(contact.email)
        contact.message_sent = True
        contact.save()
        print(f"Email sent to {contact.fullname} at {contact.email}.")
    else:
        print(f"Contact {contact_id} not found or already sent.")


# Настройка подключения к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

channel.basic_consume(
    queue='email_queue',
    on_message_callback=callback,
    auto_ack=True
)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

