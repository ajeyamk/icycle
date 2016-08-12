from .email_templates import EmailContainer


class ForgotPasswordEmail(EmailContainer):
    subject = 'Password reset request'
    message = 'A request was made to reset your account password. Please use the following token in the app to reset your password: %s'
    email_template = 'email_templates/appauth/forgot_password.html'


class PasswordChangeSuccessEmail(EmailContainer):
    subject = 'Password changed successfully'
    message = 'Your password has been changed successfully!'
    email_template = 'email_templates/appauth/password_change_success.html'


class PasswordChangeFailEmail(EmailContainer):
    subject = 'Password change unsuccessful'
    message = 'An attempt was made to change your account password. If it wasn\'t you, please contact: info@gmail.com'
    email_template = 'email_templates/appauth/password_change_fail.html'
