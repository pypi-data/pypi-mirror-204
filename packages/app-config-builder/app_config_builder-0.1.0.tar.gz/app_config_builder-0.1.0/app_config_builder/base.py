# from typing import Any
#
# from pydantic.env_settings import BaseSettings
# from pydantic.fields import Field
#
# from .constants import AUTH_KEY, BASE_DIR, OTHER_KEY
#
#
# def file_settings(settings: BaseSettings) -> dict[str, Any]:
#     conf = dict(
#         auth_key='AUTH_KEY_config_file',
#         other_key='OTHER_KEY_config_file',
#
#     )
#     return conf
#
#
# class Settings(BaseSettings):
#     auth_key: str = Field(default=AUTH_KEY)
#     other_key: str = Field(default=OTHER_KEY)
#     base_dir: str = Field(BASE_DIR.as_posix())
#
#     class Config:
#         secrets_dir = BASE_DIR / 'secrets'
#         env_file = '.env'
#         # env_file = f'{BASE_DIR.as_posix()}/../.env'
#         # env_file = f'../.env'
#
#         # @classmethod
#         # def customise_sources(
#         #         cls,
#         #         init_settings,
#         #         env_settings,
#         #         file_secret_settings,
#         # ):
#         #
#         #     output_order = (
#         #         env_settings,
#         #         file_secret_settings,
#         #         init_settings,
#         #         file_settings,
#         #         # init_settings,
#         #     )
#         #
#         #     return output_order
#
#
# settings = Settings()
# # settings = Settings(auth_key='auth_key_from_init')
#
# # print(BASE_DIR.as_posix())
# # print(f'{BASE_DIR.as_posix()}/.env')
