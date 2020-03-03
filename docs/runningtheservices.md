# Commands to start the services in the background

```python
j.servers.threebot.local_start_3bot(background=True)
gedis = j.clients.gedis.get("pm", port=8901, package_name="zerobot.packagemanager")
JSX> gedis.actors.package_manager.package_start('threefoldfoundation.unlock_service')
JSX> gedis.actors.package_manager.package_start('threefoldfoundation.conversion_service')
JSX> gedis.actors.package_manager.package_start('threefoldfoundation.transactionfunding_service')
```
