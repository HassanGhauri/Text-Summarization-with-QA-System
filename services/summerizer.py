# import and initialize the tokenizer and model from the checkpoint
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def summarize(input_file):
    checkpoint = "sshleifer/distilbart-cnn-12-6"
    result = ""
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
    # extract the sentences from the document
    import nltk
    nltk.download('punkt_tab')
    sentences = nltk.tokenize.sent_tokenize(input_file)
            
    # initialize
    length = 0
    chunk = ""
    chunks = []
    count = -1
    for sentence in sentences:
        count += 1
        combined_length = len(tokenizer.tokenize(sentence)) + length # add the no. of sentence tokens to the length counter

        if combined_length  <= tokenizer.max_len_single_sentence: # if it doesn't exceed
            chunk += sentence + " " # add the sentence to the chunk
            length = combined_length # update the length counter

            # if it is the last sentence
            if count == len(sentences) - 1:
                chunks.append(chunk.strip()) # save the chunk
        
        else: 
            chunks.append(chunk.strip()) # save the chunk
        
            # reset 
            length = 0 
            chunk = ""

            # take care of the overflow sentence
            chunk += sentence + " "
            length = len(tokenizer.tokenize(sentence))
    len(chunks)
    
    
    # inputs to the model
    inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]
        
    for input in inputs:
        output = model.generate(**input)
        result += tokenizer.decode(*output, skip_special_tokens=True)
    
    # print(result)
    return result




# # open and read the file from google drive
# file = open("./data2.txt", "r")
# input_file = file.read().strip()


# summarize(input_file)

