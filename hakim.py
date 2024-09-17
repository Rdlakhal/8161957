import os
import requests
import logging
import telebot
from telebot import types
from requests.auth import HTTPBasicAuth
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import time


API_TOKEN = "7465647986:AAFg7rMl7CGZ133FCX2LhJRhOlyL2D1SaB8"
bot = telebot.TeleBot(API_TOKEN)

username = "Rdlakhal"
token = "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"
repo = "8161957"
file_path = "data.txt"

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "bot-ff-ce808",
  "private_key_id": "2de18bf0a5522000e38bdbe8384e95f7768587d2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC85sphD9j12e0q\nfG8wvnTGSSpqeh4s3PSCHe29VWkvYYFHBkgG2iDLLUlmDntLF6Bb50wg/63iH6w8\ne9SwH53BeqM3SHX4pYX7GSQ4wkPiESws82dUSvdJHeiof7jNKA+salO5CmWm8Y0/\nHpI0j59ERQmDT5SnyLvE6FAKryxyn2Rky3FnHYUAPC8Aj6PZqLpgeWeN67QbvU7Z\n9ZZMB/EFtvx7xWuFnR/GWlv6GdoyPpqiNIoR9fCyUhqRyDQlyAmhwFws9BQx11O1\nVTx7YZ/8Jc+plXRi39HnYZsc3RYXAojqNFdgdFXr8aZgCTxfibGgYSwUg1sq9YWp\no351AcqrAgMBAAECggEAC1pIyhHhwCTGFB+WWcpDH7JAp6rfKrhnbsp4V0Ci1FjP\nzteZzI+fbkEygBJZZpHs7pkKrOZbf5OCY8AtcB2g+tfGp16Qzc4PgfUThYsR+VbU\nM39is7Ytq79DFEgDcJD6dX+OYziKE2vA9AzU90O1Fq1E0mzIn6zOBsTPdVTsdEGg\nSOSuIjb1xH3fWNj22JDsdn9roysWt/y4/jurVcarzUxzJ4pc7CW4UFCuR9fDpwVN\nUewEXTZ8/n22CJ1lvEIa3RZGpFHqM2JVXZ8BKrWW9u26QQ3cWQyt+LhoML7ltayc\nmlK9A4ng/q63kMuLwRPT4Zvax8Cs7NKsxqxqB+LFAQKBgQDhYXl3lEt0A3cNghYg\nEz8FNjS+SZ5f27HjvJOnMOsEe/sI03qSyPo2LjT41XxTPNl7AmA7r9cGJSOBjEoQ\nIbNkHGTuB/0IbvY013VGAn8/z4lXylVofkGG6Ant4PwPRfJ1m47CCm6pBykmUEft\nXBuiLVxkPuE3fG1ETu036OeG8QKBgQDWkJp9GhKLTaYz8xoIcSb/YrFevg77p6Rm\nao4z/rsRBlaHEgIbY+VaNaIZRdjsbqj1NdddNZB5OGyG7mQTcUkMLnKWL9koMEyI\nbJVWuqeu6p3HKRQw4cdC2MvrCSd/Jzo38qeIct2wfzvf8Qw8Vyw4sZsdOOWa6wxl\n1o/AdiADWwKBgAsREDfQ7kuKCAR/yLpWd5e366sUTlSCox99mPpyqneT5uWuDKy8\ndZzHdA5r3SjxKfSiTztfDP3eQPoRe2mDXh2iT0po1gHeAPTjR3zijoEBncrTwpHY\n8TrAlgw6KeZOFvOzabUZcgmWsmyRMJb1GN5Dv++kLsbcszjRb1B5fTThAoGBAJcK\nWBY0olU5pgPv36WNsbwZh26AMB/q1QnbfJsReDH12jde7+jEG5GzK5bK2nclNv7W\nlfJhYIBUveEGM6CUIK3YjIU4zY9C4L0wYrgY0S2KruKiAjqe1RwzbOjZGtqhjJQR\n1ulwoqo6BrYQA2L+onyOWfjqMocpayLNNYhwHvz9AoGALfNwOPg8Wmufx9Ok8ocF\nMLfnuGzj7+bc/AMTzLvyLzTffFH5dpdtCuP/a9Y7vvrL29og2V20g8/kSByFIrmo\nsraSZyPGUZxztcOQ7epIJr/uFAUsWTrPR3GCCpJJf7tvA5MamUWxqV4iiBRqqJwy\n9VepexXDZwnaSN/ZxQC35kY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hyjvw@bot-ff-ce808.iam.gserviceaccount.com",
  "client_id": "116844755629790343548",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hyjvw%40bot-ff-ce808.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()

