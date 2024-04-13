import streamlit as st
from langchain.prompts import PromptTemplate
import os
import warnings
warnings.filterwarnings("ignore")
import replicate
from replicate.client import Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="WellNest",
                   page_icon="https://i.pinimg.com/564x/93/35/fa/9335fa24c3134c50dca440a06206f7d7.jpg",
                   
                   layout="centered",
                   initial_sidebar_state="collapsed")


page_elements = """
<style>
[data-testid="stAppViewContainer"] {
  background-image: url("https://i.pinimg.com/originals/76/89/a9/7689a99ddfde89cedb0d098a57a5ac02.gif");
  background-size: cover;
  color: white;
}
/* Hide audio controls */
audio {
  visibility: hidden;
}
::placeholder {
  color: white;
  opacity: 1;
}
.stTextInput label,
.stSelectbox label {
  color: white !important;
  font-family: cursive;
}
</style>
"""

# Render page elements
st.markdown(page_elements, unsafe_allow_html=True)


# Embed audio using HTML audio tag with local file path
st.markdown("""
<audio controls autoplay>
  <source src="images/bgm.mp3" type="audio/mp3">
  Your browser does not support the audio element.
</audio>
""", unsafe_allow_html=True)
# Set the title text with custom CSS styling for color
st.markdown(
    """
    <h1 style="color:white;font-family: cursive;">WellNest</h1>
    """,
    unsafe_allow_html=True
)

# Apply custom styling using Markdown with HTML and CSS syntax
st.markdown(
    """
    <style>
    ::placeholder { /* Change placeholder color */
      color: white; /* Set the desired color */
      opacity: 1; /* Set opacity to make the text fully visible */
    }
    .stTextInput label { /* Change input label color */
      color: white !important; /* Set the desired color */
      font-family: cursive;
    }
   
   
    </style>
    """,
    unsafe_allow_html=True
)



import streamlit as st
import time

# Function to simulate a typing animation
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(50 / speed)

# Main content
text_content = "Hello !! I'm WellNest, your caring companion for wellness and hope... Developed by the Llama Chat Model from Meta, I'm here to provide real-time mental health insights. Feel free to ask me anything—You have me!"
speed = 100

# Check if typewriter animation has already been displayed
if 'typewriter_ran' not in st.session_state:
    st.session_state.typewriter_ran = True  # Set flag to indicate that the function has been executed
    typewriter(text=text_content, speed=speed)
else:
    # Display text directly without typing animation
    st.markdown(text_content)





system_prompt = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."


def blogs():
      os.makedirs("data", exist_ok=True)
      with open("data/blog.txt", "a", encoding="utf-8") as blog_file:
        for i in range(1, 6):  # Adjusted the range to fetch from 1 to 6 pages
            url = f"https://www.nami.org/Blogs/NAMI-Blog?page={i}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                col_divs = soup.find_all('div', class_='col-md-4 col-lg-3')

                for div in col_divs:
                    anchor_tags = div.find_all('a', href=True)

                    for anchor in anchor_tags:
                        blog_url = "https://www.nami.org" + anchor['href']
                        blog_response = requests.get(blog_url)
                        if blog_response.status_code == 200:
                            blog_soup = BeautifulSoup(blog_response.content, 'html.parser')
                            container = blog_soup.find('div', class_='content-container')
                            if container:
                                paragraphs = container.find_all(['p', 'h2'])
                                content = ""
                                for paragraph in paragraphs:
                                    content += paragraph.get_text() + "\n"

                                local_nami_index = content.find("Find Your Local NAMI")
                                if local_nami_index != -1:
                                    content = content[:local_nami_index]

                                # Append content to the blog.txt file
                                blog_file.write(content + "\n")

                                print(f"Content from {blog_url} appended to blog.txt.")
                        else:
                            print(f"Failed to fetch content from {blog_url}. Status code: {blog_response.status_code}")
            else:
                print(f"Failed to fetch HTML content for page {i}. Status code: {response.status_code}")

        print("All content appended to blog.txt successfully.")

def clean_filename(filename):
        return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in [' ', '.', '_', '-']]).rstrip()

