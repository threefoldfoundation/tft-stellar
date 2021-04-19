ldflags = '-w -s -extldflags "-static"'

build:
	GOOS=linux go build -ldflags $(ldflags)

docker: build
	cp eth-bridge genesis.json docker/ && cd docker && docker build -t eth-bridge:latest .
