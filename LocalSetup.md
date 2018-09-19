## Local Setup

- Clone the repository: https://github.com/the-deep/DEEPL
- Have [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed.
- `cd` to the DEEPL project directory and run `docker-compose up`. This should download and prepare images and might take some time since this is the first time.
- The server should be running on port `8010`.
- We don't have any models right now. So, run the command `docker-compose exec web bash`. This will take you inside the server's container.
- Now create a classifier model by issuing command `./manage.py runscript create_classifier --model_version=1`. This will create a classifier model using the data from `https://docs.docker.com/compose/install/`.
- Although DEEPL is completely [api based](https://github.com/the-deep/DEEPL/blob/develop/APISpecifications.md), there is a simple frontend to get a brief idea of how things are. It is running at port `8010`.
