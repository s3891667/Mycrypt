from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging


# Functions
def replace_vocab(statement):
    # Same Words
    statement = statement.lower().replace("cryptocurrency", "crypto")
    statement = statement.replace("cryptocurrencies", "crypto")
    statement = statement.replace("are", "is")
    # First Letter Capital
    statement = statement.capitalize()
    return statement


# Define ChatBot
bot = ChatBot(
    "MyCryptBot",
    preprocessors=[
        "chatterbot.preprocessors.clean_whitespace",
        "chatterbot.preprocessors.convert_to_ascii",
    ],
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "maximum_similarity_threshold": 0.8
        }
    ],
    database_uri="sqlite:///database.sqlite3"
)


# Logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


# Training
trainer = ListTrainer(bot)

trainer.train([
    "I am sorry, but I do not understand. Feel free to check the Learn documentation to see if it can answer any of "
    "your queries, or type 'Help' to see the list of questions you can ask.",
    "Help",
    "Here is a list of questions you can ask:"  # once trained, write this part
])

trainer.train([
    "What is crypto?",
    "1",
    "How do I purchase crypto?",
    "2",
    "How do I get crypto?",
    "2",
    "How do I store crypto?",
    "3",
    "What can I do with crypto?",
    "4",
    "How should I invest my money in crypto?",
    "5",
    "What are the dangers of investing in crypto?",
    "7",
    "How does crypto work?",
    "9",
    "How do I use crypto?",
    "10",
    "What does blockchain mean?",
    "6",
    "What is the most popular crypto?",
    "8",
    "What does the graph mean?",
    "11",
    "What is a candle?",
    "12",
    "What does candle mean?",
    "12",
    "How do I use the watchlist?",
    "13",
    "What does watching do?",
    "14",
    "What does the watchlist do?",
    "14",
    "What is market cap?",
    "15",
    "What does market cap mean?",
    "15",
    "What is volume?",
    "16",
    "What does volume mean?",
    "16",
    "What is circulating supply?",
    "17",
    "What does circulating supply mean?",
    "17",
    "What can I do?",
    "18",
    "What is MyCrypt?",
    "19",
    "How do I contact an admin?",
    "20",
    "What is a crypto wallet?",
    "21"
])


# Input Test
print("Hi. What would you like to know?")
while True:
    try:
        userInput = replace_vocab(input())
        # print(userInput)  # Test input
        botInput = bot.get_response(userInput)
        print(botInput)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break  # ctrl+c to break
