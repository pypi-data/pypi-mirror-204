import base64
import json
from collections import ChainMap
from typing import Any, Type

from botocore.exceptions import ClientError

from aws_chain_secrets.caster import cast
from aws_chain_secrets.client import Client
from aws_chain_secrets.exceptions import SecretsManagerException


class Null:
    """
    class to represent null type
    """
    pass


null = Null()


class SecretsManager(Client):
    def __init__(
            self,
            region_name: str,
            *secret_names: str,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None
    ):
        """
        initial setup
        :param region_name: AWS region name
        :param secret_names: These are the secret names from which to read settings. The last name has priority.
        """
        self.secret_names = secret_names
        super().__init__(
            "secretsmanager",
            region_name,
            aws_access_key_id,
            aws_secret_access_key
        )
        self._secrets = {secret_name: {} for secret_name in secret_names}
        self._combined = ChainMap(*reversed(self._secrets.values()))

    def __call__(self, key, *, default: Any = null, casting_type: Type = str):
        return self.get(key, default=default, casting_type=casting_type)

    def __enter__(self):
        super().__enter__()
        self.fetch()
        return self

    def get(self, key, *, default: Any = null, casting_type: Type = str):
        """
        get secret value
        :param key: key value to search
        :param default: default value if key not exists in secrets
        :param casting_type: casting type to convert value
        :return: Any secret value specified by key
        """
        try:
            value = self._combined[key]
        except KeyError:
            if isinstance(default, Null):
                raise KeyError(f"{repr(key)} not found. Please check secret value in AWS Secrets Manager.")
            return default
        return cast(value, casting_type)

    def set(self, secret_name: str, key, value):
        """
        set a `key: value` to the specified secret
        :param secret_name: secret_name of AWS Secrets Manager
        :param key: key of map
        :param value: value of map
        """
        self._secrets[secret_name][key] = value

    def keys(self):
        return self._combined.keys()

    def values(self):
        return self._combined.values()

    def items(self):
        return self._combined.items()

    def fetch(self):
        """
        get secrets from AWS and update
        """
        for secret_name in self.secret_names:
            self._secrets[secret_name].clear()
            self._secrets[secret_name].update(self._get_secrets(secret_name))

    def update(self, secret_name: str):
        """
        update specified secrets from local to AWS
        :param secret_name: secret name of AWS Secrets Manager
        """
        self._client.update_secret(SecretId=secret_name, SecretString=json.dumps(self._secrets[secret_name]))

    def _get_secrets(self, secret_name: str) -> dict:
        """
        get secrets from AWS
        :param secret_name: secret name of AWS Secrets Manager
        """
        try:
            response = self._client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise SecretsManagerException.from_code(e.response['Error']['Code'])
        else:
            if 'SecretString' in response:
                return json.loads(response['SecretString'])
            return json.loads(base64.b64decode(response['SecretBinary']))


