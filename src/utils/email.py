from email.mime.text import MIMEText
from smtplib import SMTP  # use this for standard SMTP protocol   (port 25, no encryption)

from src.config import setting


class EmailSender:
    """ for now we Email sender is in utils, till we need email module """
    @staticmethod
    def send(emails: list, msg: str, subject: str, subtype="plain") :
        msg = MIMEText(msg, subtype)
        msg['Subject'] = subject
        msg['From'] = setting.EMAIL_SERVER_USER 
        with SMTP(setting.EMAIL_SERVER) as conn :
            conn.set_debuglevel(False)
            conn.login(setting.EMAIL_SERVER_USER, setting.EMAIL_SERVER_PASS)
            try:
                conn.sendmail(setting.EMAIL_SERVER_USER, emails, msg.as_string())
            finally:
                    conn.quit()
                    
OTP_MESSAGE = """
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8" />
    <title>کد تأیید</title>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f4; font-family: Tahoma, Arial, sans-serif; direction: rtl;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding: 30px 0;">
                <table width="100%" max-width="400" cellpadding="0" cellspacing="0"
                       style="background:#ffffff; padding:30px; border-radius:8px; text-align:center;">
                    
                    <tr>
                        <td>
                            <h2 style="margin:0; color:#333;">
                                کد تأیید ایمیل
                            </h2>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:20px 0; color:#555;">
                            برای تأیید ایمیل خود، از کد زیر استفاده کنید:
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:20px 0;">
                            <div style="
                                font-size:28px;
                                letter-spacing:6px;
                                font-weight:bold;
                                color:#000;
                                background:#f0f0f0;
                                padding:15px 25px;
                                display:inline-block;
                                border-radius:6px;
                            ">
                                {{OTP_CODE}}
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding-top:20px; font-size:14px; color:#777;">
                            این کد تا <strong>{EXPIRE_TIME} ثانیه</strong> معتبر است.<br>
                            اگر این درخواست توسط شما انجام نشده است، این ایمیل را نادیده بگیرید.
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
          
                
class MessageProducer:
    
    @staticmethod
    def send_otp(otp: int, expire_seconds: int) -> str:
        return OTP_MESSAGE.format(
            OTP_CODE=otp,
            EXPIRE_TIME=expire_seconds
        )