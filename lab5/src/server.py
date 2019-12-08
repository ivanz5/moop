import db
import pika
import json

db = db.DB()

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue='moop')


def get_all():
    return db.get_authors_and_books()


def save_all(data):
    db.save_authors_and_books(data)


def on_request(ch, method, props, body):
    print(" [x] Received %r" % body)
    body = json.loads(body)
    # get_all method
    if body.get('get_all', False) is True:
        print('get_all')
        response = get_all()
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    # save_all method, no response
    elif body.get('save_all', False) is True:
        data = body.get('data', None)
        if data is not None:
            save_all(data)
            if props.reply_to is None:
                props.reply_to = ''
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body='{}')
            ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='moop', on_message_callback=on_request)
    channel.start_consuming()
