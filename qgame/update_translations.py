import codecs

new_translations = """

msgid "Manage Users"
msgstr "વપરાશકર્તાઓનું સંચાલન"

msgid "Back to Dashboard"
msgstr "ડેશબોર્ડ પર પાછા ફરો"

msgid "ID"
msgstr "ID"

msgid "Username"
msgstr "યુઝરનેમ"

msgid "Name"
msgstr "નામ"

msgid "Role"
msgstr "ભૂમિકા"

msgid "Points"
msgstr "પોઈન્ટ્સ"

msgid "Actions"
msgstr "ક્રિયાઓ"

msgid "Delete"
msgstr "ડિલીટ"
"""

with codecs.open('translations/gu/LC_MESSAGES/messages.po', 'a', 'utf-8') as f:
    f.write(new_translations)
