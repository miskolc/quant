# coding = utf-8
# ae_h - 2018/6/4
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from jinja2 import Environment, PackageLoader
from quant.config import default_config



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def mail_nofity():
    from_addr = 'Q_catcher@sohu.com'
    from_pwd = 'aedotpy000'
    to_addr = 'aemaeth@foxmail.com'
    smtp_server = 'smtp.sohu.com'

    msg = MIMEText(template_loader('hello'), 'html', 'utf-8')
    msg['From'] = _format_addr(u'Q_catcher<%s>' % from_addr)
    msg['To'] = _format_addr(u'Trader <%s>' % to_addr)
    msg['Subject'] = Header(u'Test Mail', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, from_pwd)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def template_loader(name):
    env = Environment(loader=PackageLoader(default_config.TEMPLATE_DIR, 'utf-8'))

    mail_template = env.get_template('mail_template.html')

    return mail_template.render(name=name)


if __name__ == '__main__':
    mail_nofity()