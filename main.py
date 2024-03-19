import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_dict_results(request_word):
    url = f"http://sostik.info/word/?word={request_word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    vcb_words = soup.find_all('div', {'class': 'vcb_word'})
    dict_results = {}
    for vcb_word in vcb_words:
        vcb_word_top = vcb_word.find('span', {'class': 'vcb_word_top'}).text

        vcb_ps = vcb_word.find('span', {'class': 'vcb_ps'})
        if vcb_ps:
            vcb_ps = vcb_ps.text

        vcb_forms = vcb_word.find('span', {'class': 'vcb_forms'})
        if vcb_forms:
            vcb_forms = vcb_forms.text

        assert vcb_word_top not in dict_results

        dict_results[vcb_word_top] = {
            'vcb_ps': vcb_ps,
            'vcb_forms': vcb_forms,
            'vcb_word_top': vcb_word_top,
            'translations': []
        }
        vcb_translations = vcb_word.find_all('li', {'class': 'dec'})
        for vcb_translation in vcb_translations:
            translation_meaning = vcb_translation.find('span', {'class': 'black'})
            add_info = translation_meaning.find('span', {'class': 'italic'})

            translation_meaning = translation_meaning.text

            if add_info:
                add_info = add_info.text
                translation_meaning = translation_meaning.replace(add_info, '')

            kjh_examples = vcb_translation.find_all('span', {'class': 'brown'})
            ru_examples = vcb_translation.find_all('span', {'class': 'blue'})

            assert len(kjh_examples) == len(ru_examples)

            kjh_phrases = []
            ru_phrases = []
            for kjh_example, ru_example in zip(kjh_examples, ru_examples):
                kjh_phrases.append(kjh_example.text)
                ru_phrases.append(ru_example.text)

            translation_section = {
                'translation_meaning': translation_meaning,
                'add_info': add_info,
                'kjh_phrases': kjh_phrases,
                'ru_phrases': ru_phrases
            }
            dict_results[vcb_word_top]['translations'].append(translation_section)
    return dict_results


def main():
    request_word = "кӧс"
    dict_results = get_dict_results(request_word)

    print(dict_results)


if __name__ == '__main__':
    main()

    #print(words[0].find('span', {'class': 'vcb_word_top'}).text)


    # df = pd.read_csv("data/hrs_new34.csv")['field1']
    # count = 0
    # #line = df.sample().values[0]
    # #for line in df.values:
    # if True:
    #     #line = line.replace('<b></b>', ' ')
    #     #'<b> </b>'
    #     line = df.sample().values[0]
    #
    #     # remove words inside brackets
    #     # line = re.sub(r"[\(\[].*?[\)\]]", "", line)
    #
    #     for i, part in enumerate(line.split(";")):
    #         print(i, part, part.split("</b>"))
    #         if i == 0:
    #             pass
    #         else:
    #             phrases = part.split("</b>")
    #             if len(phrases) == 2:
    #                 pass
