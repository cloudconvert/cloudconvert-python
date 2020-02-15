## cloudconvert-python

This is the official Python SDK v2 for the [CloudConvert](https://cloudconvert.com/api/v2) _API v2_. 
For API v1, please use [v1 branch](https://github.com/cloudconvert/cloudconvert-python/tree/v1) of this repository.


[![Build Status](https://travis-ci.com/cloudconvert/cloudconvert-python.svg?branch=master)](https://travis-ci.com/cloudconvert/cloudconvert-python)
## Installation

```
 pip install cloudconvert
```

## Creating API Client

```
  import cloudconvert
 
  cloudconvert.configure(api_key = 'API_KEY', sandbox = False)
```

Or set the environment variable `CLOUDCONVERT_API_KEY` and use:

```
  import cloudconvert
 
  cloudconvert.default()
```

## Creating Jobs

```js
 import cloudconvert

 cloudconvert.configure(api_key = 'API_KEY')

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

```js
exported_url_task_id = "84e872fc-d823-4363-baab-eade2e05ee54"
res = cloudconvert.Task.wait(id=exported_url_task_id) # Wait for job completion
file = res.get("result").get("files")[0]
res = cloudconvert.download(filename=file['filename'], url=file['url'])
print(res)
```

## Uploading Files

Uploads to CloudConvert are done via `import/upload` tasks (see the [docs](https://cloudconvert.com/api/v2/import#import-upload-tasks)). This SDK offers a convenient upload method:

```js
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

```js
payloadString = '...'; # The JSON string from the raw request body.
signature = '...'; # The value of the "CloudConvert-Signature" header.
signingSecret = '...'; # You can find it in your webhook settings.

isValid = cloudconvert.Webhook.verify(payloadString, signature, signingSecret); # returns true or false
```

## Unit Tests

```
# Run Task tests
$ python tests/unit/testTask.py

# Run Job tests
$ python tests/unit/testJob.py

# Run Webhook tests
$ python tests/unit/testWebhookSignature.py
 
```


## Integration Tests
```
# Run Integration test for task
$ python tests/integration/testTasks.py 

# Run Integration test for Job
$ python tests/integration/testJobs.py 

```
       

## Resources

* [API v2 Documentation](https://cloudconvert.com/api/v2)
* [CloudConvert Blog](https://cloudconvert.com/blog)
