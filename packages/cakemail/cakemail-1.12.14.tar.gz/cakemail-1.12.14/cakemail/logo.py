from cakemail_openapi import LogoApi
from cakemail.wrapper import WrappedApi


class Logo(WrappedApi):
    delete_default: LogoApi.delete_default_logo
    upload_default: LogoApi.upload_default_logo

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'delete_default': 'delete_default_logo',
                'upload_default': 'upload_default_logo',
            }
        )
