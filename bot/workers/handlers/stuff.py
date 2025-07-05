import os
import shutil
import time

import psutil

from bot import Button, botStartTime, dt, subprocess, version_file
from bot.config import _bot, conf
from bot.fun.emojis import enmoji
from bot.utils.bot_utils import add_temp_user, get_readable_file_size, rm_temp_user
from bot.utils.bot_utils import time_formatter as tf
from bot.utils.db_utils import save2db2
from bot.utils.msg_utils import (
    edit_message,
    pm_is_allowed,
    reply_message,
    temp_is_allowed,
    user_is_allowed,
    user_is_owner,
)
from bot.utils.os_utils import file_exists


async def up(event, args, client):
    """ping bot!"""
    if not user_is_allowed(event.sender_id):
        return await event.delete()
    ist = dt.now()
    msg = await reply_message(event, "…")
    st = dt.now()
    ims = (st - ist).microseconds / 1000
    msg1 = "**Pong! ——** `{}`__ms__"
    st = dt.now()
    await edit_message(msg, msg1.format(ims))
    ed = dt.now()
    ms = (ed - st).microseconds / 1000
    await edit_message(msg, f"1. {msg1.format(ims)}\n2. {msg1.format(ms)}")


async def status(event, args, client):
    """Gets status of bot and server where bot is hosted.
    Requires no arguments."""
    if not user_is_allowed(event.sender_id):
        return await event.delete()
    branch = _bot.repo_branch or "❓"
    last_commit = "UNAVAILABLE!"
    if os.path.exists(".git"):
        try:
            last_commit = subprocess.check_output(
                ["git log -1 --date=short --pretty=format:'%cd || %cr'"], shell=True
            ).decode()
        except Exception:
            pass

    if file_exists(version_file):
        with open(version_file, "r") as file:
            vercheck = file.read().strip()
            file.close()
    else:
        vercheck = "Tf?"
    currentTime = tf(time.time() - botStartTime)
    ostime = tf(time.time() - psutil.boot_time())
    swap = psutil.swap_memory()
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    p_cores = psutil.cpu_count(logical=False)
    t_cores = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/").percent
    await event.reply(
        f"**Version:** `{vercheck}`\n"
        f"**Branch:** `{branch}`\n"
        f"**Commit Date:** `{last_commit}`\n\n"
        f"**Docker:** `{'Yes' if _bot.docker_deployed else 'No'}`\n"
        f"**Bot Uptime:** `{currentTime}`\n"
        f"**System Uptime:** `{ostime}`\n\n"
        f"**Total Disk Space:** `{total}`\n"
        f"**Used:** `{used}` "
        f"**Free:** `{free}`\n\n"
        f"**SWAP:** `{get_readable_file_size(swap.total)}`"
        f"** | **"
        f"**Used:** `{swap.percent}%`\n\n"
        f"**Upload:** `{sent}`\n"
        f"**Download:** `{recv}`\n\n"
        f"**Physical Cores:** `{p_cores}`\n"
        f"**Total Cores:** `{t_cores}`\n\n"
        f"**CPU:** `{cpuUsage}%` "
        f"**RAM:** `{memory.percent}%` "
        f"**DISK:** `{disk}%`\n\n"
        f"**Total RAM:** `{get_readable_file_size(memory.total)}`\n"
        f"**Used:** `{get_readable_file_size(memory.used)}` "
        f"**Free:** `{get_readable_file_size(memory.available)}`"
    )


async def start(event, args, client):
    """A function for the start command, accepts no arguments yet!"""
    currentTime = tf(time.time() - botStartTime)
    msg = ""
    msg1 = f"Hi `{event.sender.first_name}`\n"
    msg2 = (
        f"{msg1}I've been alive for `{currentTime}` and i'm ready to encode videos 😗"
    )
    msg3 = f"{msg2}\nand by the way you're a temporary user"
    user = event.sender_id
    if not user_is_owner(user) and event.is_private:
        if not pm_is_allowed(in_pm=True):
            return await event.delete()
    if temp_is_allowed(user):
        msg = msg3
    elif not user_is_allowed(user):
        priv = await event.client.get_entity(int(conf.OWNER.split()[0]))
        msg = f"{msg1}You're not allowed access to this bot"
        msg += f"\nAsk [{priv.first_name}](tg://user?id={conf.OWNER.split()[0]}) "
        msg += "(nicely) to grant you access."

    if not msg:
        msg = msg2
    await event.reply(
        msg,
        buttons=[
            [Button.inline("Container Code", data="ihelp")],
            [Button.url("Image Maintainer", url="t.me/SamXD7")],
        ],
    )