# إعداد logger
logging.basicConfig(filename='bot_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_event(event):
    logging.info(event)


def notify_admins_on_failure(message):
    admin_ids = get_admins_from_firebase()
    for admin_id in admin_ids:
        bot.send_message(admin_id, message)


def get_github_file():
    try:
        url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, token))
        if response.status_code == 200:
            return response.json()
        else:
            log_event(f"Failed to get GitHub file: {response.status_code}")
            return None
    except Exception as e:
        log_event(f"Exception in get_github_file: {str(e)}")
        notify_admins_on_failure(f"Failed to access GitHub file: {str(e)}")
        return None


def update_github_file(updated_content):
    try:
        file_content = get_github_file()
        if not file_content:
            return False

        sha = file_content['sha']
        encoded_content = base64.b64encode(updated_content.encode()).decode()

        data = {
            "message": "تحديث الملف",
            "content": encoded_content,
            "sha": sha
        }

        url = f"https://api.github.com/repos/{username}/{repo}/contents/{file_path}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.put(url, json=data, headers=headers, auth=HTTPBasicAuth(username, token))

        if response.status_code == 200:
            log_event("GitHub file updated successfully")
            return True
        else:
            log_event(f"Failed to update GitHub file: {response.status_code}")
            return False
    except Exception as e:
        log_event(f"Exception in update_github_file: {str(e)}")
        notify_admins_on_failure(f"Failed to update GitHub file: {str(e)}")
        return False


def encode_text(text):
    try:
        api_url = f"https://c4.freefireinfo.site/api/{text}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.text
        else:
            log_event(f"Failed to encode text: {response.status_code}")
            return "Error Encode"
    except Exception as e:
        log_event(f"Exception in encode_text: {str(e)}")
        notify_admins_on_failure(f"Failed to encode text: {str(e)}")
        return "Error Encode"


def delete_unencoded_text(text_to_delete):
    try:
        file_content = get_github_file()
        if not file_content:
            return False

        decoded_content = base64.b64decode(file_content['content']).decode()

        if text_to_delete not in decoded_content:
            text_to_delete = encode_text(text_to_delete)

        updated_content = "\n".join(line for line in decoded_content.splitlines() if line != text_to_delete)

        return update_github_file(updated_content)
    except Exception as e:
        log_event(f"Exception in delete_unencoded_text: {str(e)}")
        notify_admins_on_failure(f"Failed to delete text: {str(e)}")
        return False


def update_github_file_with_check(encoded_text):
    try:
        file_content = get_github_file()
        if file_content:
            decoded_content = base64.b64decode(file_content['content']).decode()
            if encoded_text in decoded_content:
                log_event(f"Encoded text {encoded_text} already exists in GitHub file.")
                return True

            updated_content = decoded_content + "\n" + encoded_text
            return update_github_file(updated_content)
        return False
    except Exception as e:
        log_event(f"Exception in update_github_file_with_check: {str(e)}")
        notify_admins_on_failure(f"Failed to update GitHub file with check: {str(e)}")
        return False


def show_file_content():
    try:
        file_content = get_github_file()
        if file_content:
            decoded_content = base64.b64decode(file_content['content']).decode()
            return decoded_content
        else:
            log_event("Failed to get file content")
            return "Error In Get File Content"
    except Exception as e:
        log_event(f"Exception in show_file_content: {str(e)}")
        notify_admins_on_failure(f"Failed to show file content: {str(e)}")
        return "Error In Get File Content"


