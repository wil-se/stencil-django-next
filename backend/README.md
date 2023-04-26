# How to run

```
cd here
docker build -t backend-casino .
docker run -p 8000:8000 -t backend-casino
```

or

```
chmod +x run.sh # only the first time
./run.sh
```

or run those two commands here
```
git pull
docker compose build
docker compose up
```

## Create Superuser

locate the backend-cryptocasino-django CONTAINER ID
```
docker ps
```

execute the bash shell inside the container
```
docker exec -ti CONTAINER_ID bash
```

create superuser
```
python3 manage.py createsuperuser
```

# NUKE CLEAN YOUR DOCKER ENVIRONMENT 
```
docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q) && docker image prune -a && docker network prune && docker volume prune
```


## Auth Endpoints
- authentication/login
- authentication/login
- authentication/register
- authentication/verify
- authentication/user
- authentication/nonce_sign_request
- authentication/nonce_sign_verify