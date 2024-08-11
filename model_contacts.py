from mongoengine import Document, StringField, BooleanField, connect

try:
    connect(
        db='nataly-db',
        username='nataly-db',
        password='Y2FAaVc9S4eiADtz',
        host='mongodb+srv://cluster0.d0plr.mongodb.net',
        ssl=True
    )
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
