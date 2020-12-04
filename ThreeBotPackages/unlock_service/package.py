import toml

from jumpscale.loader import j


class unlock_service:
    def install(self, **kwargs):

        if "default_443" in j.sals.nginx.main.websites.list_all():
            location_actors_443 = j.sals.nginx.main.websites.default_443.locations.get(name="unlock_service_actors")
            location_actors_443.is_auth = False
            location_actors_443.is_admin = False
            location_actors_443.save()

        if "default_80" in j.sals.nginx.main.websites.list_all(): 
            location_actors_80 = j.sals.nginx.main.websites.default_80.locations.get(name="unlock_service_actors")
            location_actors_80.is_auth = False
            location_actors_80.is_admin = False
            location_actors_80.save()

        # Configure server domain (passed as kwargs if not, will be the default domain in package.toml)
        if "domain" in kwargs:
            domain = kwargs.get("domain")
            toml_config = toml.load(j.sals.fs.join_paths(j.sals.fs.dirname(__file__), "package.toml"))
            package_name = toml_config["name"]
            server_name = toml_config["servers"][0]["name"]

            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_443").domain = domain
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_443").configure()
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_80").domain = domain
            j.sals.nginx.main.websites.get(f"{package_name}_{server_name}_80").configure()

        if "default_443" in j.sals.nginx.main.websites.list_all():
            j.sals.nginx.main.websites.default_443.configure()
        
        if "default_80" in j.sals.nginx.main.websites.list_all(): 
            j.sals.nginx.main.websites.default_80.configure()

    def start(self, **kwargs):
        self.install(**kwargs)

    def uninstall(self):
        """Called when package is deleted
        """
        j.sals.nginx.main.websites.default_443.locations.delete("unlock_root_proxy")
        j.sals.nginx.main.websites.default_80.locations.delete("unlock_root_proxy")
