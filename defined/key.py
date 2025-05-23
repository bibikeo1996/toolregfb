import os
class KeyCode:
    KEYCODE_0 = 7
    KEYCODE_1 = 8
    KEYCODE_2 = 9
    KEYCODE_3 = 10
    KEYCODE_4 = 11
    KEYCODE_5 = 12
    KEYCODE_6 = 13
    KEYCODE_7 = 14
    KEYCODE_8 = 15
    KEYCODE_9 = 16
    KEYCODE_A = 29
    KEYCODE_B = 30
    KEYCODE_C = 31
    KEYCODE_D = 32
    KEYCODE_E = 33
    KEYCODE_F = 34
    KEYCODE_G = 35
    KEYCODE_H = 36
    KEYCODE_I = 37
    KEYCODE_J = 38
    KEYCODE_K = 39
    KEYCODE_L = 40
    KEYCODE_M = 41
    KEYCODE_N = 42
    KEYCODE_O = 43
    KEYCODE_P = 44
    KEYCODE_Q = 45
    KEYCODE_R = 46
    KEYCODE_S = 47
    KEYCODE_T = 48
    KEYCODE_U = 49
    KEYCODE_V = 50
    KEYCODE_W = 51
    KEYCODE_X = 52
    KEYCODE_Y = 53
    KEYCODE_Z = 54
    KEYCODE_ENTER = 66
    KEYCODE_DEL = 67
    KEYCODE_SPACE = 62
    KEYCODE_SYM = 63
    KEYCODE_EXPLORER = 64
    KEYCODE_ENVELOPE = 65
    KEYCODE_GRAVE = 68
    KEYCODE_MINUS = 69
    KEYCODE_EQUALS = 70
    KEYCODE_LEFT_BRACKET = 71
    KEYCODE_RIGHT_BRACKET = 72
    KEYCODE_BACKSLASH = 73
    KEYCODE_SEMICOLON = 74
    KEYCODE_APOSTROPHE = 75
    KEYCODE_SLASH = 76
    KEYCODE_AT = 77         # Ký tự @
    KEYCODE_PERIOD = 56     # Ký tự .
    KEYCODE_NUM = 78
    KEYCODE_HEADSETHOOK = 79
    KEYCODE_FOCUS = 80
    KEYCODE_PLUS = 81
    KEYCODE_MENU = 82
    KEYCODE_NOTIFICATION = 83
    KEYCODE_APP_SWITCH = 187

