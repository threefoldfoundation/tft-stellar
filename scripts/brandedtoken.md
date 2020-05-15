# Create branded tokens

Create a folder in `../config/brandedtokens` with  the token code as name.

Create a templatetellar.toml with the righ content:

```toml
name="Projectname "
desc="Project description"
image="https://www.threefold.io/assets/3fold_icon.png"
```

Execute `brandedtoken.py tokencode --activator_secret=<secret>` for testnet.

For production, execute `brandedtoken.py tokencode --network=public --activator_secret=<secret>`

Make sure to store the issuer secret safely.
