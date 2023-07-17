import pika
import random
from faker import Faker
from model import connect, Contact


ids = []


def generate_and_save(number_of_contacts):
    fake = Faker()

    for i in range(number_of_contacts):
        contact = Contact(fullname=fake.name(),
                          email=fake.email(),
                          phone=str(random.randint(380000000000, 380999999999)),
                          preferred=random.choice(['sms', 'email']))
        contact.save()
        ids.append(str(contact.id))


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email')
    channel.queue_declare(queue='sms')

    def sender(param):
        channel.basic_publish(exchange='', routing_key=param, body=i.encode())

    for i in ids:
        con = Contact.objects(id=i)[0].preferred
        if con == 'email':
            sender('email')
        elif con == 'sms':
            sender('sms')
        print(f" [x] Sent '{i}'")

    connection.close()


if __name__ == '__main__':
    generate_and_save(10)
    main()
