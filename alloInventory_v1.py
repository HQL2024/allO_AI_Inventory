from pdf2image import convert_from_path
from md2json import markdown_table_to_json
from GeneralAgent import Agent
import os


# role description
role_prompt = "You are an expert in Optical Character Recognition."
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


def splitPdf2Img(pdf_path, img_parent_dir):
    file_name = os.path.basename(pdf_path)
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        img_path = os.path.join(img_parent_dir, f'{file_name}_page_{i + 1}.png')
        image.save(img_path, 'PNG')
    print("--------pdf to images done!--------")
    return file_name, len(images)


def getMarkdown(num_img, img_dir, file_name):
    md_info = ''
    for i in range(num_img):
        print('For the {} page.'.format(i+1))
        img_path = os.path.join(img_dir, f'{file_name}_page_{i+1}.png')
        extract_info = agent_ocr.user_input([prompt, {'image': img_path}], verbose=False)
        md_info += extract_info
    return md_info


if __name__ == "__main__":
    pdf_file_path = r'./pdf/1.pdf'
    images_parent_dir = r'./pdf2images'
    json_file_path = r'./json'

    # step 1: convert pdf into images
    name, num_images = splitPdf2Img(pdf_file_path, images_parent_dir)

    # step 2: agent
    key = os.getenv("OPENAI_API_KEY")
    agent_ocr = Agent(role_prompt, api_key=key)

    # step 3: save the str-info of each page
    markdown_info = getMarkdown(num_images, images_parent_dir, name)

    # step 4: present the results
    print('\n--------show me results!---------\n')
    print(markdown_info)

    # step 5: convert into json files
    json_output = markdown_table_to_json(markdown_info, f'{name}_output', json_file_path)
    print('--------json saved!---------')