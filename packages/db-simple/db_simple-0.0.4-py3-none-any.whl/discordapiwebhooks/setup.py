from setuptools import setup

setup(
    name='discordapiwebhooks',
    version='1.0.1',
    description='discordapiwebhooks is a Python module that allows you to easily send webhooks to Discord. It supports sending text, images, and files to a Discord server.

To start using the module, you need to install it in your Python environment using the pip package manager:

Copy code
pip install discordapiwebhooks
After installing the module, you can start using it in your code. For example, to send a message to Discord, you can use the following code:

python
Copy code
from discordapiwebhooks import DiscordWebhooks

# Create a DiscordWebhooks instance with the webhook URL
webhook = DiscordWebhooks("https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvw")

# Send a message
webhook.post(content="Hello, world!")
This will send the message "Hello, world!" to the specified webhook.

You can also send images and files to a Discord server. To send an image, use the add_file method:

python
Copy code
from discordapiwebhooks import DiscordWebhooks

# Create a DiscordWebhooks instance with the webhook URL
webhook = DiscordWebhooks("https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvw")

# Add an image
webhook.add_file(file_path="path/to/image.jpg", filename="image.jpg")

# Send a message
webhook.post(content="Check out this cool image!")
This will send the message "Check out this cool image!" to the specified webhook and attach the image.jpg image from the specified path.

I hope this helps you understand how to use the discordapiwebhooks module.',
    author='NouName',
    author_email='duaneskalanak@gmail.com',
    packages=['discordapiwebhooks'],
)