def clear_file():
    try:
        # أولاً، حذف جميع الوثائق من مجموعة 'subscriptions' في Firebase
        docs = db.collection('subscriptions').stream()
        for doc in docs:
            db.collection('subscriptions').document(doc.id).delete()

        # ثم مسح الملف في GitHub
        return update_github_file("")
    except Exception as e:
        log_event(f"Exception in clear_file: {str(e)}")
        notify_admins_on_failure(f"Failed to clear file in GitHub or Firebase: {str(e)}")
        return False



def add_subscription_to_firebase(user_id, duration, unit):
    try:
        now = datetime.now()
        if unit == 'minute':
            expiration_date = now + timedelta(minutes=duration)
        elif unit == 'hour':
            expiration_date = now + timedelta(hours=duration)
        elif unit == 'day':
            expiration_date = now + timedelta(days=duration)
        else:
            log_event(f"Invalid time unit: {unit}")
            return False

        expiration_date_str = expiration_date.strftime("%Y-%m-%d %H:%M:%S")
        db.collection('subscriptions').document(user_id).set({
            'expiration_date': expiration_date_str
        })
        log_event(f"Added subscription for user {user_id} with expiration date {expiration_date_str}")
        return True
    except Exception as e:
        log_event(f"Exception in add_subscription_to_firebase: {str(e)}")
        notify_admins_on_failure(f"Failed to add subscription: {str(e)}")
        return False


def remove_expired_subscriptions():
    try:
        now = datetime.now()
        docs = db.collection('subscriptions').stream()

        for doc in docs:
            expiration_date = datetime.strptime(doc.to_dict()['expiration_date'], "%Y-%m-%d %H:%M:%S")
            if now > expiration_date:
                id_to_remove = doc.id
                encoded_text_to_remove = encode_text(id_to_remove)

                file_content = get_github_file()
                if file_content:
                    decoded_content = base64.b64decode(file_content['content']).decode()
                    updated_content = "\n".join(
                        line for line in decoded_content.splitlines() if line != encoded_text_to_remove)
                    update_github_file(updated_content)

                db.collection('subscriptions').document(id_to_remove).delete()
                log_event(f"Removed expired subscription for user {id_to_remove}")
    except Exception as e:
        log_event(f"Exception in remove_expired_subscriptions: {str(e)}")
        notify_admins_on_failure(f"Failed to remove expired subscriptions: {str(e)}")


def notify_before_expiration():
    try:
        now = datetime.now()
        docs = db.collection('subscriptions').stream()

        for doc in docs:
            expiration_date = datetime.strptime(doc.to_dict()['expiration_date'], "%Y-%m-%d %H:%M:%S")
            if now + timedelta(hours=24) > expiration_date:
                id_to_notify = doc.id
                try:
                    bot.send_message(id_to_notify, "⏰ Your subscription will expire within 24 hours. Please renew it.")
                    log_event(f"Notification sent to {id_to_notify} about upcoming expiration")
                except telebot.apihelper.ApiTelegramException as e:
                    if e.result_json['description'] == "Bad Request: chat not found":
                        log_event(f"Failed to send message to {id_to_notify}: Chat not found.")
                    else:
                        raise e
    except Exception as e:
        log_event(f"Exception in notify_before_expiration: {str(e)}")
        notify_admins_on_failure(f"Failed to send expiration notifications: {str(e)}")


def get_subscriptions_from_firebase():
    try:
        docs = db.collection('subscriptions').stream()
        subscriptions = ""
        for doc in docs:
            subscriptions += f"{doc.id} - Expires at {doc.to_dict()['expiration_date']}\n"
        return subscriptions if subscriptions else "No active subscriptions"
    except Exception as e:
        log_event(f"Exception in get_subscriptions_from_firebase: {str(e)}")
        notify_admins_on_failure(f"Failed to get subscriptions: {str(e)}")
        return "Error fetching subscriptions"


