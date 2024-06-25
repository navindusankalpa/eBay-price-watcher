import asyncio
from pathlib import Path
from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.foundation import IPropertyValue
from winsdk.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    NotificationData,
    ToastActivatedEventArgs,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)

DEFAULT_APP_ID = 'ebay-scraper'

xml = """
<toast activationType="protocol" launch="http:" scenario="{scenario}">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
"""


def set_attribute(document, xpath, name, value):
    attribute = document.create_attribute(name)
    attribute.value = value
    document.select_single_node(xpath).attributes.set_named_item(attribute)


def add_text(msg, document):
    if isinstance(msg, str):
        msg = {
            'text': msg
        }
    binding = document.select_single_node('//binding')
    text = document.create_element('text')
    for name, value in msg.items():
        if name == 'text':
            text.inner_text = msg['text']
        else:
            text.set_attribute(name, value)
    binding.append_child(text)


def add_icon(icon, document):
    if isinstance(icon, str):
        icon = {
            'placement': 'appLogoOverride',
            'hint-crop': 'circle',
            'src': icon
        }
    binding = document.select_single_node('//binding')
    image = document.create_element('image')
    for name, value in icon.items():
        image.set_attribute(name, value)
    binding.append_child(image)


def add_audio(aud, document):
    if isinstance(aud, str):
        aud = {
            'src': aud
        }
    toast = document.select_single_node('/toast')
    audio = document.create_element('audio')
    for name, value in aud.items():
        audio.set_attribute(name, value)
    toast.append_child(audio)


def create_actions(document):
    toast = document.select_single_node('/toast')
    actions = document.create_element('actions')
    toast.append_child(actions)
    return actions


def add_button(button, document):
    if isinstance(button, str):
        button = {
            'activationType': 'protocol',
            'arguments': 'http:' + button,
            'content': button
        }
    actions = document.select_single_node(
        '//actions') or create_actions(document)
    action = document.create_element('action')
    for name, value in button.items():
        action.set_attribute(name, value)
    actions.append_child(action)


def result_wrapper(*args):
    global result
    result = args
    return result

def activated_args(_, event):
    global result
    e = ToastActivatedEventArgs._from(event)
    user_input = dict([(name, IPropertyValue._from(
        e.user_input[name]).get_string()) for name in e.user_input])
    result = {
        'arguments': e.arguments,
        'user_input': user_input
    }
    return result


async def play_sound(audio):
    from winsdk.windows.media.core import MediaSource
    from winsdk.windows.media.playback import MediaPlayer

    if audio.startswith('http'):
        from winsdk.windows.foundation import Uri
        source = MediaSource.create_from_uri(Uri(audio))
    else:
        from winsdk.windows.storage import StorageFile
        file = await StorageFile.get_file_from_path_async(audio)
        source = MediaSource.create_from_storage_file(file)

    player = MediaPlayer()
    player.source = source
    player.play()
    await asyncio.sleep(7)


def notify(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, dialogue=None, duration=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml, app_id=DEFAULT_APP_ID, scenario=None, tag=None, group=None):
    document = XmlDocument()
    document.load_xml(xml.format(scenario=scenario if scenario else 'default'))
    if isinstance(on_click, str):
        set_attribute(document, '/toast', 'launch', on_click)

    if duration:
        set_attribute(document, '/toast', 'duration', duration)

    if title:
        add_text(title, document)
    if body:
        add_text(body, document)
    if input:
        pass
    if inputs:
        pass
    if selection:
        pass
    if selections:
        pass
    if button:
        add_button(button, document)
    if buttons:
        for button in buttons:
            add_button(button, document)
    if icon:
        add_icon(icon, document)
    if audio:
        if isinstance(audio, str) and audio.startswith('ms'):
            add_audio(audio, document)
        elif isinstance(audio, str):
            path = Path(audio)
            if path.is_file():
                add_audio(f"file:///{path.absolute().as_posix()}", document)
        elif isinstance(audio, dict) and 'src' in audio and audio['src'].startswith('ms'):
            add_audio(audio, document)
        else:
            add_audio({'silent': 'true'}, document)
    if dialogue:
        add_audio({'silent': 'true'}, document)

    notification = ToastNotification(document)
    if progress:
        data = NotificationData()
        for name, value in progress.items():
            data.values[name] = str(value)
        data.sequence_number = 1
        notification.data = data
        notification.tag = 'my_tag'
    if tag:
        notification.tag = tag
    if group:
        notification.group = group
    if app_id == DEFAULT_APP_ID:
        try:
            notifier = ToastNotificationManager.create_toast_notifier()
        except Exception as e:
            notifier = ToastNotificationManager.create_toast_notifier(app_id)
    else:
        notifier = ToastNotificationManager.create_toast_notifier(app_id)
    notifier.show(notification)
    return notification


async def toast_async(title=None, body=None, on_click=print, icon=None, image=None, progress=None, audio=None, dialogue=None, duration=None, input=None, inputs=[], selection=None, selections=[], button=None, buttons=[], xml=xml, app_id=DEFAULT_APP_ID, ocr=None, on_dismissed=print, on_failed=print, scenario=None, tag=None, group=None):
    """
    Notify
    Args:
        title: <str>
        body: <str>
        on_click: <function>
        on_dismissed: <function>
        on_failed: <function>
        inputs: <list<str>> ['textbox']
        selections: <list<str>> ['Apple', 'Banana', 'Grape']
        actions: <list<str>> ['Button']
        icon: <str> https://unsplash.it/64?image=669
        image: <str> https://4.bp.blogspot.com/-u-uyq3FEqeY/UkJLl773BHI/AAAAAAAAYPQ/7bY05EeF1oI/s800/cooking_toaster.png
        audio: <str> ms-winsoundevent:Notification.Looping.Alarm
        xml: <str>

    Returns:
        None
    """
    if ocr:
        title = 'OCR Result'
        src = ocr if isinstance(ocr, str) else ocr['ocr']
        image = {'placement': 'hero', 'src': src}
    notification = notify(title, body, on_click, icon, image,
                          progress, audio, dialogue, duration, input, inputs, selection, selections, button, buttons, xml, app_id, scenario, tag, group)
    loop = asyncio.get_running_loop()
    futures = []

    if audio and isinstance(audio, str) and not audio.startswith('ms'):
        futures.append(loop.create_task(play_sound(audio)))
    if dialogue:
        pass
        #futures.append(loop.create_task(speak(dialogue)))

    if isinstance(on_click, str):
        on_click = print
    activated_future = loop.create_future()
    activated_token = notification.add_activated(
        lambda *args: loop.call_soon_threadsafe(
            activated_future.set_result, on_click(activated_args(*args))
        )
    )
    futures.append(activated_future)

    dismissed_future = loop.create_future()
    dismissed_token = notification.add_dismissed(
        lambda _, event_args: loop.call_soon_threadsafe(
            dismissed_future.set_result, on_dismissed(result_wrapper(ToastDismissedEventArgs._from(event_args).reason)))
    )
    futures.append(dismissed_future)

    failed_future = loop.create_future()
    failed_token = notification.add_failed(
        lambda _, event_args: loop.call_soon_threadsafe(
            failed_future.set_result, on_failed(result_wrapper(ToastFailedEventArgs._from(event_args).error_code)))
    )
    futures.append(failed_future)

    try:
        _, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    finally:
        if activated_token is not None:
            notification.remove_activated(activated_token)
        if dismissed_token is not None:
            notification.remove_dismissed(dismissed_token)
        if failed_token is not None:
            notification.remove_failed(failed_token)
        return result