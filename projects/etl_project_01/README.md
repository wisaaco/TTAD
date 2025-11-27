# Price simulator platform

This platform simulates current daily variation in the price of several products through an exposed HTTP port. 
Every 10 seconds it generates updated JSON data. 

This is an example:

```json
{  
    "products": {
        "Seitan":{"coin":"dollar","price":4.45,"quantity":"100g"},
        "Tempe":{"coin":"euro","price":3.14,"quantity":"350g"},
        "Tofu":{"coin":"euro","price":10.33,"quantity":"300g"}
    },
    "time":124,
    "timestamp":"2025-11-27T08:06:34.087651"
}
```
This project uses Docker Compose to run two containers:
1. **price-simulator**: Generates product prices every 10 seconds with independent trends
2. **student-container**: Container where you'll deploy your script and configure crontab

## Starting the Platform

Note: Implicit steps: clone the project, go to the folder, ...

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Check if containers are running:
```bash
docker ps
```

3. Test the price simulator:
```bash
curl http://localhost:8088
```

Or with Python:

```python
import requests

response = requests.get("http://localhost:8088")
print(response.status_code)
print(response.json())
```

## Directory Structure

- `data/`: Shared volume where CSV files will be stored
- `scripts/`: Place your Python scripts here (they'll be available in the container at `/app/scripts`)



## Activity

1. Design a Python script that fetches the data and stores it in an incremental CSV file. Define and normalize the new columns and values.

2. Deploy this script in the container and configure it to run automatically using crontab

### Modify crontab inside the container (Recommended)

2.1. Access the student container:
```bash
docker exec -it student-container bash
```

2.2 Edit the crontab:
```bash
crontab -e
```

2.3. Add your cron job. The format is: minute hour day month weekday command. For example, to run every minute:

```
* * * * * /usr/bin/python3 /app/scripts/fetch_prices.py >> /var/log/cron.log 2>&1
```

2.4. Verify crontab is set:
```bash
crontab -l
```
2.5. Exit the container
```bash
exit
```

2.6. Check the CSV data:


## Example Script Location

Place your script in `scripts/fetch_prices.py`. It will be accessible in the container at `/app/scripts/fetch_prices.py`.

**Important**: When accessing the price simulator from inside the student-container, use:
- `http://price-simulator:8088` (container name)

When testing from your host machine, use:
- `http://localhost:8088`

An example script is provided in `scripts/example_fetch_prices.py` as a starting point.

## Accessing the Shared Data Volume

The `data/` directory is shared between both containers. Files written by your script in `/app/data/` inside the container will appear in the `data/` directory on your host machine.

## Stopping the Platform

```bash
docker-compose down
```

## Troubleshooting

- Check container logs: `docker-compose logs student-container`
- Check price simulator logs: `docker-compose logs price-simulator`
- Verify cron is running: `docker exec student-container ps aux | grep cron`