def backup_data():
    try:
        content = show_file_content()
        backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(backup_path, 'w') as backup_file:
            backup_file.write(content)
        log_event(f"Backup created at {backup_path}")
        return True, backup_path
    except Exception as e:
        log_event(f"Exception in backup_data: {str(e)}")
        notify_admins_on_failure(f"Failed to create backup: {str(e)}")
        return False, None


def add_admin_to_firebase(user_id):
    try:
        db.collection('admins').document(str(user_id)).set({})
        log_event(f"Admin {user_id} added to Firebase successfully")
        return True
    except Exception as e:
        log_event(f"Exception in add_admin_to_firebase: {str(e)}")
        notify_admins_on_failure(f"Failed to add admin: {str(e)}")
        return False


def remove_admin_from_firebase(user_id):
    try:
        db.collection('admins').document(str(user_id)).delete()
        log_event(f"Admin {user_id} removed from Firebase successfully")
        return True
    except Exception as e:
        log_event(f"Exception in remove_admin_from_firebase: {str(e)}")
        notify_admins_on_failure(f"Failed to remove admin: {str(e)}")
        return False


def get_admins_from_firebase():
    try:
        docs = db.collection('admins').stream()
        admin_list = [doc.id for doc in docs]
        return admin_list
    except Exception as e:
        log_event(f"Exception in get_admins_from_firebase: {str(e)}")
        notify_admins_on_failure(f"Failed to get admins: {str(e)}")
        return []


def is_user_admin(user_id):
    admin_list = get_admins_from_firebase()
    return str(user_id) in admin_list

# إضافات جديدة لدعم اللغات المتعددة
def set_user_language(user_id, language):
    db.collection('users').document(str(user_id)).set({'language': language}, merge=True)

def get_user_language(user_id):
    doc = db.collection('users').document(str(user_id)).get()
    if doc.exists:
        return doc.to_dict().get('language', 'en')
    return 'en'

def is_valid_subscription(user_id):
    try:
        doc = db.collection('subscriptions').document(user_id).get()
        if doc.exists:
            expiration_date = datetime.strptime(doc.to_dict()['expiration_date'], "%Y-%m-%d %H:%M:%S")
            return datetime.now() < expiration_date
        return False
    except Exception as e:
        log_event(f"Exception in is_valid_subscription: {str(e)}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    
    # إنشاء لوحة مفاتيح لاختيار اللغة
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('English')
    btn2 = types.KeyboardButton('العربية')
    markup.add(btn1, btn2)
    
    welcome_text = "Please choose your language:\nيرجى اختيار لغتك:"
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['English', 'العربية'])
def handle_language_selection(message):
    chat_id = message.chat.id
    if message.text == 'English':
        set_user_language(chat_id, 'en')
        bot.reply_to(message, "Language set to English. Use /help to see available commands.")
    elif message.text == 'العربية':
        set_user_language(chat_id, 'ar')
        bot.reply_to(message, "تم تعيين اللغة إلى العربية. استخدم /help لعرض الأوامر المتاحة.")

@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    help_text = (
        "🤖 *Bot Commands*:\n\n"
        "🔹 /add `{user_id} {duration} {unit}` - Add a subscription for a user.\n"
        "🔹 /dele `{user_id}` - Delete a subscription.\n"
        "🔹 /enc `{text}` - Encode text.\n"
        "🔹 /show - Show all stored IDs.\n"
        "🔹 /clear - Clear all stored IDs.\n"
        "🔹 /check `{user_id}` - Check if a subscription is valid.\n"
        "🔹 /list - List all active subscriptions.\n"
        "🔹 /renew `{user_id} {duration} {unit}` - Renew a subscription.\n"
        "🔹 /info `{user_id}` - Show subscription information.\n\n"
        "👮‍♂️ *Admin Commands*:\n\n"
        "🔹 /add_admin `{user_id}` - Add a new admin.\n"
        "🔹 /remove_admin `{user_id}` - Remove an admin.\n"
        "🔹 /list_admins - List all admins.\n"
        "🔹 /backup - Create a backup of the ID file."
        if language == 'en'
        else
        "🤖 *أوامر البوت*:\n\n"
        "🔹 /add `{user_id} {duration} {unit}` - إضافة اشتراك لمستخدم.\n"
        "🔹 /dele `{user_id}` - حذف اشتراك.\n"
        "🔹 /enc `{text}` - تشفير نص.\n"
        "🔹 /show - عرض جميع المعرفات المخزنة.\n"
        "🔹 /clear - مسح جميع المعرفات المخزنة.\n"
        "🔹 /check `{user_id}` - التحقق من صلاحية اشتراك.\n"
        "🔹 /list - عرض جميع الاشتراكات النشطة.\n"
        "🔹 /renew `{user_id} {duration} {unit}` - تجديد اشتراك.\n"
        "🔹 /info `{user_id}` - عرض معلومات الاشتراك.\n\n"
        "👮‍♂️ *أوامر المديرين*:\n\n"
        "🔹 /add_admin `{user_id}` - إضافة مدير جديد.\n"
        "🔹 /remove_admin `{user_id}` - إزالة مدير.\n"
        "🔹 /list_admins - عرض جميع المديرين.\n"
        "🔹 /backup - إنشاء نسخة احتياطية من ملف المعرفات."
    )
    bot.send_message(chat_id, help_text, parse_mode='Markdown')


