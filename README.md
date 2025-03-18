## cloudconvert-python

This is the official Python SDK for the [CloudConvert](https://cloudconvert.com/api/v2) **API v2**.

[![Tests](https://github.com/cloudconvert/cloudconvert-python/actions/workflows/run-tests.yml/badge.svg)](https://github.com/cloudconvert/cloudconvert-python/actions/workflows/run-tests.yml)
![PyPI](https://img.shields.io/pypi/v/cloudconvert)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cloudconvert)

## Installation

```
 pip install cloudconvert
```

## Creating API Client

```py
 import cloudconvert

cloudconvert.configure(api_key='API_KEY', sandbox=False)
```

Or set the environment variable `CLOUDCONVERT_API_KEY` and use:

```py
 import cloudconvert

cloudconvert.default()
```

## Creating Jobs

```py
 import cloudconvert

cloudconvert.configure(api_key='API_KEY')

cloudconvert.Job.create(payload={
    "tasks": {
        'import-my-file': {
            'operation': 'import/url',
            'url': 'https://my-url'
        },
        'convert-my-file': {
            'operation': 'convert',
            'input': 'import-my-file',
            'output_format': 'pdf',
            'some_other_option': 'value'
        },
        'export-my-file': {
            'operation': 'export/url',
            'input': 'convert-my-file'
        }
    }
})

```

## Downloading Files

CloudConvert can generate public URLs for using `export/url` tasks. You can use these URLs to download output files.

```py
exported_url_task_id = "84e872fc-d823-4363-baab-eade2e05ee54"
res = cloudconvert.Task.wait(id=exported_url_task_id)  # Wait for job completion
file = res.get("result").get("files")[0]
res = cloudconvert.download(filename=file['filename'], url=file['url'])
print(res)
```

## Uploading Files

Uploads to CloudConvert are done via `import/upload` tasks (see
the [docs](https://cloudconvert.com/api/v2/import#import-upload-tasks)). This SDK offers a convenient upload method:

```py
job = cloudconvert.Job.create(payload={
    'tasks': {
        'upload-my-file': {
            'operation': 'import/upload'
        }
    }
})

upload_task_id = job['tasks'][0]['id']

upload_task = cloudconvert.Task.find(id=upload_task_id)
res = cloudconvert.Task.upload(file_name='path/to/sample.pdf', task=upload_task)

res = cloudconvert.Task.find(id=upload_task_id)
```

## Webhook Signing

The node SDK allows to verify webhook requests received from CloudConvert.

```py
payloadString = '...';  # The JSON string from the raw request body.
signature = '...';  # The value of the "CloudConvert-Signature" header.
signingSecret = '...';  # You can find it in your webhook settings.

isValid = cloudconvert.Webhook.verify(payloadString, signature, signingSecret);  # returns true or false
```

## Signed URLs

Signed URLs allow converting files on demand only using URL query parameters. The Python SDK allows to generate such
URLs. Therefore, you need to obtain a signed URL base and a signing secret on
the [CloudConvert Dashboard](https://cloudconvert.com/dashboard/api/v2/signed-urls).

```py
base = 'https://s.cloudconvert.com/...'  # You can find it in your signed URL settings.
signing_secret = '...'  # You can find it in your signed URL settings.
cache_key = 'cache-key'  # Allows caching of the result file for 24h

job = {
    "tasks": {
        "import-file": {
            "operation": "import/url",
            "url": "https://github.com/cloudconvert/cloudconvert-php/raw/master/tests/Integration/files/input.pdf"
        },
        "export-file": {
            "operation": "export/url",
            "input": "import-file"
        }
    }
}

url = cloudconvert.SignedUrl.sign(base, signing_secret, job, cache_key);  # returns the URL
```

## Unit Tests

```
python -m unittest discover -s tests/unit
 
```

## Integration Tests

```
python -m unittest discover -s tests/integration 

```

## Resources

* [API v2 Documentation](https://cloudconvert.com/api/v2)
* [CloudConvert Blog](https://cloudconvert.com/blog)