async def help(event, args, client):
    return await start(event, args, client)


async def ihelp(event):
    await event.edit(
        """`
FROM encodev/svtav1enc:hdr

WORKDIR /bot
RUN chmod -R 777 /usr /bot

COPY .env .

CMD ["bash", "run.sh"]`
        """,
        buttons=[
            [Button.inline(".env", data="icommands")],
            [Button.inline("🔙 Back", data="beck")],
        ],
    )


async def beck(event):
    sender = event.query.user_id
    currentTime = tf(time.time() - botStartTime)
    msg = ""
    msg1 = f"Hi `{event.sender.first_name}`\n"
    msg2 = (
        f"{msg1}I've been alive for `{currentTime}` and i'm ready to encode videos 😗"
    )
    msg3 = f"{msg2}\nand by the way you're a temporary user"
    if temp_is_allowed(sender):
        msg = msg3
    elif not user_is_allowed(sender):
        priv = await event.client.get_entity(int(conf.OWNER.split()[0]))
        msg = f"{msg1}You're not allowed access to this bot"
        msg += f"\nAsk [{priv.first_name}](tg://user?id={conf.OWNER.split()[0]}) "
        msg += "(nicely) to grant you access."
    if not msg:
        msg = msg2
    await event.edit(
        msg,
        buttons=[
            [Button.inline("Container Code", data="ihelp")],
            [Button.url("Image Maintainer", url="t.me/SamXD7")],
        ],
    )


async def temp_unauth(event, args, client):
    """
    Un-authorise a user or chat
    Requires either reply to message or user_id as args
    """
    sender = event.sender_id
    error = "Failed!,\nCan't remove from temporarily allowed users"
    if not user_is_owner(sender):
        return event.reply("Not Happening.")
    if event.is_reply:
        rep_event = await event.get_reply_message()
        new_id = rep_event.sender_id
    else:
        if args is not None:
            args = args.strip()
            if args.lstrip("-").isdigit():
                new_id = int(args)
            else:
                return await event.reply(
                    f"What do you mean by  `{args}` ?\nneed help? send /unpermit"
                )
        else:
            return await event.reply(
                "Either reply to a message sent by the user you want to remove from temporarily allowed users or send /unpermit (user-id)\nExample:\n  /unpermit 123456"
            )
    if new_id == sender:
        return await event.reply("Why, oh why did you try to unpermit yourself?")
    if user_is_owner(new_id):
        return await event.reply(f"{error} because user is already a privileged user")
    if not user_is_allowed(new_id):
        return await event.reply(
            f"{error} because user is not in the temporary allowed user list"
        )
    try:
        new_user = await event.client.get_entity(new_id)
        new_user = new_user.first_name
    except Exception:
        new_user = new_id
    rm_temp_user(str(new_id))
    await save2db2()
    return await event.reply(
        f"Removed `{new_user}` from temporarily allowed users {enmoji()}"
    )


