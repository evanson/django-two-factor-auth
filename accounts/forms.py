from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def validate_digit(value):
    if not value.isdigit():
        raise ValidationError(u'value must be numeric')


class CreateUserForm(forms.Form):
    COUNTRY_CODE_CHOICES = [('+93', 'Afghanistan (+93)'),('+355', 'Albania (+355)'),('+213', 'Algeria (+213)'),('+376', 'Andorra (+376)'),('+244', 'Angola (+244)'),
                            ('+1264', 'Anguilla (+1264)'),('+54', 'Argentina (+54)'),('+374', 'Armenia (+374)'),('+297', 'Aruba (+297)'),('+61', 'Australia (+61)'),
                            ('+43', 'Austria (+43)'),('+994', 'Azerbaijan (+994)'),('+973', 'Bahrain (+973)'),('+880', 'Bangladesh (+880)'),('+1246', 'Barbados (+1246)'),
                            ('+375', 'Belarus (+375)'),('+32', 'Belgium (+32)'),('+501', 'Belize (+501)'),('+229', 'Benin (+229)'),('+1441', 'Bermuda (+1441)'),
                            ('+975', 'Bhutan (+975)'),('+591', 'Bolivia (+591)'),('+267', 'Botswana (+267)'),('+55', 'Brazil (+55)'),('+359', 'Bulgaria (+359)'),
                            ('+226', 'Burkina Faso (+226)'),('+257', 'Burundi (+257)'),('+855', 'Cambodia (+855)'),('+237', 'Cameroon (+237)'),('+1', 'Canada (+1)'),
                            ('+238', 'Cape Verde (+238)'),('+1345', 'Cayman Islands (+1345)'),('+236', 'Central African Republic (+236)'),('+235', 'Chad (+235)'),
                            ('+56', 'Chile (+56)'),('+86', 'China (+86)'),('+57', 'Colombia (+57)'),('+269', 'Comoros (+269)'),('+242', 'Congo (+242)'),
                            ('+682', 'Cook Islands (+682)'),('+506', 'Costa Rica (+506)'),('+385', 'Croatia (+385)'),('+53', 'Cuba (+53)'),('+5999', 'Curacao (+5999)'),
                            ('+357', 'Cyprus (+357)'),('+420', 'Czech Republic (+420)'),('+45', 'Denmark (+45)'),('+253', 'Djibouti (+253)'),('+1767', 'Dominica (+1767)'),
                            ('+1', 'Dominican Republic (+1)'),('+593', 'Ecuador (+593)'),('+20', 'Egypt (+20)'),('+503', 'El Salvador (+503)'),
                            ('+240', 'Equatorial Guinea (+240)'),('+372', 'Estonia (+372)'),('+251', 'Ethiopia (+251)'),('+500', 'Falkland Islands (+500)'),
                            ('+298', 'Faroe Islands (+298)'),('+679', 'Fiji (+679)'),('+358', 'Finland (+358)'),('+33', 'France (+33)'),('+594', 'French Guiana (+594)'),
                            ('+689', 'French Polynesia (+689)'),('+241', 'Gabon (+241)'),('+220', 'Gambia (+220)'),('+995', 'Georgia (+995)'),('+49', 'Germany (+49)'),
                            ('+233', 'Ghana (+233)'),('+350', 'Gibraltar (+350)'),('+30', 'Greece (+30)'),('+299', 'Greenland (+299)'),('+1473', 'Grenada (+1473)'),
                            ('+590', 'Guadeloupe (+590)'),('+1671', 'Guam (+1671)'),('+502', 'Guatemala (+502)'),('+44', 'Guernsey (+44)'),('+224', 'Guinea (+224)'),
                            ('+592', 'Guyana (+592)'),('+509', 'Haiti (+509)'),('+504', 'Honduras (+504)'),('+36', 'Hungary (+36)'),('+354', 'Iceland (+354)'),
                            ('+91', 'India (+91)'),('+62', 'Indonesia (+62)'),('+98', 'Iran (+98)'),('+964', 'Iraq (+964)'),('+353', 'Ireland (+353)'),
                            ('+44', 'Isle of Man (+44)'),('+972', 'Israel (+972)'),('+39', 'Italy (+39)'),('+1876', 'Jamaica (+1876)'),('+81', 'Japan (+81)'),
                            ('+44', 'Jersey (+44)'),('+962', 'Jordan (+962)'),('+7', 'Kazakhstan (+7)'),('+254', 'Kenya (+254)'),('+965', 'Kuwait (+965)'),
                            ('+996', 'Kyrgyzstan (+996)'),('+371', 'Latvia (+371)'),('+961', 'Lebanon (+961)'),('+266', 'Lesotho (+266)'),('+231', 'Liberia (+231)'),
                            ('+218', 'Libya (+218)'),('+423', 'Liechtenstein (+423)'),('+370', 'Lithuania (+370)'),('+352', 'Luxembourg (+352)'),('+853', 'Macau (+853)'),
                            ('+389', 'Macedonia (+389)'),('+261', 'Madagascar (+261)'),('+265', 'Malawi (+265)'),('+60', 'Malaysia (+60)'),('+960', 'Maldives (+960)'),
                            ('+223', 'Mali (+223)'),('+356', 'Malta (+356)'),('+596', 'Martinique (+596)'),('+222', 'Mauritania (+222)'),('+230', 'Mauritius (+230)'),
                            ('+52', 'Mexico (+52)'),('+373', 'Moldova (+373)'),('+976', 'Mongolia (+976)'),('+382', 'Montenegro (+382)'),('+1664', 'Montserrat (+1664)'),
                            ('+212', 'Morocco (+212)'),('+258', 'Mozambique (+258)'),('+95', 'Myanmar (+95)'),('+264', 'Namibia (+264)'),('+674', 'Nauru (+674)'),
                            ('+977', 'Nepal (+977)'),('+687', 'New Caledonia (+687)'),('+64', 'New Zealand (+64)'),('+505', 'Nicaragua (+505)'),('+227', 'Niger (+227)'),
                            ('+234', 'Nigeria (+234)'),('+47', 'Norway (+47)'),('+968', 'Oman (+968)'),('+92', 'Pakistan (+92)'),('+507', 'Panama (+507)'),
                            ('+675', 'Papua New Guinea (+675)'),('+595', 'Paraguay (+595)'),('+51', 'Peru (+51)'),('+63', 'Philippines (+63)'),('+48', 'Poland (+48)'),
                            ('+351', 'Portugal (+351)'),('+1', 'Puerto Rico (+1)'),('+974', 'Qatar (+974)'),('+262', 'Reunion (+262)'),('+40', 'Romania (+40)'),
                            ('+250', 'Rwanda (+250)'),('+378', 'San Marino (+378)'),('+966', 'Saudi Arabia (+966)'),('+221', 'Senegal (+221)'),('+381', 'Serbia (+381)'),
                            ('+248', 'Seychelles (+248)'),('+232', 'Sierra Leone (+232)'),('+65', 'Singapore (+65)'),('+421', 'Slovakia (+421)'),('+386', 'Slovenia (+386)'),
                            ('+677', 'Solomon Islands (+677)'),('+252', 'Somalia (+252)'),('+27', 'South Africa (+27)'),('+34', 'Spain (+34)'),('+94', 'Sri Lanka (+94)'),
                            ('+249', 'Sudan (+249)'),('+597', 'Suriname (+597)'),('+268', 'Swaziland (+268)'),('+46', 'Sweden (+46)'),('+41', 'Switzerland (+41)'),
                            ('+963', 'Syria (+963)'),('+886', 'Taiwan (+886)'),('+992', 'Tajikistan (+992)'),('+255', 'Tanzania (+255)'),('+66', 'Thailand (+66)'),
                            ('+228', 'Togo (+228)'),('+1868', 'Trinidad and Tobago (+1868)'),('+216', 'Tunisia (+216)'),('+90', 'Turkey (+90)'),('+993', 'Turkmenistan (+993)'),
                            ('+1649', 'Turks and Caicos Islands (+1649)'),('+256', 'Uganda (+256)'),('+380', 'Ukraine (+380)'),('+971', 'United Arab Emirates (+971)'),
                            ('+44', 'United Kingdom (+44)'),('+1', 'United States (+1)'),('+598', 'Uruguay (+598)'),('+998', 'Uzbekistan (+998)'),('+678', 'Vanuatu (+678)'),
                            ('+58', 'Venezuela (+58)'),('+84', 'Vietnam (+84)'),('+967', 'Yemen (+967)'),('+260', 'Zambia (+260)'),('+263', 'Zimbabwe (+263)')]

    username = forms.CharField(max_length=30)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    country_code = forms.ChoiceField(choices=COUNTRY_CODE_CHOICES)
    phone_number = forms.CharField(validators=[validate_digit])

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        raise forms.ValidationError("A user with this username already exists")

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

        raise forms.ValidationError("A user with this email already exists")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("passwords don't match")

        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            password=self.cleaned_data['password1'],
                                            email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.is_active = False
        new_user.save()

        return new_user


class TokenForm(forms.Form):
    token = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.generated_token = kwargs.pop('gen_token')
        super(TokenForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data['token']

        if token != self.generated_token:
            raise forms.ValidationError('Invalid token')

        return token


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            else:
                if not user.is_active:
                    raise forms.ValidationError("Login Account for [%s] is currently disabled. \
                    Please activate your account by clicking the activation link sent to your email" % self.cleaned_data['username'])
        return self.cleaned_data
