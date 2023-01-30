# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================
# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object
                
        guid (string): A globally unique identifier for this news story
        title (string): The news story's headline
        description (string): A paragraph or so summarizing the news story
        link (string): A link to a website with the entire story
        pubdate (datetime): Date the news was published

        A NewsStory object has five attributes:
        self._guid (string, determined by input text)
        self._title (string, determined by input text)
        self._description (string, determined by input text)
        self._link (string, determined by input text)
        self._pubdate (datetime, determined by input text)
        '''

        self._guid = guid
        self._title = title
        self._description = description
        self._link = link
        self._pubdate = pubdate
        
    def get_guid(self):
        return self._guid
    
    def get_title(self):
        return self._title
    
    def get_description(self):
        return self._description
    
    def get_link(self):
        return self._link
    
    def get_pubdate(self):
        return self._pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object
                
        phrase (string): one or more words separated by a single space between the words.
        assume phrase does not contain punctuation

        A PhraseTrigger object inherits from Trigger has two attributes:
            self._phrase (string, determined by input text)
            self.is_phrase_in (boolean, determined using helper function is_phrase_in)
        '''
        
        super().__init__()
        self._phrase = phrase
        ##implement by trigger.evaluate(NewsStory)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        if self.is_phrase_in(story): 
            return True
        else:
            return False
        
    def get_phrase(self):
        return self._phrase
    
    def is_phrase_in(self, text):
        '''
        text (string): message string comparison
        
        Returns: True if the whole phrase is present in text, False otherwise,
        '''
        
        #phrase -> lowercase
        test_phrase = self.get_phrase()
        _lowercase_phrase = test_phrase.lower()
        
        #break phrase into words on white space
        #store each discrete word in a list phrase_list
        _phrase_words =_lowercase_phrase.split() #splits string into list where each word is an item
        

        #phrases are case agnostic
        _lowercase_text = text.lower()
        #break text into words on the white space or punctionation
        #replace all punctionation in string with white space
        for char in _lowercase_text: 
            if char in string.punctuation:
                _lowercase_text = _lowercase_text.replace(char, " ")
        #store each discrete word in a list text_list
        _text_words = _lowercase_text.split()
        
        #loop through word in passed in text
        for word in _text_words: 
            #if first word of phrase is found check for rest of phrase sequentially
            if word == _phrase_words[0]:
                _starting_index = _text_words.index(word)
                increment = 0 
                for elem in _phrase_words: 
                    if (_starting_index + increment) >= len(_text_words):
                        return False
                    if _text_words[_starting_index + increment] == _phrase_words[increment]:
                        increment = increment +1
                    else: 
                        return False
                return True
        

        
        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object
                
        title (string): title of element being triggered
        phrase(string): one or more words separated by a single space between the words.
        assume phrase does not contain punctuation

        A TitleTrigger object inherits from PhraseTrigger has two attributes:
            self._title (string, determined by input text)
            self.is_phrase_in_title (boolean, determined using helper function is_phrase_in)
        '''
        
        super().__init__(phrase)
        self._phrase = phrase
        #get passed in title from news story and compare to phrase called on method
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.is_phrase_in_title(story): 
            return True
        else:
            return False
        
    def is_phrase_in_title(self, story):
        _title = story.get_title()
        return self.is_phrase_in(_title)
    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object
                
        description (string): description of element being triggered
        phrase(string): one or more words separated by a single space between the words.
        assume phrase does not contain punctuation

        A TitleTrigger object inherits from PhraseTrigger has two attributes:
            self._description (string, determined by input text)
            self.is_phrase_in_title (boolean, determined using helper function is_phrase_in)
        '''
        
        super().__init__(phrase)
        self._phrase = phrase
        #get passed in title from news story and compare to phrase called on method
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.is_phrase_in_description(story): 
            return True
        else:
            return False
        
    def is_phrase_in_description(self, story):
        _description = story.get_description()
        return self.is_phrase_in(_description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, unformatted_time):
        '''
        Initializes a Trigger object
                
        time (string): needs to be converted to a datetime

        A TimeTrigger object inherits from Trigger has two attribute:
            self.unformatted_time (string, determined by input text)
            self._time (datetime, determined using helper function format_time)
            #how it will be called: TimeTrigger('12 Oct 2016 23:59:59')
            %d = Day of the month as a zero-padded decimal number.
            %b = Month as locale’s abbreviated name.
            %Y = Year with century as a decimal number.	
            %H = Hour (24-hour clock) as a zero-padded decimal number.
            %M = Minute as a zero-padded decimal number.
            %S = Second as a zero-padded decimal number.
        '''
        #The class's constructor should take in time in EST as a string in the
        #ormat of "3 Oct 2016 17:00:10 ".
        super().__init__()
        self.unformatted_time = unformatted_time
        
    def format_time(self, unformatted_time):
        _formatted_time = datetime.strptime(unformatted_time, "%d %b %Y %H:%M:%S")
        _formatted_time = _formatted_time.replace(tzinfo=pytz.timezone("EST"))
        return _formatted_time
    
        
    def get_time(self):
        return self.format_time(self.unformatted_time)
    
# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, unformatted_time):
        '''
        Initializes a TimeTrigger object
                
        description (string): description of element being triggered
        phrase(string): one or more words separated by a single space between the words.
        assume phrase does not contain punctuation

        A BeforeTrigger object inherits from Trigger has one attribute:
            self.unformatted_time (string, determined by input text)
            self._time (datetime, converted from passed time string)
            #how it will be called: TimeTrigger('12 Oct 2016 23:59:59')
            self.is_date_before (boolean, determined using helper function is_date_before)
        '''
        
        super().__init__(unformatted_time)
        self._time = self.get_time()
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.is_date_before(story): 
            return True
        else:
            return False
        
    def is_date_before(self, story):
        _pub_date = story.get_pubdate()
        if _pub_date < self._time: 
            return True
        else: 
            return False
        
class AfterTrigger(TimeTrigger):
    def __init__(self, unformatted_time):
        '''
        Initializes a TimeTrigger object
                
        description (string): description of element being triggered
        phrase(string): one or more words separated by a single space between the words.
        assume phrase does not contain punctuation

        A BeforeTrigger object inherits from Trigger has one attribute:
            self.unformatted_time (string, determined by input text)
            self._time (datetime, converted from passed time string)
            #how it will be called: TimeTrigger('12 Oct 2016 23:59:59')
            self.is_date_after (boolean, determined using helper function is_date_after)
        '''
        
        super().__init__(unformatted_time)
        self._time = self.get_time()
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.is_date_after(story): 
            return True
        else:
            return False
        
    def is_date_after(self, story):
        _pub_date = story.get_pubdate()
        if _pub_date > self._time: 
            return True
        else: 
            return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        '''
        Initializes a Trigger object
                
        Given a trigger T and a news item x , the output of the NOT trigger's
        evaluate method should be equivalent to not T.evaluate(x) .

        A NotTrigger object inherits from Trigger has two attributes:
            other_trigger = (Trigger) passed in to be inverted
        '''
        #The class's constructor should take in time in EST as a string in the
        #ormat of "3 Oct 2016 17:00:10 ".
        super().__init__()
        self.other_trigger = other_trigger
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.other_trigger.evaluate(story): 
            return False
        else:
            return True
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        '''
        Initializes a Trigger object
        Will fire on a news story only if both of the inputted triggers 
        would fire on that item


        A AndTrigger object inherits from Trigger has two attributes:
            trigger_one = (Trigger) passed in 
            trigger_two = (Trigger) passed in

        '''
        #The class's constructor should take in time in EST as a string in the
        #ormat of "3 Oct 2016 17:00:10 ".
        super().__init__()
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.trigger_one.evaluate(story): 
            if self.trigger_two.evaluate(story): 
                return True
        else:
            return False
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        '''
        Initializes a Trigger object
        Will fire on a news story if either of the inputted triggers 
        would fire on that item


        A AndTrigger object inherits from Trigger has two attributes:
            trigger_one = (Trigger) passed in 
            trigger_two = (Trigger) passed in

        '''
        #The class's constructor should take in time in EST as a string in the
        #ormat of "3 Oct 2016 17:00:10 ".
        super().__init__()
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two
        
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        if self.trigger_one.evaluate(story): 
            return True 
        
        if self.trigger_two.evaluate(story): 
            return True
        
        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    requested_stories = []
    for story in stories:
        for trig in triggerlist: 
            if trig.evaluate(story):
                requested_stories.append(story)
    return requested_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