async def temp_auth(event, args, client):
    """
    Authorizes a chat or user,
    Requires either a reply to message or user_id as argument
    """
    sender = event.sender_id
    error = "Failed!,\nCan't add to temporarily allowed users"
    if not user_is_owner(sender):
        return event.reply("Nope, not happening.")
    if event.is_reply:
        rep_event = await event.get_reply_message()
        new_id = rep_event.sender_id
    else:
        if args is not None:
            args = args.strip()
            if args.lstrip("-").isdigit():
                new_id = args
            else:
                return await event.reply(
                    f"What do you mean by  `{args}` ?\nneed help? send /permit"
                )
        else:
            return await event.reply(
                "Either reply to a message sent by the user you want to add to temporarily allowed users or send /permit (user-id)\nExample:\n  /permit 123456"
            )
    new_id = int(new_id)
    if new_id == sender:
        return await event.reply("Why, oh why did you try to permit yourself?")
    if user_is_owner(new_id):
        return await event.reply(f"{error} because user is already a privileged user")
    if user_is_allowed(new_id):
        return await event.reply(f"{error} because user is already added")
    try:
        new_user = await event.client.get_entity(new_id)
        new_user = new_user.first_name
    except Exception:
        new_user = new_id
    add_temp_user(str(new_id))
    await save2db2()
    return await event.reply(
        f"Added `{new_user}` to temporarily allowed users {enmoji()}"
    )


async def icommands(event):
    conf.CMD_SUFFIX or str()
    await event.edit(
        """`
# Don't use quotes( " and ' )

APP_ID=
API_HASH=
BOT_TOKEN=
OWNER=

# [OPTIONAL]
# Uncomment (remove the '#') the below variables before adding their values

#FFMPEG=
#Encode commands to execute in sequence
#FFMPEG2=
#FFMPEG3=
#FFMPEG4=

#MUX_ARGS=  #arguements passed to ffmpeg to mux encoded content.

#TEMP_USERS
#THUMBNAIL=
#CACHE_DL=
#ENCODER=
#LOG_CHANNEL=
#LOGS_IN_CHANNEL=True   #Automatically dumps error in channels
#DBNAME=
#DATABASE_URL=
#CMD_SUFFIX=
#CUSTOM_RENAME=
#FILENAME_AS_CAPTION=
#FLOOD_SLEEP_THRESHOLD=

# Number of pyrogram event workers; if you want to always queue videos as sent set to 1
#WORKERS=1

# list of links separated by commas to download on startup
#DL_STUFF=

# Channel id , message id, sticker id , Bool, codec name (and quality) for forward channel
#FCHANNEL=
#FCHANNEL_STAT=
#FSTICKER=
#FBANNER=True #Increases the frequency of banner messages in forward channels
#FCODEC=
#NO_BANNER=True #Disables banner messages for forward channel 

# Channel short link
#C_LINK=

# Emoji or other beautifier to be added before captions
#CAP_DECO=

# Enable logging to log channel // off by default set value to True to enable 
#LOGS_IN_CHANNEL=

# Release Name
#RELEASER=

# Enable dumping leeched videos to bot pm and log_channel if available // On by default set value to False to disable 
#DUMP_LEECH=
#DUMP_CHANNEL= # Channel/Group id to dump leeched videos

# Always deploy latest version of repo during startup // Off by default set to True to enable 
#ALWAYS_DEPLOY_LATEST=

# Lock encoding on startup
#LOCK_ON_STARTUP=

# Enable encoding chat action in bot // on by default…
#ALLOW_ACTION=

# if not added defaults to original repo
#UPSTREAM_REPO=
#UPSTREAM_BRANCH=

#Aria2 & Qbit port
#ARIA2_PORT=
#QBIT_PORT=

# Force timeout long downloads in seconds
#ARIA2_DL_TIMEOUT=
#QBIT_DL_TIMEOUT=

#Telegraph
#TELEGRAPH_API=
#TELEGRAPH_AUTHOR=

# Report failed processes
#REPORT_FAILED=   #change to False to allow the two variables below 
#REPORT_FAILED_DL=
#REPORT_FAILED_ENC= 

#PODI=False  #Bot will no longer keep dl paused while in download info

#RSS
#RSS_CHAT=
#RSS_DELAY=
#RSS_DIRECT=

#USE_ANILIST=False #Disables Anilist
#USE_CAPTION=False #Disables treating captions without newlines as filenames

#UPLOAD_AS_VIDEO=True
#UPLOAD_VIDEO_AS_SPOILER=True`
        """,
        buttons=[Button.inline("🔙 Back", data="ihelp")],
    )