@bot.message_handler(commands=['add_admin', 'remove_admin', 'list_admins'])
def handle_admin_commands(message):
    chat_id = message.chat.id
    if not is_user_admin(chat_id):
        bot.reply_to(message, "❌ You are not authorized to perform this action." if get_user_language(chat_id) == 'en' else "❌ عذرًا، أنت غير مخول للقيام بهذا الإجراء.")
        return

    command = message.text.split()[0]

    if command == '/add_admin':
        try:
            new_admin_id = int(message.text.split()[1])
            if add_admin_to_firebase(new_admin_id):
                bot.reply_to(message, "✅ Admin added successfully!" if get_user_language(chat_id) == 'en' else "✅ تم إضافة المدير بنجاح!")
            else:
                bot.reply_to(message, "❌ Failed to add admin." if get_user_language(chat_id) == 'en' else "❌ فشل في إضافة المدير.")
        except IndexError:
            bot.reply_to(message, "Usage: /add_admin {admin_id}" if get_user_language(chat_id) == 'en' else "الاستخدام: /add_admin {معرف المدير}")
        except ValueError:
            bot.reply_to(message, "Invalid admin ID." if get_user_language(chat_id) == 'en' else "معرف المدير غير صالح.")

    elif command == '/remove_admin':
        try:
            remove_admin_id = int(message.text.split()[1])
            if remove_admin_from_firebase(remove_admin_id):
                bot.reply_to(message, "✅ Admin removed successfully!" if get_user_language(chat_id) == 'en' else "✅ تم إزالة المدير بنجاح!")
            else:
                bot.reply_to(message, "❌ Failed to remove admin." if get_user_language(chat_id) == 'en' else "❌ فشل في إزالة المدير.")
        except IndexError:
            bot.reply_to(message, "Usage: /remove_admin {admin_id}" if get_user_language(chat_id) == 'en' else "الاستخدام: /remove_admin {معرف المدير}")
        except ValueError:
            bot.reply_to(message, "Invalid admin ID." if get_user_language(chat_id) == 'en' else "معرف المدير غير صالح.")

    elif command == '/list_admins':
        admin_list = get_admins_from_firebase()
        if admin_list:
            admin_list_str = "\n".join(admin_list)
            bot.reply_to(message, f"👮‍♂️ Current admins:\n{admin_list_str}" if get_user_language(chat_id) == 'en' else f"👮‍♂️ المديرون الحاليون:\n{admin_list_str}")
        else:
            bot.reply_to(message, "No admins found." if get_user_language(chat_id) == 'en' else "لم يتم العثور على أي مديرين.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = get_user_language(chat_id)

    if not is_user_admin(chat_id):
        bot.reply_to(message,
                     "❌ You are not in the admin list." if language == 'en' else "❌ عذرًا، أنت لست في قائمة المديرين.")
        return

    remove_expired_subscriptions()

    text = mes
