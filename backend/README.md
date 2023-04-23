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