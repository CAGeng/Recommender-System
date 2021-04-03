import smtplib
from email.mime.text import MIMEText

#JHLOFFRUSSOVQRFT
#qq
#wyyqbrkfdfwgbeed

# 第三方 SMTP 服务
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "recommendersystem@163.com"  # 用户名
mail_pass = "JHLOFFRUSSOVQRFT"           # 授权密码

sender ='recommendersystem@163.com'    # 发件人邮箱

title = 'RecommenderSystem--邮箱身份验证'  # 邮件主题
     

def sendEmail(email, VerificationCode):
    receivers = []  # 接收邮件
    receivers.append(email)
    content = '您好，感谢您使用RecommenderSystem。您正在进行邮箱验证，本次请求的验证码为:\n' #内容 
    content = content + VerificationCode + "\n"

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)  # 发件人邮箱
    message['To'] = ",".join(receivers)     # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message['Subject'] = title     # 邮件主题
    
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("邮件发送成功")
        return 0
    except smtplib.SMTPException as e:
        print(e)     #错误信息
        return 1

if __name__ == '__main__':
    sendEmail('1256736926@qq.com','123132')  #调用实例化   进行发送邮件