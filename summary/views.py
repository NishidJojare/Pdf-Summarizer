from django.shortcuts import render
from summary.forms import Upload_Pdf_Form
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from googletrans import Translator
import yake

# created function for extracting text from pdf
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()
    return text



# created function for uploading pdf 
def upload_pdf(request):
    if request.method=='POST':
        # getting fileds from form.py
        form=Upload_Pdf_Form(request.POST,request.FILES)
        
        # getting pdf file
        pdf_file = request.FILES['file']
        if form.is_valid():
            
            # get the length of pdf pages
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
             
            # if pdf contains greater than 15 pages then go further
            if num_pages >= 15:
                    uploaded_file = request.FILES['file']
                    
                    # extract the text from pdf file
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    
                    # generate summary of extracted text
                    parser = PlaintextParser.from_string(extracted_text, Tokenizer("english"))
                    summarizer = LsaSummarizer()
                    summary = summarizer(parser.document, sentences_count=5)  # Adjust sentences_count as needed
                    summary = " ".join(str(sentence) for sentence in summary)
                    
                    # get important keywords from summary
                    extracted_keywords = yake.KeywordExtractor()
                    keywords = extracted_keywords.extract_keywords(extracted_text)
                    word = [keyword[0] for keyword in keywords]
                    
                    translation_text = ""
                    translation_words = []
                    
                    # if user press for generate summary in english
                    if 'translate_to_english' in request.POST:
                        
                        translation_text = translate_to_english(summary)
                        translation_words = [translate_word_to_english(w) for w in word]

                    # if user press for generate summary in marathi
                    if 'translate_to_marathi' in request.POST:
                        
                        translation_text = translate_to_marathi(summary)
                        translation_words = [translate_word_to_marathi(w) for w in word]
                        
                    return render(request, 'index.html', {'form': form,
                                                          'translation_text': translation_text,
                                                          'translation_words': translation_words
                                                        })
                    
                    
                  
                       
            else:
                # else case if the pdf has less than 15 pages
                error_msg = "Can't upload: PDF should have more than 15 pages."
                return render(request, 'index.html', {'form': form, 'error_msg': error_msg})
              
    else:
        form = Upload_Pdf_Form()
        
    return render(request, 'index.html', {'form': form})



# function for english translation
def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='mr', dest='en')
    return translated_text.text
    
## for translating words
def translate_word_to_english(word):
    translator = Translator()
    translated_word = translator.translate(word, src='mr', dest='en')
    return translated_word.text
  


# function for marathi translation
def translate_to_marathi(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='mr')
    return translated_text.text

   
## for translating words in marathi
def translate_word_to_marathi(word):
    translator = Translator()
    translated_word = translator.translate(word, src='en', dest='mr')
    return translated_word.text
  