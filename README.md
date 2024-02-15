Here is an example of how to call the CBRAIN API using Python.

It perfoms low level calls to the API, and is not meant to be used directly.

It mainly give example on how to use the API in order to move data from one storage to another, or
to download data from a storage.

You should have a config (config.json) file in the same directory as this script, with the following content:

```json
{
    {
    "base_url": "http://XXX.XXX.XXX.XXX:3000",
    "login": "login",
    "password": "password",
    "s3_dp_id": "your_s3_dataprovider_id",
    "uk_dp_id": "your_uk_dataprovider_id",
    "group_id": "user_group_id",
    "directory_basename": "directory_basename",
    "file_browse_path": "file_browse_path",
    "file_basename": "file_basename"
}
```

Numerotation in code corresponds to the numerotation in API-documentation.pdf
