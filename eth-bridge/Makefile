ldflags = '-w -s -extldflags "-static"'

build:
	GOOS=linux go build -ldflags $(ldflags)

docker: build
	cp -r eth-bridge genesis docker/ && cd docker && docker build -t eth-bridge:latest .
