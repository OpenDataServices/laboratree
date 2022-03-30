# LaboraTree crawlers

Crawlers ([memorious](https://github.com/alephdata/memorious)) for planning application documents on local authority websites.

Seeded by planning application URLs from the [EPDS]() database.

## Setup

Create `config.env` from `config.env.tmpl` and fill in the variables.

To start, run: `docker-compose up -d`

To access the memorious CLI, run: `docker-compose run --rm shell`

Inside the shell, you can:

* See crawlers: `memorious list`
* Run a crawler: `memorious run my_crawler`
* More: `memorious --help`

Run a crawler in the background:

```
docker-compose run -d --rm shell memorious run my_crawler
```

Check if it's running:

```
docker-compose run --rm shell memorious status my_crawler
```

## Development

Crawlers are in `config/`. Common helper functions or operations are in `src/padocs/__init__.py` and crawler-specific helper functions or operations are in `src/padocs/{my_crawler}.py`.

Crawlers generally operate as follows:

* Get a list of URLs directly from the ODSC EPDS database. Each crawler is configured with `area_name`, `start_date` and `end_date` to constrain the URLs.
* Fetch each URL, parse the HTML to find documents associated with the planning application.
* Download each document, extract additional metadata if possible (eg. title, file name).
* Send each document to the Laboratree aleph instance (for text extraction).
* Store the aleph document id alongside other metadata in a local database.
* When the crawler has finished running, insert all document metadata into the main EPDS database.

TODO: Text extraction with aleph is not instantaneous. There is a separate process to query the aleph API for each document; if text extraction has been completed, insert the extracted text into the EPDS database alongside the metadata.

### Poking around in the database

You can connect to the postgres database where the crawler results go through the datastore container:

````
(host) sudo docker-compose run datastore psql -h datastore -U datastore -d datastore
```

(The password is also datastore - configured in docker-compose.yml).