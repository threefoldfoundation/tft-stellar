# lock small list of addresses

execute the createlockingscript.py with the tfchaina addresses to unlock as parameters.

execute the generated `createunlockingscript.sh` and send the output to a cosigner to execute.

for example:

```sh
./createlockingscript.sh > cosignlocks.sh
```

and then send the `cosignlocks.sh` script to a valid cosigner to execute.