def m_conditions():
    os.makedirs("data", exist_ok=True)

    url = "https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all section tags with class 'sectionPromowLinks'
        sections = soup.find_all('section', class_='sectionPromowLinks')

        # Iterate over each section
        for section in sections:
            # Get the heading text within the section
            heading = section.find('h3', class_='heading').get_text().strip()

            # Remove illegal characters from heading to use as filename
            filename = clean_filename(heading)

            # Get the ul tag within the section
            ul_tag = section.find('ul')

            # Create a directory for each section if it doesn't exist
            directory = f"{filename}"
            os.makedirs(directory, exist_ok=True)

            # Initialize variables to store content text
            overview_text = ""
            treatment_text = ""
            support_text = ""

            # Iterate over each li tag within the ul tag
            for idx, li_tag in enumerate(ul_tag.find_all('li'), start=1):
                # Get the href attribute value from the anchor tag
                href = li_tag.find('a')['href']

                # Construct the full URL
                full_url = f"https://www.nami.org{href}"

                # Fetch the content of the URL
                content_response = requests.get(full_url)

                if content_response.status_code == 200:
                    # Parse the content
                    content_soup = BeautifulSoup(content_response.content, 'html.parser')

                    # Extract the content text based on class
                    content_div = None

                    if "Treatment" in href:
                        content_div = content_soup.find('div', class_='treatments-content tab-content')
                        print("yest")
                        treatment_text += content_div.get_text(separator="\n\n") + "\n\n"

                    elif "Support" in href:
                        content_div = content_soup.find('div', class_='support-content tab-content')
                        print("yess")
                        support_text += content_div.get_text(separator="\n\n") + "\n\n"

                    else:
                        content_div = content_soup.find('div', class_='overview-content tab-content')
                        print("yes0")
                        overview_text += content_div.get_text(separator="\n\n") + "\n\n"

                else:
                    print(f"Failed to fetch content from {full_url}. Status code: {content_response.status_code}")

            # Write the concatenated content text to a single file
            with open(f"data/{filename}.txt", "w", encoding="utf-8") as file:
                file.write("Overview:\n\n" + overview_text)
                file.write("\n\nTreatment:\n\n" + treatment_text)
                file.write("\n\nSupport:\n\n" + support_text)

            print(f"Content saved to '{filename}.txt'")
    else:
        print(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

def m_illness():    
    os.makedirs("data", exist_ok=True)
    url = "https://www.nami.org/About-Mental-Illness/Common-with-Mental-Illness"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all section tags with class 'sectionPromowLinks'
        sections = soup.find_all('section', class_='sectionPromowLinks')

        # Iterate over each section
        for section in sections:
            # Get the heading text within the section
            heading = section.find('h3', class_='heading').get_text().strip()

            # Remove illegal characters from heading to use as filename
            filename = clean_filename(heading)

            # Get the ul tag within the section
            ul_tag = section.find('ul')

            # Create a directory for each section if it doesn't exist
            directory = f"{filename}"
            os.makedirs(directory, exist_ok=True)

            # Iterate over each li tag within the ul tag
            for idx, li_tag in enumerate(ul_tag.find_all('li'), start=1):
                # Get the href attribute value from the anchor tag
                href = li_tag.find('a')['href']

                # Construct the full URL
                full_url = f"https://www.nami.org{href}"

                # Fetch the content of the URL
                content_response = requests.get(full_url)

                if content_response.status_code == 200:
                    # Parse the content
                    content_soup = BeautifulSoup(content_response.content, 'html.parser')

                    # Check for the presence of specific classes and extract text accordingly
                    content_div = content_soup.find('div', class_='overview-content tab-content') or \
                                content_soup.find('div', class_='dynamic-content random-dynamic-content content')

                    if content_div:
                        content_text = content_div.get_text(separator="\n\n")

                        # Write the content to a file
                        with open(f"data/{filename}_{idx}.txt", "w", encoding="utf-8") as file:
                            file.write(content_text)

                        print(f"Content saved to '{filename}_{idx}.txt'")
                    else:
                        print(f"No suitable content found in {full_url}.")
                else:
                    print(f"Failed to fetch content from {full_url}. Status code: {content_response.status_code}")
    else:
        print(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")



def m_treatments():    
    os.makedirs("data", exist_ok=True)
    url = "https://www.nami.org/About-Mental-Illness/Treatments"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all section tags with class 'sectionPromowLinks'
        sections = soup.find_all('section', class_='sectionPromowLinks')

        # Iterate over each section
        for section in sections:
            # Get the heading text within the section
            heading = section.find('h3', class_='heading').get_text().strip()

            # Remove illegal characters from heading to use as filename
            filename = clean_filename(heading)

            # Get the ul tag within the section
            ul_tag = section.find('ul')

            # Create a directory for each section if it doesn't exist
            directory = f"{filename}"
            os.makedirs(directory, exist_ok=True)

            # Iterate over each li tag within the ul tag
            for idx, li_tag in enumerate(ul_tag.find_all('li'), start=1):
                # Get the href attribute value from the anchor tag
                href = li_tag.find('a')['href']

                # Construct the full URL
                full_url = f"https://www.nami.org{href}"

                # Fetch the content of the URL
                content_response = requests.get(full_url)

                if content_response.status_code == 200:
                    # Parse the content
                    content_soup = BeautifulSoup(content_response.content, 'html.parser')

                    # Check for the presence of specific classes and extract text accordingly
                    content_div = content_soup.find('div', class_='overview-content tab-content') or \
                                content_soup.find('div', class_='dynamic-content random-dynamic-content content')

                    if content_div:
                        content_text = content_div.get_text(separator="\n\n")

                        # Write the content to a file
                        with open(f"data/{filename}_{idx}.txt", "w", encoding="utf-8") as file:
                            file.write(content_text)

                        print(f"Content saved to '{filename}_{idx}.txt'")
                    else:
                        print(f"No suitable content found in {full_url}.")
                else:
                    print(f"Failed to fetch content from {full_url}. Status code: {content_response.status_code}")
    else:
        print(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

def process_documents(query,chunk_size=1000, chunk_overlap=20):
    # Scraping content from URLs
    directory = 'data/'
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)


    # Initializing SentenceTransformerEmbeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embeddings)

    # Performing similarity search
    matching_docs = db.similarity_search(query)

    return matching_docs    



def generate_response(query,matching_docs):
    PROMPT_TEMPLATE = f'''[INST]
    You are WellNest. Your goal is to help me in solving mental illness related doubts.
    You will be given a query and a series of answers solving that query. 
    You will respond  to me tailoring better friendly response .
    Make sure you do not include ulrelated things in your answer.
    You can suggest them online sites or resouces to help them to solve their problem if they want you to suggest them resources
    Provide response with 3 4 lines
    recent query :{query}
    context: {matching_docs}
    advice by YOU :

    [/INST]
'''
    api = Client(api_token=st.secrets["REPLICATE_API_TOKEN"])
    # api = Client(api_token="r8_1weJ3tgitKQyV71KXxaDqzGLhaCWMj30wgMZU")



    output = api.run(
        "meta/llama-2-7b-chat",
        input={
            "top_k": 0,
            "top_p": 1,
            "prompt": PROMPT_TEMPLATE,
            "temperature": 0.23,
            "system_prompt": system_prompt,
            "length_penalty": 1,
            "max_new_tokens":400,
            "prompt_template": "<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
            "presence_penalty": 0
        }
    )
    return ''.join([str(s) for s in output])



# Call data scraping functions
# m_conditions()
# m_illness()
# m_treatments()



# Initialize conversation memory if it doesn't exist
if 'conversation_memory' not in st.session_state:
    st.session_state.conversation_memory = []

# Function to display conversation
def display_conversation():
    text_area_style = """
    <style>
    textarea.stTextArea{
        background-color: skyblue !important;
        color: black !important;
    }
    textarea.stTextArea:nth-child(odd) > div > div > textarea {
        color: pink !important;
    }
    </style>
    """ 

        # Render the CSS style
    st.markdown(text_area_style, unsafe_allow_html=True)

# Display the text area with the specified text
    for i, text in enumerate(st.session_state.conversation_memory):
        # User messages on the right
        if text.startswith("You: "):
            with st.container():
                st.write('')
                col1, col2 = st.columns([1, 5])
                with col2:
                    num_lines = text.count('\n') + 1
                    st.text_area("", text[5:], key=f"text_{i}", height=num_lines)
        # Bot messages on the left
        elif text.startswith("Bot: "):
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    num_lines = text.count('\n') + 1
                    st.text_area("", text[5:], key=f"text_{i}", height=num_lines*10)
                st.write('')

# Display the chat
display_conversation()

# Footer text input for user query
input_key = 'input_key'  # Define the key for the text input
button_style = """
<style>
div.stButton>button {
    color: black !important;
}
</style>
"""

# Render button style
st.markdown(button_style, unsafe_allow_html=True)
# Display text input at the footer of the website
footer_container = st.container()
with footer_container:
    
    input_text = st.text_input("Share your Thoughts:", key=input_key, placeholder="Type here...", on_change=None)

if st.button('Ask'):
    st.session_state.conversation_memory.append(f"You: {input_text}")
    
    # Generate bot response (replace with your model's response generation code)
    matching_docs = process_documents(input_text)
    bot_response = generate_response(input_text, matching_docs)
    st.session_state.conversation_memory.append(f"Bot: {bot_response}")

    # Clear the text input
    # st.session_state[input_key] = ""

    # Rerun the app to update the conversation
    st.rerun()
