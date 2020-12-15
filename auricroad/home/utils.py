from wagtail.admin.mail import send_mail


#  taken from https://github.com/wagtail/wagtail/blob/master/wagtail/contrib/forms/models.py
def form_send_mail(form, to_address, from_address, subject):
    addresses = [x.strip() for x in to_address.split(",")]
    content = []
    for field in form:
        value = field.value()
        if isinstance(value, list):
            value = ", ".join(value)
        content.append("{}: {}".format(field.label, value))
    content = "\n".join(content)
    send_mail(subject, content, addresses, from_address)
