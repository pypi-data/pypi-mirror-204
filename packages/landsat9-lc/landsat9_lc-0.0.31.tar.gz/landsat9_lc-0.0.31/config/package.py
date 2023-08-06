from pydantic import BaseSettings


class PackageConfig(BaseSettings):
    name: str = 'landsat_9_lc'
    version: str = '0.0.2'


package_config = PackageConfig()
