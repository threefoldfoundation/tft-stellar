import toml

from jumpscale.loader import j


class unlock_service:
    def uninstall(self):
        """Called when package is deleted"""
        j.sals.nginx.main.websites.default_443.locations.delete("unlock_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("unlock_root_proxy")
