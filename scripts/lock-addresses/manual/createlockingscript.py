#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
import click


@click.command()
@click.option("--outputfile", type=click.File("w"), default="createlockingscript.sh")
@click.argument("tfchainaddresses", type=str, required=False, nargs=-1)
def createlockingscript(outputfile, tfchainaddresses):
    outputfile.write("#!/bin/bash\n")
    for address in tfchainaddresses:
        outputfile.write(f'deauthtx="$(tfchainc wallet authcoin authaddresses --deauth {address})"\n')
        outputfile.write(f'signeddeauthtx="$(tfchainc wallet sign $deauthtx)"\n')
        outputfile.write('echo "tfchainc wallet send transaction \\"\\$(tfchainc wallet sign $signeddeauthtx)\\""\n')


if __name__ == "__main__":
    createlockingscript()
