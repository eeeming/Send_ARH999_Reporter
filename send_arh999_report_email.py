import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
# 你的邮箱密码或授权码
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
# 接收报告的邮箱地址
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
# SMTP 服务器地址和端口 (请根据你的邮箱服务商进行修改)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.163.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '465'))

# 简单检查是否所有必要变量都已设置
if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
    print("错误：邮件发送所需的环境变量未完全设置。请检查 SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL。")
    # 可以选择退出程序或采取其他错误处理
    exit(1) # 退出程序

def send_arh999_report_email():
    msg = MIMEMultipart('related')
    msg['Subject'] = 'ARH999 指数每日报告'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    # 1. 读取 HTML 表格内容
    try:
        with open("arh999_report_table.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("错误：未找到 arh999_report_table.html 文件。请确保已先生成。")
        return
    
    # 2. 读取图片文件（二进制模式）
    try:
        with open("arh999_report_chart.png", 'rb') as fp:
            img_data = fp.read()
    except FileNotFoundError:
        print("错误：未找到 arh999_report_chart.png 文件。请确保已先生成。")
        return

    # 3. 创建 HTML 部分并添加到邮件中
    full_html_body = f"""
    <html>
    <head></head>
    <body>
        <p>您好，</p>
        <p>这是您的ARH999指数每日报告，包含图表和近30天数据。</p>
        
        <h2>ARH999 指数趋势图</h2>
        <img src="cid:arh999_chart_cid" alt="ARH999 指数图表" style="max-width:100%;"> 
        <br><br>
        
        <h2>近30天 ARH999 指数数据</h2>
        {html_content}
        
        <p>祝您有美好的一天！</p>
        <p>您的自动化报告系统</p>
    </body>
    </html>
    """
    msg_html = MIMEText(full_html_body, 'html', 'utf-8')
    msg.attach(msg_html)

    # 4. 创建图片部分并添加到邮件中
    msg_image = MIMEImage(img_data, name="arh999_report_chart.png")
    msg_image.add_header('Content-ID', '<arh999_chart_cid>') # 确保与 HTML 中的 cid 匹配
    msg.attach(msg_image)

    # 5. 连接 SMTP 服务器并发送邮件
    try:
        # 使用 smtplib.SMTP_SSL 适用于 SSL 连接 (通常端口 465)
        # 如果使用 TLS (通常端口 587)，则使用 smtplib.SMTP() 后跟 server.starttls()
        
        # 推荐使用 SSL 连接，因为它在连接开始时就加密
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) 
        
        # 如果你的邮箱是 TLS (端口587)，请用下面的替换上面一行：
        # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # server.starttls() # 启动 TLS 加密

        server.login(SENDER_EMAIL, SENDER_PASSWORD) # 登录邮箱
        server.send_message(msg) # 发送邮件
        server.quit() # 关闭连接

        print("邮件发送成功！请检查收件箱。")
    except smtplib.SMTPAuthenticationError:
        print("邮件发送失败：SMTP 认证错误。请检查邮箱账号和密码/授权码，并确认是否开启了相关服务（如Gmail的应用专用密码）。")
    except smtplib.SMTPConnectError:
        print("邮件发送失败：SMTP 连接错误。请检查服务器地址和端口，或网络连接。")
    except Exception as e:
        print(f"邮件发送过程中发生未知错误: {e}")

if __name__ == "__main__":
    send_arh999_report_email()
