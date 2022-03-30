# Laboratree aleph

This contains config for an instance of aleph used for Laboratree.

nginx config is customsed (see `ui/`).

`pages/` contains customised home and about pages.

## Setup

```bash
docker-compose up --scale ingest-file=6 --scale convert-document=4 --scale worker=2
```

If you modify nginx config, you need to `docker-compose down` and back up again.

It can take a while for elasticsearch to kick in after a restart, give it a few minutes if things seem weird.

Enter a shell to do things like create users:

```bash
docker-compose run --rm shell /bin/bash
```

There is no email server set up, so users registering through the UI will not receive a confirmation. When you create users at the commandline, remember to inform them of their password, and grab their API key as well (though this is available through the UI).

```bash
aleph createuser --name="test" \
                 --password=test \
                 test@opendataservices.coop
```