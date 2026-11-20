from config.settings.env import env
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = env("ARVAN_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = env("ARVAN_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = env("ARVAN_BUCKET_NAME")

AWS_S3_ENDPOINT_URL = env("ARVAN_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = env("ARVAN_REGION", default="ir-thr-at1")

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True