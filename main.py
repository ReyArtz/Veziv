import datetime
import os
from docx import Document
from groq import Groq


os.environ['GROQ_API_KEY'] = os.environ.get('GROQ_API_KEY', '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')


print("GROQ_API_KEY:", os.environ.get("GROQ_API_KEY"))

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def read_file(filepath):
    doc = Document(filepath)
    fulltext = []
    for paragraph in doc.paragraphs:
        fulltext.append(paragraph.text)
    return '\n'.join(fulltext)


def get_input():
    name = input("Introduceti numele fisierului .docx: ")
    output = input("Introduceti numele fisierului pentru salvare (fara extensie): ") + ".txt"
    return name.strip(), output.strip()


name, output = get_input()
offer_content = read_file(name)

complete = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": (
                f"Te rog sa construiesti un rezumat personalizat pentru aceasta oferta de job. "
                "Extrage urmatoarele informatii: "
                "Descrierea aplicatiei solicitate.\n"
                "Tehnologiile folosite pentru dezvoltarea aplicatiei (ex: stack tehnologic - front-end, back-end, baze de date, etc.).\n"
                "Task-urile concrete si detaliate necesare pentru dezvoltarea aplicatiei, "
                "inclusiv cele care nu sunt mentionate direct de client dar sunt necesare (ex: sectiuni financiare, facturare, etc.).\n\n"
                f"Aici sunt detaliile:\n{offer_content}"
            )
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

if hasattr(complete, 'choices') and complete.choices:
    print(complete.choices[0].message.content)
    
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(output, 'w', encoding='utf-8') as output_file:
        output_file.write(complete.choices[0].message.content)
    print(f"Rezumat salvat in: {output}")
else:
    print("Structura de raspuns neasteptata:", complete)
