from cakemail_openapi import LogApi
from cakemail.wrapper import WrappedApi


class Log(WrappedApi):
    campaign_log_export_create: LogApi.campaign_log_export_create
    campaign_log_export_download: LogApi.campaign_log_export_download
    get_action: LogApi.get_action_logs
    get_campaign: LogApi.get_campaign_logs
    get_email: LogApi.get_email_logs
    get_list: LogApi.get_list_logs
    list_campaign_log_exports: LogApi.list_campaign_log_exports

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'campaign_log_export_create': 'campaign_log_export_create',
                'campaign_log_export_download': 'campaign_log_export_download',
                'get_action': 'get_action_logs',
                'get_campaign': 'get_campaign_logs',
                'get_email': 'get_email_logs',
                'get_list': 'get_list_logs',
                'list_campaign_log_exports': 'list_campaign_log_exports',
            }
        )
