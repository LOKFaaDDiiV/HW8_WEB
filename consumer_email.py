import pika
import sys
from model import connect, Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    def callback(ch, method, properties, body):
        print(f" [x] Sending email to contact with id {body.decode()}")
        contact = Contact.objects(id=body.decode())
        contact.update(is_delivered=True)

    channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
