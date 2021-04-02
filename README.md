# RecipeMatcher

![Recipe](https://thumbs.gfycat.com/UnluckyLimitedLark-mobile.mp4)

------

## Installation Instruction

### 1. Install Docker and Python (if necessary)

#### 	1.1 Docker

​		Link: https://www.docker.com/get-started

#### 	1.2 Python

​		Link: https://www.python.org/downloads/

### 2. Obtain and run Elasticsearch Docker Image

```sh
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.2

docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.11.2
```

### 3. Clone the Repository

```sh
git clone https://github.com/apugachev/RecipeMatcher.git
```

### 4. Create virtual environment and install dependencies

```sh
python3 -m venv recipe-env
source recipe-env/bin/activate
cd recipematcher
pip3 install -r requirements.txt
```

### 5. Run application

```sh
python3 app.py
```

### 6. Go to http://127.0.0.1:5000/

------

## Data sources:

- https://www.allrecipes.com/
- https://eda.ru/