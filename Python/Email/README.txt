Generate_Auto_Email.py -> Generates an email .docx message that will be attached to an automatically sent email.
The message will tell the receiver whether their registration was accepted, denied, or requires manual review based
on the response that was stored from the ML model.

Required installs:
docx


Send_Email.py -> Sends the generated email to the designated receiving address and deletes the email from temp storage after sent.
Required installs:
TBD

pip installs:
pip install docx