1. Import CSV file as argument||give hardcoded location, clean it, Export it.
2. then dockerize the whole process.

## Build Docker Image
docker build -t my_image:1.0 . # (build a docker image, with tag, of the current directory based on Dockerfile)

## Run Docker Image as a container
docker run --name test_container my_image (Create and run a container)

## start a stopped container
docker start -ai test_container (start again a stopped container with output showing in the terminal)






## How to run (if not using hardcoded values)
{bash}
python main.py ../files/sampleData1.csv
