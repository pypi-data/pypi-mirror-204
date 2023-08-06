import subprocess
import threading
import time
import re
import os
import openai
import pyttsx3

def speak(text):
    # initialize the text-to-speech engine
    engine = pyttsx3.init()

    # set the rate and volume of the voice
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    # ask the user for input
    # word = input(ticker)

    # speak the word
    engine.say(text)
    engine.runAndWait()

def chat(conversation,option):
    if len(conversation)>4096:
        prompt = conversation[-4096:]
    else:
        prompt = conversation
        
    if option=="explain":
        prompt=prompt+"\n explain above output."
    elif option=="suggest":
        prompt=prompt+"\n give debugging suggestions for above output."
    elif option=="chat":
        prompt==prompt
    elif option=="ask":
        prompt==prompt

    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a Windows debugger copilot."},
                {"role": "user", "content": "How to start debugging a memory dump?"},
                {"role": "assistant", "content": "You may run !analyze -v"},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        print(str(e))
        return str(e)
    # response=openai.Completion.create(
    # model="gpt-3.5-turbo",
    # prompt=output,
    # max_tokens=4096,
    # temperature=0
    # )
    text = response.choices[0].message.content.strip()
    print("\n"+text)
    return text

class ReaderThread(threading.Thread):
    def __init__(self, stream):
        super().__init__()
        self.buffer_lock = threading.Lock()
        self.stream = stream  # underlying stream for reading
        self.output = ""  # holds console output which can be retrieved by getoutput()

    def run(self):
        """
        Reads one from the stream line by lines and caches the result.
        :return: when the underlying stream was closed.
        """
        while True:
            try:
                line = self.stream.readline()  # readline() will block and wait for \r\n
            except Exception as e:
                line = str(e)
                print(str(e))
            if len(line) == 0:  # this will only apply if the stream was closed. Otherwise there is always \r\n
                break
            with self.buffer_lock:
                self.output += line

    def getoutput(self, timeout=0.1):
        """
        Get the console output that has been cached until now.
        If there's still output incoming, it will continue waiting in 1/10 of a second until no new
        output has been detected.
        :return:
        """
        temp = ""
        while True:
            time.sleep(timeout)
            if self.output == temp:
                break  # no new output for 100 ms, assume it's complete
            else:
                temp = self.output
        with self.buffer_lock:
            temp = self.output
            self.output = ""
        return temp

def start():
    print("\nThis software is used for Windows debugging learning purpose, please do not load any customer data, all input and output will be sent to OpenAI.")
    speak("This software is used for Windows debugging learning purpose, please do not load any customer data, all input and output will be sent to OpenAI.")

    print("\nHello, I am Windows debugger copilot, I'm here to assist you.")
    speak("Hello, I am Windows debugger copilot, I'm here to assist you.")

    print("\nFirst, please enter the windbg installation path which contains windbg.exe.")
    speak("First, please enter the windbg installation path which contains windbg.exe.")

    windbg_path = input("\nwindbg installation path which contains windbg.exe:")+r"\cdb.exe"

    while not os.path.exists(windbg_path):
        print("\nPath does not exist or does not include windbg.exe")
        speak("Path does not exist or does not include windbg.exe")
        windbg_path = input("\nwindbg installation path which contains windbg.exe:")+r"\cdb.exe"

    print("\nSecond, please enter the memory dump file path.")
    speak("Second, please enter the memory dump file path.")

    dumpfilename = input("\nMemory dump file path:")

    while not os.path.exists(dumpfilename):
        print("\nFile does not exist")
        speak("File does not exist")
        dumpfilename = input("\nMemory dump file path:")

    # command = r'C:\Program Files\Debugging Tools for Windows (x64)\cdb.exe'
    arguments = [windbg_path]
    arguments.extend(['-y', "srv*C:\symbols*https://msdl.microsoft.com/download/symbols"])  # Symbol path, may use sys.argv[1]
    # arguments.extend(['-i', sys.argv[2]])  # Image path
    arguments.extend(['-z', dumpfilename])  # Dump file
    arguments.extend(['-c', ".echo LOADING DONE"])
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True, encoding='utf-8')
    reader = ReaderThread(process.stdout)
    reader.start()

    result = ""
    while not re.search("LOADING DONE", result):
        result = reader.getoutput()  # ignore initial output

    def dbg(command):
        process.stdin.write(command+"\r\n")
        process.stdin.flush()
        result = reader.getoutput(2)
        return result

    # dump_type = ""

    print("\nSymbol path is set to srv*C:\symbols*https://msdl.microsoft.com/download/symbols, you may change the symbol path by running .sympath command")

    result = dbg("||")
    print("\n"+result)
    # speak(result)
    # if "user mini" in result:
    #     # dump_type="User"
    #     print("Yay, it's a User mode dump")
    #     # speak("Yay, it's a User mode dump")
    # elif "kernel" in result:
    #     # dump_type="Kernel"
    #     print("Yay, it's a Kernel mode dump")
        # speak("Yay, it's a Kernel mode dump")
        
    # result = dbg("!analyze -v")
    # print(result)
    # chat(result,"explain")
    # chat(result,"suggest")

    conversation=""
    while True:
        # Prompt the user for input
        
        # speak("Please enter your input.")
        user_input = input("\n"+'kd> ')
        
        # speak(user_input)
        if user_input.startswith("!chat"):
            text=chat(user_input,"chat")
            # speak(text)
        elif user_input.startswith("!explain"):
            # Print the output of cdb.exe
            text=chat(conversation,"explain")
            # speak(text)
        elif user_input.startswith("!suggest"):
            # Print the output of cdb.exe
            text=chat(conversation,"suggest")
            # speak(text)
        elif user_input.startswith("!ask"):
            # Print the output of cdb.exe
            question = conversation + "\n" + user_input[4:]
            text=chat(question,"ask")
            # speak(text)
        elif user_input.startswith("!q"):
            # Print the output of cdb.exe
            text=chat("Goodbye Windows debugger copilot, please quit","chat")
            speak(text)
            dbg("q")
            break
        elif user_input.startswith("!help"):
            help_msg = '''
            !chat <you may ask anything related to debugging>
            !ask <ask any question for the above output>
            !explain: explain the last output
            !suggest: suggest how to do next
            !q: quit
            '''
            print(help_msg)
            # speak(help_msg)
        else:
            # Send the user input to cdb.exe
            result = dbg(user_input)
            conversation += "\n"+result
            print("\n"+result)



start()