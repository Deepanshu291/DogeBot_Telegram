import requests
from aiogram  import *
from aiogram.types import *
import pytube as pt
import os
import shutil

token = "5799520080:AAEoTbfH987-lrIBG0yO45S--wLnWDXjcdU"

bot = Bot(token=token)
dp = Dispatcher(bot)
url2 = "https://meme-api.herokuapp.com/gimme"
# dp =  json.load(url)

class Ytube:
    url = " "
    
    def Downloder(self):
        ytube = pt.YouTube(url=self.url) 
        vid = ytube.streams.get_highest_resolution().download(output_path="./data", filename="video.mp4")
        aud = ytube.streams.get_audio_only().download(output_path="./data", filename="song.mp4")
    # def audDown(self):
    #     ytube = pt.YouTube(url=self.url)
    #     aud = ytube.streams.get_audio_only().download(output_path="./data", filename="song.mp4")
    def title(self):
        ytube = pt.YouTube(url=self.url)
        return ytube.title
    def thumnail(self):
        ytube = pt.YouTube(url=self.url)
        return ytube.thumbnail_url
    def fileh(self):
        if os.path.exists("data"):
            shutil.rmtree("data")
        else:    
            os.makedirs(name="data")

p= Ytube()
p.fileh()
bt1 = InlineKeyboardButton(text="Download Audio", callback_data="audDown")
bt2 = InlineKeyboardButton(text="Download Video", callback_data="vidDown")

kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add("😉😝MEMES").add("🔢Whatsapp link to Instant Chat").add("📽️Youtube Video Download").add("🌆Image Enchancement","🔃Restart")
lb1 = InlineKeyboardMarkup().add(bt1,bt2)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f" Hi {message.from_user.full_name}😄 \n\nChoose any one of the Option👇👇👇👇" , reply_markup=kb1)

@dp.message_handler(commands="vl")
async def wblink(msg: types.Message):
    p.fileh()
    url = (msg.text).split('/vl')[1]
    p.url = url
    p.audDown()
    await msg.answer_photo(p.thumnail(), caption=p.title() , reply_markup=lb1)
 
@dp.callback_query_handler(text = ["vidDown", "audDown","more"])
async def downloader(call: types.CallbackQuery):
   
    if call.data == "vidDown":
         f = open("./data/video.mp4","rb")
         await call.message.reply_video(video=f, caption=p.title())
    elif call.data == "audDown":
        f = open("./data/song.mp4","rb")
        await call.message.reply_audio(audio=f, title=p.title(),caption=p.title()) 
    elif call.data == "more":
        res = requests.get(url2)
        dt = res.json()
        await call.message.answer_photo(dt["url"], reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton( text="Want More Memes",callback_data="more")))
    f.close()    
         
    
@dp.message_handler()
async def chat(msg: types.Message):
    if msg.text == "🔢Whatsapp link to Instant Chat":
        await msg.answer("Type Your Whatsapp No \n as  9889xxxxx ")
    elif msg.text.isnumeric():
        phoneno = msg.text
        await msg.answer(parse_mode="Markdown", text=f" [{phoneno} open in Whatsapp ](https://wa.me/91{phoneno})")
    elif msg.text == "😉😝MEMES":
        res = requests.get(url2)
        dt = res.json()
        await msg.answer_photo(dt["url"], reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton( text="Want More Memes",callback_data="more")))
    elif msg.text == "🔃Restart":
        # await msg.delete
        await msg.answer(reply_markup=kb1)
    elif  msg.text =="📽️Youtube Video Download":
        if p.url == " ":
            await msg.answer("Please Forward link of youtube video")
        else:
            await msg.answer_photo(p.thumnail(), caption=p.title() , reply_markup=lb1)
    elif "https" in msg.text:
        # p.fileh()
        p.url = msg.text
        p.Downloder()
        await msg.answer_photo(p.thumnail(), caption=p.title() , reply_markup=lb1)
      
        
        
print("I am Live")        
executor.start_polling(dp)
