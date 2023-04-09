import requests
from aiogram  import *
from aiogram.types import *
import pytube as pt
import os
import io
import shutil
import time
from rembg import remove
from PIL import Image

token = "5421069203:AAFfrwK4v58x-7N4cmhcGa9i6_wLoYUnz8M"

bot = Bot(token=token)
dp = Dispatcher(bot)
url2 = "https://meme-api.com/gimme"
# dp =  json.load(url)

class Ytube:
    url = " "
    username = " "
    vidpath = " "
    audpath= " "
    #video details :-
    thumb_url = " "
    desc = " "
    duration = " "
    author = " "
    metadata = " "
    title = " "
    imgurl = " "
    # ----------
    aichat = False
    def Downloder(self):
        ytube = pt.YouTube(url=self.url)
        self.title = ytube.title
        self.metadata= ytube.metadata
        self.thumb_url =  ytube.thumbnail_url
        self.desc = ytube.description
        self.duration = ytube.length
        self.author = ytube.author

        # self.vidpath = ytube.streams.get_highest_resolution().download(output_path="./data",)
        self.audpath = ytube.streams.get_audio_only().download(output_path="./data")
        print(self.audpath,self.vidpath, self.thumb_url)
    # def audDown(self):
    #     ytube = pt.YouTube(url=self.url)
    #     aud = ytube.streams.get_audio_only().download(output_path="./data", filename="song.mp4")
    def title(self):
        ytube = pt.YouTube(url=self.url)
        self.metadata= ytube.metadata
        self.thumb_url =  ytube.thumbnail_url
        self.desc = ytube.description
        self.duration = ytube.length
        self.author = ytube.author
        
    def thumnail(self):
        ytube = pt.YouTube(url=self.url)
        return ytube.thumbnail_url 
    
    def fileh(self):
        if os.path.exists("data"):
            shutil.rmtree("data")
        else:
            os.makedirs(name="data")
    def AIbot(self, msg):
        # print(msg)
        url = f"https://v6.rsa-api.xyz/ai/response?user_id=420&message={msg}"
         # querystring = {f"message": "{msg}"}
        headers = {
             'Authorization': 'Qgy5DMPfjnYX'
           }
        response = requests.request("GET", url, headers=headers,)
        r = response.text
        r = r.split('"message":"')
        r = r[1]
        r = r.split('","warning')
        r = r[0]
        r = r.replace('"}', '')
        # print(r)
        return r

p= Ytube()
p.fileh()
audio_download = InlineKeyboardButton(text="Download Audio", callback_data="audDown")
video_download = InlineKeyboardButton(text="Download Video", callback_data="vidDown")



kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add("😉😝MEMES","▶️Start AI Chat").add("🔢Whatsapp link to Instant Chat").add("📽️Youtube Video Download")
kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add("⏹️Stop AI Chat")
kb3 = ReplyKeyboardMarkup(resize_keyboard=True).add("⏹️Stop AI Image Enchancement")
lb1 = InlineKeyboardMarkup().add(audio_download,video_download)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    p.username = message.from_user.username
    await message.answer(f" Hi {message.from_user.full_name}😄 \n\nChoose any one of the Option👇👇👇👇" , reply_markup=kb1)

@dp.message_handler(commands="vl")
async def wblink(msg: types.Message):
    p.fileh()
    url = (msg.text).split('/vl')[1]
    p.url = url
    p.audDown()
    await msg.answer_photo(p.thumnail(), caption=p.title() , reply_markup=lb1)

@dp.callback_query_handler(text = ["vidDown", "audDown","more","bgrem"])
async def downloader(call: types.CallbackQuery):

    if call.data == "vidDown":
        f = open("./data/video.mp4","rb")
        await call.message.reply_video(video=f, caption=p.title())
    elif call.data == "audDown":
        # f = open("./data/song.mp4","rb")
        f = open(p.audpath, "rb")
        await call.message.reply_audio(audio=f,  title=p.title,caption=p.title ,  thumb=p.thumb_url ,performer=p.author , duration= p.duration)
    elif call.data == "more":
        res = requests.get(url2)
        dt = res.json()
        await call.message.answer_photo(dt["url"], reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton( text="Want More Memes",callback_data="more")))
    elif call.data == "bgrem":
        url = p.imgurl
        print(url)
        img = Image.open(requests.get(url,stream=True).raw)
        rmbg = remove(img)
        rmbg.save('output.png')
        f = open('./output.png', "rb")
        await call.message.reply_photo(photo=f)
        os.remove('output.png')
    f.close()

@dp.message_handler(content_types=['photo', 'document'])
async def get_file(msg: types.Message):
    ctfile = msg.content_type
    des=r"C:\\Users\\Deepanshu\\Desktop\\New folder\\Telegram Bot\\DogeBot\\media"
    if ctfile == "document":
        # await msg.document.download(destination_dir=des)
        imgpath =   await msg.document.download()
        await msg.reply("file uploaded...")
    elif ctfile == "photo":
        # imgpath = await msg.photo[-1].download()
        imgurl = await msg.photo[-1].get_url()
        p.imgurl = imgurl  
        await msg.reply("Picture uploaded...",reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Remove Background", callback_data="bgrem")))

@dp.message_handler()
async def chat(msg: types.Message):
    # print(files.file_id)
    if p.aichat == True:
        res= p.AIbot(msg=msg.text)
        await msg.answer(text=res)
    if msg.text == "🔢Whatsapp link to Instant Chat":
        await msg.answer("Type Your Whatsapp No \n as  9889xxxxx ")
    # elif msg.content_type == 'document':
    #     await msg.document.download(destination_dir=r"C:\\Users\\Deepanshu\\Desktop\\New folder\\Telegram Bot\\DogeBot\\media")
    #     await msg.reply("file uploaded...")
    #     # print(files.file_id)
    #     # await bot.download_file(destination_dir="/media", file_path=msg.document)
    #     # dcpath =  doc.get_file()
    #     # fpath = files.get_file()
    #     # print(dcpath, fpath)
    elif msg.text.isnumeric():
        phoneno = msg.text
        await msg.answer(parse_mode="Markdown", text=f" [{phoneno}]" ,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton( text="Open in Whatsapp", url=f"https://wa.me/91{phoneno}")) )
    elif msg.text == "😉😝MEMES":
        res = requests.get(url2)
        dt = res.json()
        await msg.answer_photo(dt["url"], reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton( text="Want More Memes",callback_data="more")))
    elif msg.text == "▶️Start AI Chat":
        p.aichat = True
        await msg.answer(reply_markup=kb2,text="AI Chat Start now you can chat\n and want to stop so press stop AI Chat")
    elif msg.text == "⏹️Stop AI Chat":
        p.aichat =False
        await msg.answer(reply_markup=kb1, text="Bye Nice to meet you😄")
    elif msg.text == "🌆Image Enchancement":
        p.removeimg = True
    # elif msg.text == ""
    elif  msg.text =="📽️Youtube Video Download":

        #if p.url == " ":
        await msg.answer("Please Forward link of youtube video")
        time.sleep(10)
        p.fileh()
 # else:
         #   await msg.answer_photo(p.thumnail(), caption=p.title() , reply_markup=lb1)
    elif "https" in msg.text:
        # p.fileh()
        p.url = msg.text
        # p.fpath = f"{p.title()}."
        p.Downloder()
        await msg.answer_photo(p.thumb_url, caption=p.title , reply_markup=lb1)



print("I am Live")
executor.start_polling(dp)