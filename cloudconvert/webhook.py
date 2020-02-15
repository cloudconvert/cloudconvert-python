import hmac
import hashlib


class Webhook():
    """Webhook class for verifying the webhook signature

    Usage::
        >>> Webhook.verify(payload_string, signature, signature_secret)     # return True or False
    """

    @classmethod
    def verify(cls, payload_string, signature, signature_secret):
        generate_signature = hmac.new(signature_secret.encode('utf-8'), payload_string.encode('utf-8'),
                                      hashlib.sha256).hexdigest()
        return signature == generate_signature