class Action:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    setDate_Btn = os.path.join(base_dir, '..', 'imageAction', 'setdate.png')
    sett_Btn = os.path.join(base_dir, '..', 'imageAction', 'set.png')

    createbutton_Btn = os.path.join(base_dir, '..', 'imageAction', 'createaccount.png')
    getstarted_Btn = os.path.join(base_dir, '..', 'imageAction', 'getstarted.png')
    firstname2_Btn = os.path.join(base_dir, '..', 'imageAction', 'firstname2.png')
    firstname3_Btn = os.path.join(base_dir, '..', 'imageAction', 'firstname3.png')
    lastname_Btn = os.path.join(base_dir, '..', 'imageAction', 'lastname.png')
    nextt_Btn = os.path.join(base_dir, '..', 'imageAction', 'next.png')
    choosedateAgain_Btn = os.path.join(base_dir, '..', 'imageAction', 'choosedate.png')
    resetdateagain_Btn = os.path.join(base_dir, '..', 'imageAction', 'resetdateagain.png')
    month_Btn = os.path.join(base_dir, '..', 'imageAction', 'month.png')
    date_Btn = os.path.join(base_dir, '..', 'imageAction', 'date.png')
    year_Btn = os.path.join(base_dir, '..', 'imageAction', 'year.png')
    selectyourname_Btn = os.path.join(base_dir, '..', 'imageAction', 'selectyourname.png')
    pickname_Btn = os.path.join(base_dir, '..', 'imageAction', 'pickname.png')
    female_Btn = os.path.join(base_dir, '..', 'imageAction', 'female.png')
    male_Btn = os.path.join(base_dir, '..', 'imageAction', 'male.png')
    defaultClick_btn = os.path.join(base_dir, '..', 'imageAction', 'clickDefault.png')

    agree_Btn = os.path.join(base_dir, '..', 'imageAction', 'agree.png')
    allowaccesscamera_Btn = os.path.join(base_dir, '..', 'imageAction', 'allowaccesscamera.png')
    skip1_Btn = os.path.join(base_dir, '..', 'imageAction', 'skip1.png')
    skip_Btn = os.path.join(base_dir, '..', 'imageAction', 'skipbtn.png')
    notnow_Btn = os.path.join(base_dir, '..', 'imageAction', 'notnow.png')
    ok_Btn = os.path.join(base_dir, '..', 'imageAction', 'ok.png')
    passwordField_Btn = os.path.join(base_dir, '..', 'imageAction', 'passwordfield.png')
    clickcreatepassword_Btn = os.path.join(base_dir, '..', 'imageAction', 'clickcreatepassword.png')
    deny_Btn = os.path.join(base_dir, '..', 'imageAction', 'deny.png')
    emailfield_Btn = os.path.join(base_dir, '..', 'imageAction', 'emailfield.png')
    emailfieldv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'emailfieldv2.png')
    phonenumberfield_Btn = os.path.join(base_dir, '..', 'imageAction', 'phonenumberfield.png')
    
    doyouhaveaccount_Btn = os.path.join(base_dir, '..', 'imageAction', 'doyouhaveaccount.png')
    continuecreate_Btn = os.path.join(base_dir, '..', 'imageAction', 'continueCreate.png')
    

    statusContent_Btn = os.path.join(base_dir, '..', 'imageAction', 'statusContent.png')
    postFirstStatus_Btn = os.path.join(base_dir, '..', 'imageAction', 'postFirstStatus.png')
    signupWithEmail_Btn = os.path.join(base_dir, '..', 'imageAction', 'signupWithEmail.png')
    clickWhatYourEmail_Btn = os.path.join(base_dir, '..', 'imageAction', 'clickWhatsyouremail.png')
    chat_Btn = os.path.join(base_dir, '..', 'imageAction', 'chat.png')
    whatvideo_Btn = os.path.join(base_dir, '..', 'imageAction', 'whatvideo.png')
    verifycodefield_Btn = os.path.join(base_dir, '..', 'imageAction', 'verifycode.png')

    successReg_Btn = os.path.join(base_dir, '..', 'imageAction', 'successReg.png')
    successReg2_Btn = os.path.join(base_dir, '..', 'imageAction', 'successReg2.png')
    successReg3_Btn = os.path.join(base_dir, '..', 'imageAction', 'successReg3.png')

    issue282_Btn = os.path.join(base_dir, '..', 'imageAction', 'err282.png')
    issue282v2_Btn = os.path.join(base_dir, '..', 'imageAction', 'err282v2.png')
    issue282v3_Btn = os.path.join(base_dir, '..', 'imageAction', 'err282v3.jpg')

    somethingwrongpopup_Btn = os.path.join(base_dir, '..', 'imageAction', 'somethingwrongpopup.png')
    wrongdate_Btn = os.path.join(base_dir, '..', 'imageAction', 'wrongdate.png')
    validateName_Btn = os.path.join(base_dir, '..', 'imageAction', 'validateName.png')

    isStartedLD_Btn = os.path.join(base_dir, '..', 'imageAction', 'isStarted.png')

    isLDRunning_Btn = os.path.join(base_dir, '..', 'imageAction', 'isLDRunning.png')
    isFacebookExist_Btn = os.path.join(base_dir, '..', 'imageAction', 'facebook.png')
    isOpenApp_Btn = os.path.join(base_dir, '..', 'imageAction', 'openapp.png')
    isInvalidEmail_Btn = os.path.join(base_dir, '..', 'imageAction', 'invalidemail.png')
    isInvalidBirth_Btn = os.path.join(base_dir, '..', 'imageAction', 'validaBirth.png')
    isInvalidAccount_Btn = os.path.join(base_dir, '..', 'imageAction', 'invalidaccount.png')

    sendviasmsField_Btn = os.path.join(base_dir, '..', 'imageAction', 'sendviasms.png')
    sendviasmsFieldv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'sendviasmsv2.png')
    sendviasmsFieldv3_Btn = os.path.join(base_dir, '..', 'imageAction', 'sendviasmsv3.jpg')

    ididntgethecode_Btn = os.path.join(base_dir, '..', 'imageAction', 'ididntgethecode.png')
    confimbyemailbtn_Btn = os.path.join(base_dir, '..', 'imageAction', 'confimbyemailbtn.png')

    clearField_Btn = os.path.join(base_dir, '..', 'imageAction', 'clearfield.png')
    clearFieldv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'clearfieldv2.jpg')

    agefield_Btn = os.path.join(base_dir, '..', 'imageAction', 'agefield.jpg')
    okHideBirthDate_Btn = os.path.join(base_dir, '..', 'imageAction', 'okHideBirthDate.jpg')

    turnonProxifier_Btn = os.path.join(base_dir, '..', 'imageAction', 'turnonProxifier.jpg')
    decidelater_Btn = os.path.join(base_dir, '..', 'imageAction', 'decidelater.jpg')

    
    idontseemyaccountv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'idontseemyaccountv2.png')
    idontseemyaccountv3_Btn = os.path.join(base_dir, '..', 'imageAction', 'idontseemyaccountv3.png')
    tryanotherway_Btn = os.path.join(base_dir, '..', 'imageAction', 'tryanotherway.png')

    wrongphonenumber_Btn = os.path.join(base_dir, '..', 'imageAction', 'wrongphonenumber.png')
    

    smslimitreached_Btn = os.path.join(base_dir, '..', 'imageAction', 'smslimit.png')
    smsreachlimitfield_Btn = os.path.join(base_dir, '..', 'imageAction', 'smsreachlimitfield.jpg')
    smsreachlimitAdd_Btn = os.path.join(base_dir, '..', 'imageAction', 'addSmsreachlimit.png')
    
    sendcodeviasms_Btn = os.path.join(base_dir, '..', 'imageAction', 'sendcode.png')
    # sendviaemail_Btn = os.path.join(base_dir, '..', 'imageAction', 'confirmviaemail.png')
    newEmailField_Btn = os.path.join(base_dir, '..', 'imageAction', 'newemail.png')
    phonenumber_Btn = os.path.join(base_dir, '..', 'imageAction', 'phonenumberfield.png')
    confirmviaemail_Btn = os.path.join(base_dir, '..', 'imageAction', 'confirmviaemail.png')
    confirmviaemailv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'comfirmviaemailv2.png')
    nextviaemail_Btn = os.path.join(base_dir, '..', 'imageAction', 'newemailnext.png')
    incorrectemail_Btn = os.path.join(base_dir, '..', 'imageAction', 'incorrectemail.png')
    isphonenumused_Btn = os.path.join(base_dir, '..', 'imageAction', 'phonenumused.png')


    wecounldntfindyouaccount_Btn = os.path.join(base_dir, '..', 'imageAction', 'wecounldntfindyouaccount.png')
    wecounldntfindyouaccountv2_Btn = os.path.join(base_dir, '..', 'imageAction', 'wecouldntcreateaccountforyou.jpg')
    wecoulndfindyouraccountOk_Btn = os.path.join(base_dir, '..', 'imageAction', 'wecoulndfindyouraccountOk.png')

