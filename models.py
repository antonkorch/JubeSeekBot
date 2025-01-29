class MessageHistory:
    def __init__(self, user):
        """
        Initializes the MessageHistory with a user and an empty dictionary for messages.
        
        :param user: The identifier of the user.
        """
        self.user = user
        self.messages = [{"role": "system", "content": "You are a helpful assistant"},]

    def add_message(self, message):
        self.messages.append({"role": "user", "content": message})