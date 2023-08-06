# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 10:10:43
# @Author  : Pane Li
# @File    : mail.py
"""
mail

"""
import datetime
import logging
import emails
import os


def pytest_send_report_mail(mail_to: str or list, mail_from: tuple or list, render: dict):
    """使用已配置好的邮件模板，发送邮件内容

    :param mail_to:  发送给谁
    :param mail_from: 元组($email, $password)
    :param render: 字典类型，需要将报告的内容传入 key值如下：
                             model：测试设备型号， 如VG710
                             fun: 测试功能
                             version: 测试的版本, 如 VG7-V209bfd4(test)-2023-03-31-14-52-02.bin
                             host: 测试主机， 10.5.24.107
                             report_url： 报告的链接
                             summary: 字典类型 从报告中的/allure-results/widgets/summary.json 获取内容

    :return:
    """
    html_file_path = os.path.join(os.path.dirname(__file__), 'pytest_email.html')
    from emails.template import JinjaTemplate as Te

    message = emails.html(html=Te(open(html_file_path, encoding='utf-8').read()),
                          subject=f'{render.get("model")}自动化测试',
                          mail_from=('映翰通网络测试', mail_from[0]))
    render.update(render.get('summary').get('statistic'))
    start = datetime.datetime.fromtimestamp(render.get('summary').get('time').get("start") / 1000.0).strftime(
        '%Y-%m-%d %H:%M:%S')
    stop = datetime.datetime.fromtimestamp(render.get('summary').get('time').get("stop") / 1000.0).strftime(
        '%Y-%m-%d %H:%M:%S')
    render.update({'start': start, 'stop': stop})
    render.pop('summary')
    r = message.send(mail_to, smtp={'host': 'smtp.exmail.qq.com', 'port': 465, 'user': mail_from[0], 'ssl': True,
                                    'password': mail_from[1]},
                     render=render)
    assert r.status_code == 250, 'send email failed'
    logging.info(f'send {mail_to} test result success!')


# def get_mail():
#     import imaplib
#     import email
#
#     # 连接到 IMAP 服务器
#     imap_server = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
#     imap_server.login('test@inhand.com.cn', 'ABc124')
#     imap_server.select('INBOX')
#
#     # 搜索邮件
#     status, email_ids = imap_server.uid('search', '(SENTSINCE "2023-04-14 11:00:00")')
#     print(status, email_ids)
#
#     # 循环处理每个邮件
#     for email_id in email_ids[0].split():
#         # 获取邮件内容
#         status, email_data = imap_server.fetch(email_id, '(RFC822)')
#         if email_data is not None:
#             raw_email = email_data[0][1]
#             email_message = email.message_from_bytes(raw_email)
#
#             # 获取邮件发送者和主题
#             sender = email_message['From']
#             subject = email_message['Subject']
#
#             # 对发送者和主题进行判断
#             if sender == 'trusted_sender@example.com' and 'important' in subject:
#                 # 处理邮件内容
#                 email_body = email_message.get_payload(decode=True).decode('utf-8')
#                 print('Received an important email from a trusted sender:')
#                 print('Sender:', sender)
#                 print('Subject:', subject)
#                 print('Body:', email_body)
#
#     # 关闭 IMAP 连接
#     imap_server.close()
#     imap_server.logout()


if __name__ == '__main__':
    # get_mail()
    pass