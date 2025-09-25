from openai import OpenAI              
import os                     ## machine operating system
import dotenv                  

dotenv.load_dotenv()                     #  load api key  from env
groq_key = os.getenv("GROQ_API_KEY")        ## get api key

# Groq client  = like it is the way to talk to the api                              
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")         

                    ## Task 1: Conversation Manager 

''' 1 create a class named cm
    2 default turns are 3
    3 create a list where we want to store chat
   4 store maximum number of turns
   5 count the chat turn'''



class ConversationManager:                        
    def __init__(self, k=3):                        
        self.history = []                             
        self.k = k                                   
        self.turn_count = 0                            



    ''' 1 create a function to add messages to the list we created above 
    2 append msgs in such a way that it include role and content 
    3 if we received and send message its count increases
    '''
    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self.turn_count += 1

        ''' 1 we will check the count of msgs if count will be divisible by k .. we summarize the entire chat'''

        if self.turn_count % self.k == 0:
            self.summarize_history()
    

    '''1. we get history of chat 
       2 if limit increased return last N msgs
       3 else return full history
       4 if char limit give or crossed --- truncate the string ...'''
    
    def get_history(self, limit=None, char_limit=None):
        history_text = ""
        if limit:
            messages = self.history[-limit:]
        else:
            messages = self.history    



        '''1 return the history as a string '''
        for m in messages:
            history_text += f"{m['role']}: {m['content']}\n"
            
            ''' if character limit is greater then we will cut the last text and add ... inplace like we use "to be continued" and break the text '''
            if char_limit and len(history_text) > char_limit:
                history_text = history_text[:char_limit] + "..."
                break
        return history_text
    
    '''Correct: summarize the entire history into a short text; first concatenate all messages into one string
    '''

    def summarize_history(self):
        text_to_summarize = ""
        for m in self.history:
            text_to_summarize += f"{m['role']}: {m['content']}\n"
         

        '''here we find out the response of the model 
        1  Call client.chat.completions.create to ask model for summary,
        
        2 response parameters are = model,messages
        3  use groq  model llama 3.1
        4 in messages  we see that msgs send to the system it summarize after 3 chats and return history     '''
        response = client.chat.completions.create(       ## client = groq connection,chat = chat style api,completion = jo adhuri baat reh gayi usko pura karna,create= create new connection
            model="llama-3.1-8b-instant",    
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize the conversation briefly."},
                {"role": "user", "content": text_to_summarize}            ## to give user's actual message here
            ]
        )
        ## response = when we call model it sends a response object,
        summary = response.choices[0].message.content   ## pehle answer ka actual text
        self.history = [{"role": "system", "content": f"Summary: {summary}"}]
        ## it replaces the old history in single summarized version kyunki next wale mein well set context mile bda nahi

# Demo Task 1
cm = ConversationManager(k=3)

cm.add_message("user", "Hi, I want to learn Artificial Intelligance.")
cm.add_message("assistant", "Sure, where do you want to start?")
cm.add_message("user", "Tell me about AI and how it is so popular now.")

print("History after 3rd turn (summary applied):")
print(cm.get_history())

cm.add_message("assistant", "AI is the science of making machines think and learn like humans, and it’s popular because it powers everyday tech like chatbots, recommendations, self-driving cars, and smart assistants..")
cm.add_message("user", "Give me some examples.")
cm.add_message("assistant", "Examples: , Siri,Alexa,self driving cars etc.")

print("\nHistory after 6th turn (another summary applied):")
print(cm.get_history())


                       ##  Task 2: JSON Schema Extraction 

'''this is dictionar just like json we want to extract useful data from its parameters like name,email,phone,age etc'''
schema = {
    "name": "extract_user_info",
    "description": "Extracts personal info from chat",   ##determine the purpose of schema
    "parameters": {   ## it shows which data should extract and in which format
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "location": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "email", "phone", "location", "age"]  ## these are mandatory fields
    }
}
''' same use llama 3 model so output follows the JSON schema'''
def extract_info(chat_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   
        messages=[    ## system = instruct to model that only extract the user info in json schema, user = jahan se info nikalna hai
            {"role": "system", "content": "Extract user info in JSON schema."},
            {"role": "user", "content": chat_text}
        ],
        tools=[{"type": "function", "function": schema}],
        tool_choice="auto"
    )


    return response.choices[0].message.tool_calls[0].function.arguments
##  response jo mujhe client chat completion se mila choice[0] mein mein extract karungi 1st wala,msg = ye actual reply hai model ka
## tool calls[0] = kyunki maine schema tool diya hai aur first wala nikal liya
## function arguments = it is extracted json data string



# Demo Task 2
chat1 = "Hi, my name is Mohit, I am 20 years old, from Kaithal. My email is navisharma204@gmail.com and my phone is 9812345786."
chat2 = "Hello, I'm Bob. 30 years old, living in Bangalore. My number is 9123456789 and my email is bob30@yahoo.com."
chat3 = "My name is Naveen, age 22, based in Panipat. Contact me at 9812345678 or naveen.panipat@gmail.com."

print("\nChat 1:", extract_info(chat1))
print("Chat 2:", extract_info(chat2))
print("Chat 3:", extract_info(chat3))
