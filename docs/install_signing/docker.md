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
johndoe@badaboom github % docker
```
This should give you a lot of output describing what options are available for the `docker` command.

## 1. Download and update the docker ubuntu image

To download and store the docker ubuntu image:
```
docker run -v /$HOME:/mnt/my_home -ti ubuntu
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

To do the following needed steps, it's easiest to copy & paste the following steps into the ubuntu container.  copy paste them one by one and press `enter`

```bash
apt update
```

```bash
apt upgrade -y
```

```bash
apt-get install -y git python3-venv python3-pip redis-server tmux nginx wget -y
```

## 2. Install the required software for the signing SDK

```bash
pip3 install poetry
```

```bash
python3 -m pip install js-sdk
```

Copy paste all the lines above into the ubuntu container and press `enter`. This will take a while and a lot of output will be generated to your screen.  Have a coffee and wait it out.  When this is done - repeat with all the lines in the blocks below:
```bash
cd
mkdir code
cd code
mkdir github
cd github
mkdir threefoldtech
cd threefoldtech
```

```bash
wget https://github.com/threefoldtech/js-sdk/tarball/master ; tar xvf ./master ; rm master
cd three*
```

```bash
poetry update
poetry install
poetry shell
```
It will produce again a lot of output - another coffee or do some work.

The end result is all updates software, and in the ubuntu container you now have a fully configures poetry shell which is what you need to start `jsng`.

So type ```jsng``` and see something like this:
```
root@51b1e37e5510:~/code/github/threefoldtech/threefoldtech-js-sdk-e44e950# jsng
JS-NG>





 [F4] Emacs  1/1 [F3] History [F6] Paste mode                                                                                                                  [F2] Menu - CPython 3.8.5
 ```

## 3. Install the private key in the `jsngz` container
Now we're ready to rock. Last item is to install you private key.  To do so - we need type in two command in the `jsng` shell.

First one:
```
j.clients.stellar.new('TFCosigningwallet', secret='<<insert your private key - starting with a capital S>>')
```
Response should look like:
```
Stellar(
  instance_name='TFCosigningwallet',
  network=<Network.STD: 'STD'>,
  address='<<your stella signing wallet address>>',
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

## 4. Get the signing script and previous signers output.

To get the signing script please do this:
```
wget  https://raw.githubusercontent.com/threefoldfoundation/tft-stellar/development_install_minting/docs/install_signing/sign.py
chmod 755 ./sign.py
```

And to get the previous signers output please go to the issue and copy the link to the file of the previous signer: ![](img/copy_link.png)

With that link, comlpete the following command in the ubuntu container:
```
wget <<insert copied link>>
```
you should now have that file in the base directory of the `js-sdk` repo.   To sign all we need to do is:

## 5. Sign the TFT payouts with your private key
```
./sign.py <<name_of_downloaded_file_from_previous_signer.txt>> <<my_name_outputfile.txt>>
```

A process should start (and take a couple of hours to complete) that looks like this:
```
JS-NG> exit()
root@acc50e7f1bda:~/code/github/threefoldtech/threefoldtech-js-sdk-e44e950# ./sign.py payouts_signed_by_ahmed.txt new_out.txt
Signing 1386.1497888 TFT:GBOVQKJYHXRR3DX6NOX2RRYFRCUMSADGDESTDNBDS6CDVLGVESRTAC47 to <MuxedAccount [account_id=GAMT37U3JASMVGI5GR4TD7HV7ECOUUY7I4A7NZPOVNJKBY27ET7NQFQ2, account_id_id=None]> with memo 000cd192858680a001f70cdbbadde487322a58bfc27804afc050e13e272f9336 and sequence number 121828310719140709
Signing 9656.2832274 
.......
```
## 6. Upload the output to the Github issue to the next singer to use.

Depending of the month there will be a dedicated issue to handle the multi-signature sequence.  When you are done - please upload the resulting file to a comment in github.

To do so copy the output file (result) from you signing the transactions to your laptop:

```
cp ./<<output_file_name.txt>> /mnt/my_home
```

For the record, when you exit the container it does not store any of the actions that you have done in / on the container.  So for the next minting period you have to go through the whole procedure again.

We can however preserve the correct status of the container but then you have to be able to "maintain" that container and makde sure you do updates and upgrades that will happen in the 30 day period between singing activities yourself.  At this point we belief it's better to not store the state in you laptop and buidl the container everytime from scratch.  Let me (@weynandkuijpers) know if you feel that you can maintain the container in the appropriate way.


Now you can exit the docker container:
```
exit
```

```
exit
```
first `exit` exits the poetry shell, the second `exit` exits the container.

Now you should find the file you created in you `homedirectory`.  For Macos this is here in the finder:
![](img/homedir.png)

You can simply drag and drop the file to a the Github issue comment.


