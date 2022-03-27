import hmac
import hashlib
import json
import base64


class SignedUrl():
    """SignedUrl class for create signed URLs

    Usage::
        >>> SignedUrl.create(base, signing_secret, job, cache_key)     # return True or False
    """

    @classmethod
    def sign(cls, base, signing_secret, job, cache_key=None):
        jobJson = json.dumps(job)
        jobBase64 = base64.urlsafe_b64encode(bytes(jobJson, 'utf-8')).decode('utf-8')

        url = base + "?job=" + jobBase64

        if cache_key:
            url += "&cache_key=" + cache_key

        signature = hmac.new(signing_secret.encode('utf-8'), url.encode('utf-8'),
                             hashlib.sha256).hexdigest()

        url += "&s=" + signature

        return url
