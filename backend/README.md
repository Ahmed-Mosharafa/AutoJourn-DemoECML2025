# TextSummarizationLab21

Includes the code-base for the NLP Lab Course for Text Summarization SOSE2021

## API Documentation

### **[GET]** `/search`

#### Example:

##### Request:

```shell
curl http://127.0.0.1:8787/search?query="Football"  > data.json
```

### **[GET]** `/topics`

#### Example:

##### Request:

```bash
curl --header "Content-Type: application/json" --request POST --data "@data.json"  http://127.0.0.1:8787/topics?num_topics=10 > topics.json
```

### **[GET]** `/summarize`

#### Example:

##### Request:

```bash
curl --header "Content-Type: application/json" --request POST --data "@data.json" http://127.0.0.1:8787/summarize > summaries.json
```

## Installation:

- Create and run a Python virtualenv

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

- Install the app and its dependencies with pip. Inside the app root folder (the one containing `requirements.txt`, run the following command)

```
$ pip3 install -r requirements.txt
```

- Export the environment varialbes in the `.env` file.

```
$ set -a; source .env; set +a
```

- Run the gunicorn server:

```
$ gunicorn -w <number_of_worker_processes> -b <host_ip> -k gevent ratimator.app:app /
   --timeout <worker timeout in seconds> --keep-alive <keep request connection live time in seconds> /
   --access-logfile -

 // Example:
 gunicorn -w 4 -b localhost:8787 -k gevent app:app --timeout 1000 --keep-alive 1000 --access-logfile - --preload
```
