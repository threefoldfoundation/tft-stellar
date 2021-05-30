## Install the signing software

To install a fresh copy of the singing software to partake and complete the multi signature process at the end of the month to create and sign the farmed TFT's to farmers, you need to have 2 things to start the installation
- A cosign private key  
- Installed docker on you operating system of choice.

For help with installing the Docker software suite on your operating system of choice, please refer to the docker documentation [here](https://www.docker.com/products/docker-desktop)

Per operating system:
- for Macos: https://hub.docker.com/editions/community/docker-ce-desktop-mac
- for Windows: https://hub.docker.com/editions/community/docker-ce-desktop-windows
- for linux:  see you distribution to find how to install docker.

Once installed you should be able to do the following test in a terminal / command shell and get the (long) output of the docker command.
```
johndoe@Johns-MacBook-Pro-6 github % docker
```
This should give you a lot of outout describing what options are available for the `docker` command.

## 1. download and store the docker ubuntu image

To download and store the docker ubuntu image:
```
docker run -ti ubuntu
```

Output should look like:
```
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
Digest: sha256:adf73ca014822ad8237623d388cedf4d5346aa72c270c5acc01431cc93e18e2d
Status: Downloaded newer image for ubuntu:latest
root@a6c169a3ac2f:/#
```
And if you look carefully, the command prompt changed to `root@a6c169a3ac2f:/#` which means you are no inside the running ubuntu container.

To do the following needed steps, it's easiest to copy & paste the following steps into the ubuntu container.  You can select the complete block and press `enter`
```
apt update
apt upgrade -y
apt-get install -y git python3-venv python3-pip redis-server tmux nginx wget -y
pip3 install poetry
python3 -m pip install js-sdk
```
Copy paste the above into the ubuntu container and wait. This will take a while and a lot of output will be generated to your screen.  Have a coffee and wait it out.

```
cd
mkdir code
cd code
mkdir github
cd github
mkdir threefoldtech
cd threefoldtech
wget https://github.com/threefoldtech/js-sdk/tarball/master ; tar xvf ./master ; rm master
poetry update
poetry install
poetry shell
```
It will produce again a lot of output - another coffee or do some work.

The end result is all updates software, and in the ubuntu container you now have a fully configures poetry shell which is what you need to start `jsng`.

So type ```jsng``` and see something liek this:
```
  • Installing minio (4.0.21)
  • Installing netaddr (0.7.20)
  • Installing protobuf (3.17.1)
  • Installing pycountry (19.8.18)
  • Installing pygithub (1.54.1)
  • Installing pypng (0.0.20)
  • Installing pyqrcode (1.2.1)
  • Installing python-digitalocean (1.16.0)
  • Installing python-taiga (1.0.0)
  • Installing requests-unixsocket (0.2.0)
  • Installing sendgrid (6.7.0)
  • Installing stellar-sdk (2.4.1)
root@51b1e37e5510:~/code/github/threefoldtech/threefoldtech-js-sdk-e44e950# jsng
JS-NG>





 [F4] Emacs  1/1 [F3] History [F6] Paste mode                                                                                                                  [F2] Menu - CPython 3.8.5
 ```

Now we're ready to rock. Last item is to install you private key.  To do so - we need type in two command in the `jsng` shell.

First one:
```
j.clients.stellar.new('TFCosigningwallet', secret='<<insert your private key - starting with a capital S')
```
Response should look like:
```
Stellar(
  instance_name='TFCosigningwallet',
  network=<Network.STD: 'STD'>,
  address='<<your stella signing wallet address',
  secret='<<your private key>>'
)

JS-NG>
```
Success!  you now just need to save the private in in the `jsng` environment.  This is one more command:
```
j.clients.stellar.TFCosigningwallet.save()
```
All done, you can now exit.
```
exit()
```




