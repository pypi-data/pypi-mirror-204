from cakemail_openapi import ContactApi
from cakemail.wrapper import WrappedApi


class Contact(WrappedApi):
    add_interests_to: ContactApi.add_interests_to_contacts
    create: ContactApi.create_contact
    delete: ContactApi.delete_contact
    delete_contacts_export: ContactApi.delete_contacts_export
    download_contacts_export: ContactApi.download_contacts_export
    export_contacts: ContactApi.export_contacts
    get: ContactApi.get_contact
    get_contacts_export: ContactApi.get_contacts_export
    import_contacts: ContactApi.import_contacts
    list_contacts_exports: ContactApi.list_contacts_exports
    list: ContactApi.list_contacts_of_list
    list_from_segments: ContactApi.list_contacts_of_segment
    update: ContactApi.patch_contact
    remove_interests_from: ContactApi.remove_interests_from_contacts
    tag: ContactApi.tag_contact
    tag_multiple: ContactApi.tag_multiple_contacts
    unsubscribe: ContactApi.unsubscribe_contact
    untag: ContactApi.untag_contact
    untag_multiple: ContactApi.untag_multiple_contacts

    def __init__(self, superclass):
        super().__init__(
            superclass=superclass,
            namemap={
                'add_interests_to': 'add_interests_to_contacts',
                'create': 'create_contact',
                'delete': 'delete_contact',
                'delete_contacts_export': 'delete_contacts_export',
                'download_contacts_export': 'download_contacts_export',
                'export_contacts': 'export_contacts',
                'get': 'get_contact',
                'get_contacts_export': 'get_contacts_export',
                'import_contacts': 'import_contacts',
                'list_contacts_exports': 'list_contacts_exports',
                'list': 'list_contacts_of_list',
                'list_from_segments': 'list_contacts_of_segment',
                'update': 'patch_contact',
                'remove_interests_from': 'remove_interests_from_contacts',
                'tag': 'tag_contact',
                'tag_multiple': 'tag_multiple_contacts',
                'unsubscribe': 'unsubscribe_contact',
                'untag': 'untag_contact',
                'untag_multiple': 'untag_multiple_contacts',
            }
        )
