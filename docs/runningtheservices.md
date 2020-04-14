# Commands to start the services in the background

Assuming the packages are already installed:

```python
j.servers.threebot.start(background=True)
gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
gedis.actors.package_manager.package_start('threefoldfoundation.unlock_service')
gedis.actors.package_manager.package_start('threefoldfoundation.conversion_service')
gedis.actors.package_manager.package_start('threefoldfoundation.transactionfunding_service')
gedis.actors.package_manager.package_start('threefoldfoundation.activation_service')
gedis.actors.package_manager.package_start('threefoldfoundation.stellar_faucet')
```
