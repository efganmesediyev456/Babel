import os

import polib
from flask_paginate import Pagination, get_page_args


class Pofile(object):

    path='app'
    filename='messages'
    babel_config_file_name='babel.cfg'

    def __init__(self, locale="az"):
        self.locale = locale
        self.po = polib.pofile(
            os.path.join(os.getcwd(), r'{}\translations\{}\LC_MESSAGES\{}.po'.format(self.path,self.locale, self.filename)))


    def getPO(self):
        return self.po

    def poFilterValues(self, filter=None):
        self.po = [e for e in self.po if not e.obsolete]
        po_entries = []
        for entry in self.po:
            if (filter):
                if filter in entry.msgid or filter in entry.msgstr:
                    po_entries.append({'msgid': entry.msgid, 'msgstr': entry.msgstr})
            else:
                po_entries.append({'msgid': entry.msgid, 'msgstr': entry.msgstr})
        return po_entries

    @staticmethod
    def get_users(offset=0, per_page=10, po_entries=None):
        return po_entries[offset: offset + per_page]

    def filterPagination(self, filter=None):
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        po_entries = self.poFilterValues(filter)
        total = len(po_entries)
        pagination_entries = self.get_users(offset=offset, per_page=per_page, po_entries=po_entries)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4', per_page_parameter='per_page', per_page_name='per_page')
        return {'page': page, 'per_page': per_page, 'pagination': pagination, 'pagination_entries': pagination_entries}
    def poUpdate(self, msgid, msgstr):
        for num, a in enumerate(msgid):
            entry = self.po.find(a)
            if entry:
                entry.msgstr = msgstr[num]
                if 'fuzzy' in entry.flags:
                    entry.flags.remove('fuzzy')
        self.po.save(os.path.join(os.getcwd(),r'{}\translations\{}\LC_MESSAGES\{}.po'.format(self.path, self.locale, self.filename)))
        os.system('pybabel compile -d {}/translations'.format(self.path))
        return True
    def poScan(self):
        os.system('pybabel extract -F {} -o {}.pot .'.format(self.babel_config_file_name, self.filename))
        os.system('pybabel update -i {}.pot -d {}/translations'.format(self.filename, self.path))
        os.system('pybabel compile -d src/translations')
        return True
    def poCreate(self, language):
        os.system('pybabel init -i {}.pot -d {}\\translations -l {}'.format(self.filename, self.path,language))
        return True