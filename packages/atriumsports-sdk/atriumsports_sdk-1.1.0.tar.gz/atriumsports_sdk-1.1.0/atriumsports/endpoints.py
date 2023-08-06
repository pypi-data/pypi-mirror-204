""" A file defining all the endpoint addresses """


class ConfigurationException(Exception):
    """Exception to be raised when a configuration is invalid"""

    pass


def _get_endpoint(environment, endpoint_type):
    """return urls for the atriumsports environments"""

    # add some extra mapping
    fix_mapping = {
        "prod": "production",
        "uat": "nonprod",
        "dev": "sandpit",
        "test": "sandpit",
    }
    environment = fix_mapping.get(environment, environment)
    envs = {
        "auth": {
            "production": "https://token.prod.cloud.atriumsports.com/v1/oauth2/rest/token",
            "nonprod": "https://token.nonprod.cloud.atriumsports.com/v1/oauth2/rest/token",
            "sandpit": "https://token.sandpit.cloud.atriumsports.com/v1/oauth2/rest/token",
            "localhost": "http://localhost:XXXX",
        },
        "api": {
            "production": "https://api.dc.prod.cloud.atriumsports.com",
            "nonprod": "https://api.dc.nonprod.cloud.atriumsports.com",
            "sandpit": "https://api.dc.sandpit.cloud.atriumsports.com",
            "localhost": "http://localhost:XXXX",
        },
        "streamauth": {
            "production": "https://token.prod.cloud.atriumsports.com/v1/stream/XXXX/access",
            "nonprod": "https://token.nonprod.cloud.atriumsports.com/v1/stream/XXXX/access",
            "sandpit": "https://token.sandpit.cloud.atriumsports.com/v1/stream/XXXX/access",
            "localhost": "http://localhost:XXXX",
        },
    }
    return envs.get(endpoint_type, {}).get(environment)


def get_endpoint_url(environment, endpoint_type, version=None):
    endpoint_url = _get_endpoint(environment, endpoint_type)
    if not endpoint_url:
        raise ConfigurationException(f"No endpoint {endpoint_type} for environment {environment}")
    if version is not None:
        endpoint_url = f"{endpoint_url}/v{version}"
    return endpoint_url
