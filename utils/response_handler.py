class ResponseHandler(object):
    @staticmethod
    def get_result(message, key=None):
        if isinstance(message, list):
            message = message[0]
        return {'detail': message}
