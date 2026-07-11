from seleniumbase import Driver
from selenium.webdriver.common.by import By
from config import MAX_COMMENT_CHAR,NUMBER_OF_COMMENTS,SUBREDDIT,IMAGES,AUDIOS
from random import randint
from tiktok_voice import tts,Voice

class DataScraper:
    def __init__(self):
        self.driver = Driver(uc=True, browser="brave")

    def get_url(self):
        combined_url:str=f'https://www.reddit.com/r/{SUBREDDIT}/hot/'
        return combined_url

    def initiate_website_connection(self,url:str):
        self.driver.get(url=url)
        if self.driver.is_element_visible(By.TAG_NAME,'shreddit-post'):
            
            posts=self.driver.find_elements(By.TAG_NAME,'shreddit-post')

            randomizer:int=randint(0,len(posts))
            posts[randomizer].uc_click()

            post_title=self.grab_post_title()

            self.screenshot_post_question()
            self.transcribe_post_title_text(post_title)

            comment_list:list=self.driver.find_elements('shreddit-comment')

            self.transcribe_comment_text(comments=comment_list)

            

    def transcribe_comment_text(self,comments:list):
        cleaned_comment_list:list=[]
        for i,comment in enumerate(comments):
            comment=comment.find_element(By.TAG_NAME,'p')
            if len(comment.text) < MAX_COMMENT_CHAR and len(cleaned_comment_list) >= NUMBER_OF_COMMENTS :
                comment.screenshot(fr'{IMAGES}/shot{i+1}.png')
                tts(comment.text,voice=Voice.US_MALE_1,output_file_path=fr'{AUDIOS}/audio{i+1}.mp3')

    
    def transcribe_post_title_text(self,text:str):
        tts(text=text,voice=Voice.US_MALE_1,output_file_path=fr'{AUDIOS}/audio0.mp3')

    def screenshot_post_question(self):
        post_main_frame=self.driver.find_element(By.TAG_NAME,'shreddit-post')
        post_main_frame.screenshot(fr'{IMAGES}/shot0.png')

    def grab_post_title(self):
        post_title:str=self.driver.find_element(By.TAG_NAME,'h1').text
        return post_title

if __name__ == "__main__":
    scraper = DataScraper()
    response_url=scraper.get_url()
    scraper.initiate_website_connection(url=response_url)