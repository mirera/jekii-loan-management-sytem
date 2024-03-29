from user.models import CompanyStaff
from django.contrib.auth.models import User
from member.models import Member
from company.models import Organization, Package, SmsSetting, SystemSetting, SecuritySetting
from jekiiLMS.tasks import send_email_task, send_sms_task


#get the company of a user.
def get_user_company(request): 
    if request.user.is_authenticated and request.user.is_active:
        try:
            companystaff = CompanyStaff.objects.get(username=request.user.username)
            company = companystaff.company
        except CompanyStaff.DoesNotExist:
            company = None
    else:
        company = None

    return company

# activate staff/user
def activate_user(uid):
    staff = CompanyStaff.objects.get(id=uid)
    staff.status = 'active'
    staff.save()

    company = staff.company
    user = User.objects.get(username=staff.username) 
    user.is_active= True
    user.save()
    #send sms
    sms_setting = SmsSetting.objects.get(company=company)
    sender_id = sms_setting.sender_id
    token = sms_setting.api_token 
    message = f"Dear {staff.first_name}, Your {company.name} user account has been activated. You can now login"
    
    preferences = SystemSetting.objects.get(company=company)
    if preferences.is_send_sms and sender_id is not None and token is not None:
        send_sms_task.delay(
        sender_id,
        token,
        staff.phone_no, 
        message,
        )

# deactivate staff/user
def deactivate_user(uid):
    staff = CompanyStaff.objects.get(id=uid)
    user = User.objects.get(username=staff.username)
    company = staff.company
    system_preferences = SystemSetting.objects.get(company=company)
    staff.status = 'inactive'
    user.is_active= False
    user.save()
    staff.save()
    
    if system_preferences.is_send_sms:
        #send sms
        sms_setting = SmsSetting.objects.get(company=company) 
        sender_id = sms_setting.sender_id
        token = sms_setting.api_token 
        message = f"Dear {staff.first_name}, Your {company.name} user account has been deactivated. Contact your system admin"
        preferences = SystemSetting.objects.get(company=company)
        if preferences.is_send_sms and sender_id is not None and token is not None:
            send_sms_task.delay(
                sender_id,
                token,
                staff.phone_no, 
                message,
            )

# delete staff
def delete_staff(uid):
    staff = CompanyStaff.objects.get(id=uid)
    user = User.objects.get(username=staff.username)
    staff.delete()
    user.delete()

# delete member
def delete_member(uid):
    member = Member.objects.get(id=uid)
    member.delete()

