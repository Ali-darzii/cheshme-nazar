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
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Your OTP Code</title>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f4; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding: 30px 0;">
                <table width="100%" max-width="400" cellpadding="0" cellspacing="0"
                       style="background:#ffffff; padding:30px; border-radius:8px;">
                    
                    <tr>
                        <td align="center">
                            <h2 style="margin:0; color:#333;">Verification Code</h2>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding:20px 0; color:#555; text-align:center;">
                            Use the following OTP to verify your email:
                        </td>
                    </tr>

                    <tr>
                        <td align="center" style="padding:20px 0;">
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
                        <td style="padding-top:20px; font-size:14px; color:#777; text-align:center;">
                            This code will expire in <strong>{EXPIRE_TIME} secondes</strong>.<br>
                            If you did not request this, please ignore this email.
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