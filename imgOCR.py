from GeneralAgent import Agent
import os

img_path = r'.image/page_1.png'

# set the agent
key = os.getenv('OPEN_AI_KEY')
# role description
role_prompt = "You are an expert in Optical Character Recognition"
prompt = "Extract text information of the input image" \
         "Organize product-related information into a table in markdown format and return it." \
         "Without any additional explanation or content." \
         "Carefully check the information in the 'Product Description' column " \
         "(in German: 'Artikelbezeichnung' or 'Bezeichnung' or 'Produkt’)." \
         "The correct format for the string in this column should be: 'Product Name + Additional Information'. " \
         "For example: 'Giesinger Craft Lemondrop Triple 7.5% Vol. 20 × 330 ml'." \
         "The additional information is typically in the format: 'number × number [unit]', or simply 'number [unit]'." \
         "Some incorrect formats involve " \
         "the 'Additional Information' appearing in the middle of the product name string." \
         "For example: 'Giesinger Craft Lemondrop Triple 7.5% 20 × 330 ml Vol.'" \
         "Identify any instances of such incorrect information and correct them." \
         "Without any additional explanation or content."

agent_ocr = Agent(role_prompt, api_key=key)
extract_info = agent_ocr.user_input([prompt, {'image': img_path}], verbose=False)
