import os


def split_documents(input_file='temp/all_documents.txt', documents_dir='documents', separator='__NEW_DOCUMENT__'):
    with open(input_file, 'r') as file:
        documents_str = file.read()

    documents_list = documents_str.split(separator)
   
    os.makedirs(documents_dir, exist_ok=True)

    for document in documents_list:
        document = document.strip()
        if document == '':
            continue

        title = document.split('\n')[0]
        output_file = title.replace(os.path.sep, ' - ') + '.txt'
        output_file = os.path.join(documents_dir, output_file)

        with open(output_file, 'w') as file:
            file.write(document)

        print(f"Document saved: {output_file}")


if __name__ == "__main__":
    split_documents()