# ae_h - 2018/6/5
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from jinja2 import Environment, PackageLoader

from quant.config import default_config


def _format_addr(args):
    name, addr = parseaddr(args)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def mail_notify_sender(mail_to, mail_subject, mail_templates):
    msg = MIMEText(mail_templates, 'html', 'utf-8')
    msg['From'] = _format_addr(u'Q_catcher<%s>' % default_config.MAIL_FROM_ADDR)
    msg['To'] = _format_addr(u'Trader <%s>' % mail_to)
    msg['Subject'] = Header(mail_subject, 'utf-8').encode()

    server = smtplib.SMTP(default_config.MAIL_SMTP, 25)
    server.set_debuglevel(1)
    server.login(default_config.MAIL_FROM_ADDR, default_config.MAIL_FROM_PWD)
    server.sendmail(default_config.MAIL_FROM_ADDR, [mail_to], msg.as_string())
    server.quit()


def mail_content_render(*args, **kwargs):
    env = Environment(loader=PackageLoader(default_config.ROOT_DIR, 'templates'))
    template = env.get_template('mail_template.html')
    template.render(k=w)
