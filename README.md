# Factiva News Stream Client for Docker

Factiva Analytics Stream Client project template to be executed as part of a Docker container.

Getting a runing client is as easy as 1, 2, 3...

## 1. Customise the `app.main.py` file

Create your own logic to handle messages by creating/modifying the `message_handler` method in the `app/main.py` file.

There's a list of pre-built handlers that can be used:

* **[BigQueryHandler](https://devportal/bigqueryhandler/docs)**: Save each message to to a BigQuery table. As prerequisite, it is necessary to define the following `env` variables:

    | Var Name | Description |
    | ----- | ----- |
    | GOOGLE_APPLICATION_CREDENTIALS | A path to a JSON credentials file exported from Google Cloud, and having the right privilegdes to write records to the table. Example: `/app/svcacc.json` |
    | STREAMLOG_BQ_TABLENAME | A BQ full table path like `<project.dataset.table>` |

* **[JSONFileHander](https://devportal/jsonfile/docs)**: Save each mesasge to a JSONL file. This file contains one document per line. The following `env` variables are needed:
    | Var Name | Description |
    | ----- | ----- |
    | STREAM_FILES_DIR | A path to a folder that will contain the JSONL files, like `/articles` |

* **[MongoDBHandler](https://devportal/jsonfile/docs)**: Save each mesasge to a MongoDB collection. As prerequisite, it is necessary to define the following `env` variables:
    | Var Name | Description |
    | ----- | ----- |
    | MONGODB_CONNECTION_STRING | MongoDB url instance, like `mongodb://localhost:27017` |
    | MONGODB_DATABASE_NAME | Name of the database, like `factiva-stream` |
    | MONGODB_COLLECTION_NAME | Name of the collection (table) where the logs will be stored, like `streams` |

Also, we provide the following optional environment vars to allow you customize certain functions.

Enable proxy request

* **Proxy request**: Allow to perform http request through a proxy server:
    | Var Name | Description |
    | ----- | ----- |
    | HTTP_PROXY | The proxy URL to use for HTTP connections, like: `http://10.10.1.10:3128` |
    | HTTPS_PROXY | The proxy URL to use for HTTPS connections, like: `http://10.10.1.10:1080`. To use HTTP basic auth with your proxy, use the `http://user:password@host/` syntax, like `http://admin:admin123@10.10.1.10:1080`|
  
* **Files directories**: Path where the downloaded files and logs will be stored:

    | Var Name | Description |
    | ----- | ----- |
    | DOWNLOAD_FILES_DIR | Directory where the taxonomies, companies categories and job files will be stored, like `/files`. The `rootProject/downloads` is using by default|
    | LOG_FILES_DIR | Directory where the logs will be stored, like `/logs`. The `rootProject/logs` is using by default|

## 2. Run `docker build` to create the Docker Image

Review the `Dockerfile` before creating the image in order to enable/disable the relevant configurations according to the handlers or operations that will be used within the `main.py` script.

After the `Dockerfile` review is complete, just run the following command:

```bash
docker build -t fstream-client-python .
```

## 3. Start the Container instance

The container instance can be started either by running `docker run` or using `docker-compose`.

### Docker Run

This command starts the client in dettached mode.

```bash
docker run -d --name mystream-bqlogger \
 -v <host_logs_path>:/logs \
 -v <host_path_to>/service_account.json:/app/service_account.json \
 -e FACTIVA_USERKEY=<your user KEY> \
 -e FACTIVA_STREAMID=<your full stream ID> \
 -e <ENV_VAR_REQUIRED_BY_A_HANDLER>=<handler env var value> \
 fstream-client-python
```

### Docker-Compose

Use the following template as reference:

```yaml
version: '3.9'

services:
  listener:
    image: fstream-client-python
    volumes:
      - <host_logs_path>:/log
      - <host_path_to>/service_account.json:/app/service_account.json
    restart: always
    environment:
      FACTIVA_USERKEY: <your user KEY>
      FACTIVA_STREAMID: <your full stream ID>
      <ENV_VAR_REQUIRED_BY_A_HANDLER>: <handler env var value>

```