phone_codes = [
    ('+93', 'AF +93'),
    ('+355', 'AL +355'),
    ('+213', 'DZ +213'),
    ('+376', 'AD +376'),
    ('+244', 'AO +244'),
    ('+1264', 'AI +1264'),
    ('+672', 'AQ +672'),
    ('+54', 'AR +54'),
    ('+374', 'AM +374'),
    ('+297', 'AW +297'),
    ('+61', 'AU +61'),
    ('+43', 'AT +43'),
    ('+994', 'AZ +994'),
    ('+1242', 'BS +1242'),
    ('+973', 'BH +973'),
    ('+880', 'BD +880'),
    ('+1246', 'BB +1246'),
    ('+375', 'BY +375'),
    ('+32', 'BE +32'),
    ('+501', 'BZ +501'),
    ('+229', 'BJ +229'),
    ('+1441', 'BM +1441'),
    ('+975', 'BT +975'),
    ('+591', 'BO +591'),
    ('+387', 'BA +387'),
    ('+267', 'BW +267'),
    ('+55', 'BR +55'),
    ('+246', 'IO +246'),
    ('+673', 'BN +673'),
    ('+359', 'BG +359'),
    ('+226', 'BF +226'),
    ('+257', 'BI +257'),
    ('+855', 'KH +855'),
    ('+237', 'CM +237'),
    ('+1', 'CA +1'),
    ('+238', 'CV +238'),
    ('+599', 'BQ +599'),
    ('+236', 'CF +236'),
    ('+235', 'TD +235'),
    ('+56', 'CL +56'),
    ('+86', 'CN +86'),
    ('+61', 'CX +61'),
    ('+57', 'CO +57'),
    ('+269', 'KM +269'),
    ('+243', 'CD +243'),
    ('+242', 'CG +242'),
    ('+682', 'CK +682'),
    ('+506', 'CR +506'),
    ('+225', 'CI +225'),
    ('+385', 'HR +385'),
    ('+53', 'CU +53'),
    ('+599', 'CW +599'),
    ('+357', 'CY +357'),
    ('+420', 'CZ +420'),
    ('+45', 'DK +45'),
    ('+253', 'DJ +253'),
    ('+1767', 'DM +1767'),
    ('+1809', 'DO +1809'),
    ('+1829', 'DO +1829'),
    ('+1849', 'DO +1849'),
    ('+593', 'EC +593'),
    ('+20', 'EG +20'),
    ('+503', 'SV +503'),
    ('+240', 'GQ +240'),
    ('+291', 'ER +291'),
    ('+372', 'EE +372'),
    ('+251', 'ET +251'),
    ('+500', 'FK +500'),
    ('+298', 'FO +298'),
    ('+679', 'FJ +679'),
    ('+358', 'FI +358'),
    ('+33', 'FR +33'),
    ('+594', 'GF +594'),
    ('+689', 'PF +689'),
    ('+241', 'GA +241'),
    ('+220', 'GM +220'),
    ('+995', 'GE +995'),
    ('+49', 'DE +49'),
    ('+233', 'GH +233'),
    ('+350', 'GI +350'),
    ('+30', 'GR +30'),
    ('+299', 'GL +299'),
    ('+1473', 'GD +1473'),
    ('+590', 'GP +590'),
    ('+1671', 'GU +1671'),
    ('+502', 'GT +502'),
    ('+44', 'GG +44'),
    ('+224', 'GN +224'),
    ('+245', 'GW +245'),
    ('+592', 'GY +592'),
    ('+509', 'HT +509'),
    ('+379', 'VA +379'),
    ('+504', 'HN +504'),
    ('+852', 'HK +852'),
    ('+36', 'HU +36'),
    ('+354', 'IS +354'),
    ('+91', 'IN +91'),
    ('+62', 'ID +62'),
    ('+98', 'IR +98'),
    ('+964', 'IQ +964'),
    ('+353', 'IE +353'),
    ('+44', 'IM +44'),
    ('+972', 'IL +972'),
    ('+39', 'IT +39'),
    ('+1876', 'JM +1876'),
    ('+81', 'JP +81'),
    ('+44', 'JE +44'),
    ('+962', 'JO +962'),
    ('+7', 'KZ +7'),
    ('+254', 'KE +254'),
    ('+686', 'KI +686'),
    ('+965', 'KW +965'),
    ('+996', 'KG +996'),
    ('+856', 'LA +856'),
    ('+371', 'LV +371'),
    ('+961', 'LB +961'),
    ('+266', 'LS +266'),
    ('+231', 'LR +231'),
    ('+218', 'LY +218'),
    ('+423', 'LI +423'),
    ('+370', 'LT +370'),
    ('+352', 'LU +352'),
    ('+853', 'MO +853'),
    ('+389', 'MK +389'),
    ('+261', 'MG +261'),
    ('+265', 'MW +265'),
    ('+60', 'MY +60'),
    ('+960', 'MV +960'),
    ('+223', 'ML +223'),
    ('+356', 'MT +356'),
    ('+692', 'MH +692'),
    ('+596', 'MQ +596'),
    ('+222', 'MR +222'),
    ('+230', 'MU +230'),
    ('+262', 'YT +262'),
    ('+52', 'MX +52'),
    ('+691', 'FM +691'),
    ('+373', 'MD +373'),
    ('+377', 'MC +377'),
    ('+976', 'MN +976'),
    ('+382', 'ME +382'),
    ('+1664', 'MS +1664'),
    ('+212', 'MA +212'),
    ('+258', 'MZ +258'),
    ('+95', 'MM +95'),
    ('+264', 'NA +264'),
    ('+674', 'NR +674'),
    ('+977', 'NP +977'),
    ('+31', 'NL +31'),
    ('+687', 'NC +687'),
    ('+64', 'NZ +64'),
    ('+505', 'NI +505'),
    ('+227', 'NE +227'),
    ('+234', 'NG +234'),
    ('+683', 'NU +683'),
    ('+672', 'NF +672'),
    ('+850', 'KP +850'),
    ('+1670', 'MP +1670'),
    ('+47', 'NO +47'),
    ('+968', 'OM +968'),
    ('+92', 'PK +92'),
    ('+680', 'PW +680'),
    ('+970', 'PS +970'),
    ('+507', 'PA +507'),
    ('+675', 'PG +675'),
    ('+595', 'PY +595'),
    ('+51', 'PE +51'),
    ('+63', 'PH +63'),
    ('+64', 'PN +64'),
    ('+48', 'PL +48'),
    ('+351', 'PT +351'),
    ('+1787', 'PR +1787'),
    ('+974', 'QA +974'),
    ('+40', 'RO +40'),
    ('+7', 'RU +7'),
    ('+250', 'RW +250'),
    ('+590', 'BL +590'),
    ('+290', 'SH +290'),
    ('+1869', 'KN +1869'),
    ('+1758', 'LC +1758'),
    ('+590', 'MF +590'),
    ('+508', 'PM +508'),
    ('+1784', 'VC +1784'),
    ('+685', 'WS +685'),
    ('+378', 'SM +378'),
    ('+239', 'ST +239'),
    ('+966', 'SA +966'),
    ('+221', 'SN +221'),
    ('+381', 'RS +381'),
    ('+248', 'SC +248'),
    ('+232', 'SL +232'),
    ('+65', 'SG +65'),
    ('+1721', 'SX +1721'),
    ('+421', 'SK +421'),
    ('+386', 'SI +386'),
    ('+677', 'SB +677'),
    ('+252', 'SO +252'),
    ('+27', 'ZA +27'),
    ('+82', 'KR +82'),
    ('+211', 'SS +211'),
    ('+34', 'ES +34'),
    ('+94', 'LK +94'),
    ('+249', 'SD +249'),
    ('+597', 'SR +597'),
    ('+4779', 'SJ +4779'),
    ('+268', 'SZ +268'),
    ('+46', 'SE +46'),
    ('+41', 'CH +41'),
    ('+963', 'SY +963'),
    ('+886', 'TW +886'),
    ('+992', 'TJ +992'),
    ('+255', 'TZ +255'),
    ('+66', 'TH +66'),
    ('+670', 'TL +670'),
    ('+228', 'TG +228'),
    ('+690', 'TK +690'),
    ('+676', 'TO +676'),
    ('+1868', 'TT +1868'),
    ('+216', 'TN +216'),
    ('+90', 'TR +90'),
    ('+993', 'TM +993'),
    ('+1649', 'TC +1649'),
    ('+688', 'TV +688'),
    ('+256', 'UG +256'),
    ('+380', 'UA +380'),
    ('+971', 'AE +971'),
    ('+44', 'GB +44'),
    ('+1', 'US +1'),
    ('+598', 'UY +598'),
    ('+998', 'UZ +998'),
    ('+678', 'VU +678'),
    ('+58', 'VE +58'),
    ('+84', 'VN +84'),
    ('+1284', 'VG +1284'),
    ('+1340', 'VI +1340'),
    ('+681', 'WF +681'),
    ('+967', 'YE +967'),
    ('+260', 'ZM +260'),
    ('+263', 'ZW +263')
]
