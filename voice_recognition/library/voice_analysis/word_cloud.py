import matplotlib.pyplot as plt
from wordcloud import WordCloud

def journalWordCloud(first_name:str, last_name:str) -> None:
    """
    This method will create a word cloud from the journal
    :param first_name:      The first name of the user
    :param last_name:    The last name of the user
    :return:    None
    """
    with open("Voice_To_Text_File.txt", "r") as f:
        data = f.read()
        f.close()
    wordcloud = WordCloud().generate(data)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.savefig("wordCloud.png")
    plt.show()
