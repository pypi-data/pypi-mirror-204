# PyDillo

### Local

```
export PYTHONPATH=/path/to/pydillo:$PYTHONPATH
```

### Docker

0. Buid local **development** docker image

```
bash development.sh
```

1. Run **development** image with local source

```
sudo docker run \
  -it \
  --name pydillo --rm \
  -v /home/ermiry/Documents/Work/pydillo:/home/pydillo \
  itdillo/pydillo:development /bin/bash
```

2. Handle **pydillo** module

```
export PYTHONPATH=$pwd:$PYTHONPATH
```
