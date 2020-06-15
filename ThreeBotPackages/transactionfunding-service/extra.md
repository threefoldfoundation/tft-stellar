# Some info that might be useful

## change the number of slaves after installation

Before starting the threebot:

```python
p=j.tools.threebot_packages.threefoldfoundation__transactionfunding_service
p.install_kwargs={"slaves":2}
p.save()
```
