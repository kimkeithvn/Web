from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # widget: 定义生成的html标签形式
    username_or_email = forms.CharField(label='用户名或邮箱',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))

    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入8-20位用户名'}))

    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击发送"验证码"发送到指定邮箱'}))

    password = forms.CharField(label='密码',
                               max_length=20,
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入6-20位密码'}))

    pwd_again = forms.CharField(label='密码',
                                max_length=20,
                                min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_code', '')  # 生成的验证码
        verification_code = self.cleaned_data.get('verification_code', '')  # 用户填写的验证码
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_pwd_again(self):
        password = self.cleaned_data['password']
        pwd_again = self.cleaned_data['pwd_again']
        if password != pwd_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return pwd_again

    def clean_verifivation_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangeNicknameForm(forms.Form):
    new_nickname = forms.CharField(label='新的昵称',
                                   widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        return self.cleaned_data

    def clean_new_nickname(self):
        new_nickname = self.cleaned_data.get('new_nickname', '').strip()
        if new_nickname == '':
            raise forms.ValidationError('新的昵称不能为空')
        return new_nickname


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': '请输入您的邮箱地址'}))

    verification_code = forms.CharField(label='验证码', required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到指定邮箱'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登陆')

        # 判断用户是否已经绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('您已绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')  # 生成的验证码
        verification_code = self.cleaned_data.get('verification_code', '')  # 用户填写的验证码
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

    def clean_verifivation_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码',
                                   widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}))

    new_password = forms.CharField(label='新的密码',
                                   widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))

    new_pwd_again = forms.CharField(label='新的密码',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    # 验证新的密码是否一致
    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        new_pwd_again = self.cleaned_data.get('new_pwd_again', '')
        if new_password != new_pwd_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        else:
            return self.cleaned_data

    # 验证旧的密码是否正确
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        else:
            return old_password


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱'}))

    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到用户邮箱'}))

    new_password = forms.CharField(label='新的密码',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if email == '':
            raise forms.ValidationError('邮箱不能为空')
        else:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verifivation_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码是否一致
        code = self.request.session.get('forget_password_code', '')  # 生成的验证码
        verification_code = self.cleaned_data.get('verification_code', '')  # 用户填写的验证码
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code
